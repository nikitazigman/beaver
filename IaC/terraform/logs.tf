
resource "aws_cloudwatch_log_group" "beaver-api-log-group" {
  name              = "/ecs/beaver-api"
  retention_in_days = var.log_retention_in_days
}
