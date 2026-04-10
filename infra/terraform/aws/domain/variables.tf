variable "phase" {
  type        = string
  description = "Deployment phase."
  default     = "dev"
}

variable "root_domain" {
  type        = string
  description = "Hosted zone root domain."
  default     = "example.com"
}

variable "service_fqdn" {
  type        = string
  description = "Optional explicit final service domain."
  default     = ""
}

variable "aws_region" {
  type        = string
  description = "AWS region for Route53 and general provider calls."
  default     = "ap-northeast-2"
}

variable "target_ip" {
  type        = string
  description = "Origin target IPv4."
}

variable "origin_port" {
  type        = number
  description = "Origin backend port."
  default     = 8080
}

variable "ttl" {
  type        = number
  description = "DNS TTL."
  default     = 60
}

variable "enabled" {
  type        = bool
  description = "Enable record management."
  default     = true
}

variable "cdn_enabled" {
  type        = bool
  description = "Enable CloudFront distribution and alias record."
  default     = true
}

variable "cdn_price_class" {
  type        = string
  description = "CloudFront price class."
  default     = "PriceClass_200"
}
