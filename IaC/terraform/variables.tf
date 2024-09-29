# networking
variable "region" {
  description = "The AWS region to create resources in."
  default     = "eu-west-2"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["eu-west-2a", "eu-west-2b"]
}

variable "health_check_path" {
  description = "Health check path for the default target group"
  default     = "/ping/"
}

variable "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  default     = "production"
}

variable "log_retention_in_days" {
  default = 30
}

variable "docker_image_url_django" {
  description = "Docker image to run in the ECS cluster"
  default     = "public.ecr.aws/d0s9n5w1/beaver-api:latest"
}

variable "desired_tasks" {
  description = "Number of tasks to run"
  default     = 2
}

variable "instance_type" {
  description = "Instance type for the ECS cluster"
  default     = "t4g.nano"
}

variable "task_cpu" {
  description = "Amount of CPU for Fargate task. E.g., '256' (.25 vCPU)"
  default     = 1000 * 2
}

variable "task_memory" {
  description = "Amount of memory for Fargate task. E.g., '512' (0.5GB)"
  default     = 400
}

variable "autoscale_min" {
  description = "Minimum autoscale (number of tasks)"
  default     = 2
}

variable "autoscale_max" {
  description = "Maximum autoscale (number of tasks)"
  default     = 2
}


variable "rds_db_name" {
  description = "RDS database name"
  default     = "postgres"
}

variable "rds_username" {
  description = "RDS database username"
  default     = "postgres"
}

variable "rds_password" {
  description = "RDS database password"
}

variable "rds_instance_class" {
  description = "RDS instance type"
  default     = "db.t4g.micro"
}

variable "certificate_arn" {
  description = "AWS Certificate Manager ARN for validated domain"
  default     = "arn:aws:acm:eu-west-2:397234372915:certificate/f1b8c29c-589a-4a1f-af43-b47d9150a278"
}

# route 53 variables
variable "domain_name" {
  description = "Domain name for the hosted zone"
  default     = "beaver-api.com"
}

variable "record_name" {
  description = "Subdomain name for the hosted zone"
  default     = ""
}

variable "docker_image_url_nginx" {
  description = "Docker nginx image to run in the ECS cluster"
  default     = "public.ecr.aws/d0s9n5w1/beaver-nginx:latest"
}
