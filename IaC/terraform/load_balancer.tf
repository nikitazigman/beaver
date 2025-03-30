resource "aws_lb" "production" {
  name               = "${var.ecs_cluster_name}-alb"
  load_balancer_type = "application"
  subnets            = aws_subnet.public[*].id
  security_groups    = [aws_security_group.load-balancer.id]
}

resource "aws_lb_target_group" "default-target-group" {
  name        = "${var.ecs_cluster_name}-tg"
  vpc_id      = aws_vpc.production-vpc.id
  protocol    = "HTTP"
  port        = 80
  target_type = "ip"

  health_check {
    path                = var.health_check_path
    port                = "traffic-port"
    healthy_threshold   = 5
    unhealthy_threshold = 2
    timeout             = 2
    interval            = 5
    matcher             = "200"
  }
}

# Listener (redirects traffic from the load balancer to the target group)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.production.id
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn
  depends_on        = [aws_lb_target_group.default-target-group]
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.default-target-group.arn
  }
}
