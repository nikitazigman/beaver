# networking
variable "region" {
  description = "The AWS region to create resources in."
  default     = "eu-west-1"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["eu-west-1a", "eu-west-1b"]
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
  default = 1
}

variable "docker_image_api" {
  description = "Docker image to run in the ECS cluster"
  default     = "public.ecr.aws/d0s9n5w1/beaver-api-v2:latest"
}


variable "fargate_cpu" {
  description = "Amount of CPU for Fargate task. E.g., '256' (.25 vCPU)"
  default     = 256
}

variable "fargate_memory" {
  description = "Amount of memory for Fargate task. E.g., '512' (0.5GB)"
  default     = 512
}

variable "desired_tasks" {
  description = "Number of tasks to run"
  default     = 1
}

variable "autoscale_max" {
  description = "Maximum number of tasks to run"
  default     = 2
}

variable "autoscale_min" {
  description = "Minimum number of tasks to run"
  default     = 1
}


variable "db_name" {
  description = "DB database name"
  default     = "beaver"
}

variable "db_username" {
  description = "DB database username"
  default     = "beaver_owner"
}

variable "db_password" {
  description = "DB database password"
}

variable "api_secret" {
  description = "API secret"
}

variable "db_hostname" {
  description = "DB database hostname"
  default     = "ep-super-rice-abzeq4un-pooler.eu-west-2.aws.neon.tech"
}

variable "certificate_arn" {
  description = "AWS Certificate Manager ARN for validated domain"
  default     = "arn:aws:acm:eu-west-1:397234372915:certificate/3a8cdbdc-d433-4c2d-9d39-038908cda3a4"
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
