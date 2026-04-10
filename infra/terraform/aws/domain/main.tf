provider "aws" {
  region = var.aws_region
}

provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

locals {
  phase       = lower(var.phase)
  root_domain = lower(trimspace(var.root_domain))
  service_fqdn = lower(
    trimspace(var.service_fqdn) != ""
    ? var.service_fqdn
    : (local.phase == "prod" ? local.root_domain : "dev.${local.root_domain}")
  )
  origin_fqdn = "origin.${local.service_fqdn}"
  origin_id   = replace(local.origin_fqdn, ".", "-")
}

data "aws_route53_zone" "root" {
  name         = "${local.root_domain}."
  private_zone = false
}

resource "aws_route53_record" "origin_a" {
  count   = var.enabled ? 1 : 0
  zone_id = data.aws_route53_zone.root.zone_id
  name    = local.origin_fqdn
  type    = "A"
  ttl     = var.ttl
  records = [var.target_ip]

  allow_overwrite = true
}

resource "aws_acm_certificate" "service" {
  count             = var.enabled && var.cdn_enabled ? 1 : 0
  provider          = aws.us_east_1
  domain_name       = local.service_fqdn
  validation_method = "DNS"
}

resource "aws_route53_record" "cert_validation" {
  for_each = var.enabled && var.cdn_enabled ? {
    for dvo in aws_acm_certificate.service[0].domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  } : {}

  zone_id = data.aws_route53_zone.root.zone_id
  name    = each.value.name
  type    = each.value.type
  ttl     = 60
  records = [each.value.record]

  allow_overwrite = true
}

resource "aws_acm_certificate_validation" "service" {
  count                   = var.enabled && var.cdn_enabled ? 1 : 0
  provider                = aws.us_east_1
  certificate_arn         = aws_acm_certificate.service[0].arn
  validation_record_fqdns = [for row in aws_route53_record.cert_validation : row.fqdn]
}

resource "aws_cloudfront_distribution" "service" {
  count           = var.enabled && var.cdn_enabled ? 1 : 0
  enabled         = true
  is_ipv6_enabled = true
  price_class     = var.cdn_price_class
  comment         = "template edge for ${local.service_fqdn}"
  aliases         = [local.service_fqdn]

  origin {
    domain_name = local.origin_fqdn
    origin_id   = local.origin_id

    custom_origin_config {
      http_port              = var.origin_port
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = local.origin_id
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD", "OPTIONS"]

    forwarded_values {
      query_string = true
      headers      = ["*"]

      cookies {
        forward = "all"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.service[0].certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  depends_on = [
    aws_route53_record.origin_a,
    aws_acm_certificate_validation.service,
  ]
}

resource "aws_route53_record" "service_alias" {
  count   = var.enabled && var.cdn_enabled ? 1 : 0
  zone_id = data.aws_route53_zone.root.zone_id
  name    = local.service_fqdn
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.service[0].domain_name
    zone_id                = aws_cloudfront_distribution.service[0].hosted_zone_id
    evaluate_target_health = false
  }

  allow_overwrite = true
}

resource "aws_route53_record" "service_a" {
  count   = var.enabled && !var.cdn_enabled ? 1 : 0
  zone_id = data.aws_route53_zone.root.zone_id
  name    = local.service_fqdn
  type    = "A"
  ttl     = var.ttl
  records = [var.target_ip]

  allow_overwrite = true
}
