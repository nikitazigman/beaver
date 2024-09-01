
resource "aws_cloudwatch_log_group" "django-log-group" {
  name              = "/ecs/beaver-api"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_group" "nginx-log-group" {
  name              = "/ecs/nginx"
  retention_in_days = 30
}