output "service_fqdn" {
  value       = local.service_fqdn
  description = "Managed public service domain."
}

output "origin_fqdn" {
  value       = local.origin_fqdn
  description = "Origin DNS name that points to the OpenStack backend."
}

output "origin_url" {
  value       = "http://${local.origin_fqdn}:${var.origin_port}"
  description = "Origin URL that CloudFront points to."
}

output "root_domain" {
  value       = local.root_domain
  description = "Resolved root domain."
}

output "cloudfront_domain_name" {
  value       = var.cdn_enabled ? aws_cloudfront_distribution.service[0].domain_name : ""
  description = "CloudFront distribution domain."
}

output "cloudfront_distribution_id" {
  value       = var.cdn_enabled ? aws_cloudfront_distribution.service[0].id : ""
  description = "CloudFront distribution id."
}
