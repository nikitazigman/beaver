resource "aws_ecs_cluster" "main" {
  name = "beaver-cluster"
}

resource "aws_ecs_capacity_provider" "main" {
  name = "main-ecs-ec2"

  auto_scaling_group_provider {
    auto_scaling_group_arn         = aws_autoscaling_group.ecs.arn
    managed_termination_protection = "DISABLED"

    managed_scaling {
      maximum_scaling_step_size = 2
      minimum_scaling_step_size = 1
      status                    = "ENABLED"
      target_capacity           = 100
    }
  }
}

resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name       = aws_ecs_cluster.main.name
  capacity_providers = [aws_ecs_capacity_provider.main.name]

  default_capacity_provider_strategy {
    capacity_provider = aws_ecs_capacity_provider.main.name
    base              = 1
    weight            = 100
  }
}

data "aws_iam_policy_document" "ecs_task_doc" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_role" {
  name_prefix        = "ecs-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_doc.json
}

resource "aws_iam_role" "ecs_exec_role" {
  name_prefix        = "ecs-exec-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_doc.json
}

resource "aws_iam_role_policy_attachment" "ecs_exec_role_policy" {
  role       = aws_iam_role.ecs_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "app" {
  family                   = "beaver-api"
  network_mode             = "awsvpc" # Required for Fargate
  requires_compatibilities = ["EC2"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  execution_role_arn       = aws_iam_role.ecs_exec_role.arn
  depends_on               = [aws_db_instance.production]
  runtime_platform {
    cpu_architecture = "ARM64"
  }
  volume {
    name = "efs-volume"
    efs_volume_configuration {
      file_system_id          = aws_efs_file_system.efs.id
      root_directory          = "/"
      transit_encryption      = "ENABLED"
      transit_encryption_port = 2049
      authorization_config {
        access_point_id = aws_efs_access_point.app_access_point.id
        iam             = "ENABLED"
      }
    }
  }
  container_definitions = jsonencode([
    {
      name      = "beaver-api"
      image     = "public.ecr.aws/d0s9n5w1/beaver-api:latest",
      cpu       = floor(var.task_cpu * 0.8),
      memory    = floor(var.task_memory * 0.8),
      essential = true,
      command   = ["sh", "start.sh"],
      environment = [
        {
          "name" : "DEBUG",
          "value" : "False"
        },
        {
          "name" : "ALLOWED_HOSTS",
          "value" : "*"
        },
        {
          "name" : "RDS_DB_NAME",
          "value" : var.rds_db_name
        },
        {
          "name" : "RDS_USERNAME",
          "value" : var.rds_username
        },
        {
          "name" : "RDS_PASSWORD",
          "value" : var.rds_password
        },
        {
          "name" : "RDS_HOSTNAME",
          "value" : aws_db_instance.production.address
        },
        {
          "name" : "RDS_PORT",
          "value" : "5432"
        }
      ],
      mountPoints = [
        {
          containerPath = "/opt/app/static",
          sourceVolume  = "efs-volume",
          readOnly      = false

        }
      ],
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/beaver-api"
          awslogs-region        = var.region
          awslogs-stream-prefix = "ecs"
        }
      }
      portMappings = [
        {
          containerPort = 8000
          protocol      = "tcp"
        }
      ]
    },
    {
      name      = "beaver-nginx",
      image     = "public.ecr.aws/d0s9n5w1/beaver-nginx:latest",
      cpu       = floor(var.task_cpu * 0.2),
      memory    = floor(var.task_memory * 0.2),
      essential = true,
      portMappings = [
        {
          containerPort = 80,
          protocol      = "tcp"
        }
      ],
      mountPoints = [
        {
          containerPath = "/opt/app/static",
          sourceVolume  = "efs-volume",
          readOnly      = false

        }
      ],
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/nginx",
          awslogs-region        = var.region,
          awslogs-stream-prefix = "nginx-log-stream"
        }
      }
    }
    ]
  )
}

resource "aws_security_group" "ecs_task" {
  name_prefix = "ecs-task-sg-"
  description = "Allow all traffic within the VPC"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_service" "app" {
  name                               = "app"
  cluster                            = aws_ecs_cluster.main.id
  task_definition                    = aws_ecs_task_definition.app.arn
  desired_count                      = var.desired_tasks
  force_new_deployment               = true
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 100


  network_configuration {
    security_groups = [aws_security_group.ecs_task.id]
    subnets         = aws_subnet.public[*].id
  }

  capacity_provider_strategy {
    capacity_provider = aws_ecs_capacity_provider.main.name
    base              = 1
    weight            = 100
  }

  ordered_placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "beaver-nginx"
    container_port   = 80
  }
  triggers = {
    redeployment = plantimestamp()
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}
