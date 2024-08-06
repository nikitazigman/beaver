variable "region" {
  description = "The AWS region to create resources in."
  default     = "eu-west-2"
}

variable "public_subnet_1_cidr" {
  description = "CIDR Block for Public Subnet"
  default     = "10.0.1.0/24"
}
variable "private_subnet_1_cidr" {
  description = "CIDR Block for Private Subnet"
  default     = "10.0.2.0/24"
}
variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["eu-west-2a"]
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

variable "app_count" {
  description = "Number of Docker containers to run"
  default     = 2
}

variable "fargate_cpu" {
  description = "Amount of CPU for Fargate task. E.g., '256' (.25 vCPU)"
  default     = "256"
}

variable "fargate_memory" {
  description = "Amount of memory for Fargate task. E.g., '512' (0.5GB)"
  default     = "512"
}

variable "autoscale_min" {
  description = "Minimum autoscale (number of tasks)"
  default     = "1"
}

variable "autoscale_max" {
  description = "Maximum autoscale (number of tasks)"
  default     = "4"
}

variable "autoscale_desired" {
  description = "Desired number of tasks to run initially"
  default     = "2"
}