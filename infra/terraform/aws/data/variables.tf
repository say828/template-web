variable "aws_region" {
  type        = string
  description = "AWS region."
  default     = "ap-northeast-2"
}

variable "phase" {
  type        = string
  description = "Deployment phase."
  default     = "prod"
}

variable "table_name" {
  type        = string
  description = "Application DynamoDB table name."
  default     = "template-service"
}

variable "project_name" {
  type        = string
  description = "Project tag used across resources."
  default     = "template-service"
}

variable "bucket_name" {
  type        = string
  description = "Optional explicit bucket name."
  default     = ""
}

variable "bucket_prefix" {
  type        = string
  description = "Bucket prefix used when bucket_name is empty."
  default     = "template-assets"
}

variable "cors_allowed_origins" {
  type        = list(string)
  description = "Allowed origins for browser asset access."
  default = [
    "https://app.example.com",
    "https://admin.example.com",
    "https://dev.example.com"
  ]
}

variable "public_read_enabled" {
  type        = bool
  description = "Allow public read access for uploaded image objects."
  default     = true
}

variable "force_destroy" {
  type        = bool
  description = "Allow bucket destroy with objects."
  default     = false
}
