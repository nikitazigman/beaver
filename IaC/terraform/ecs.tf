resource "aws_ecs_cluster" "production" {
  name = "beaver-cluster"
}


resource "aws_ecs_task_definition" "app" {
  family                   = "beaver-api"
  network_mode             = "awsvpc" # Required for Fargate
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs-task-execution-role.arn
  task_role_arn            = aws_iam_role.ecs-task-execution-role.arn
  runtime_platform {
    cpu_architecture = "ARM64"
  }
  container_definitions = jsonencode([
    {
      name      = "beaver-api"
      image     = "public.ecr.aws/d0s9n5w1/beaver-api:latest",
      cpu       = var.fargate_cpu,
      memory    = var.fargate_memory,
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
          "value" : var.rds_hostname
        },
        {
          "name" : "RDS_PORT",
          "value" : "5432"
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
    }
    ]
  )
}

resource "aws_ecs_service" "app" {
  name                 = "beaver-api"
  cluster              = aws_ecs_cluster.production.id
  task_definition      = aws_ecs_task_definition.app.arn
  desired_count        = var.desired_tasks
  force_new_deployment = true
  launch_type          = "FARGATE"

  network_configuration {
    security_groups  = [aws_security_group.ecs-fargate.id]
    subnets          = aws_subnet.public[*].id
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.default-target-group.arn
    container_name   = "beaver-api"
    container_port   = 8000
  }
  triggers = {
    redeployment = plantimestamp()
  }
  lifecycle {
    ignore_changes = [desired_count]
  }
}
