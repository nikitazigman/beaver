data "aws_route53_zone" "beaver_api" {
  name = var.domain_name
}

resource "aws_route53_record" "site_domain" {
  zone_id = data.aws_route53_zone.beaver_api.zone_id
  name    = var.record_name
  type    = "A"

  alias {
    name                   = aws_lb.production.dns_name
    zone_id                = aws_lb.production.zone_id
    evaluate_target_health = true
  }
}