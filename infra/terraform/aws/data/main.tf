provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

locals {
  phase       = lower(var.phase)
  bucket_name = trimspace(var.bucket_name) != "" ? trimspace(var.bucket_name) : "${var.bucket_prefix}-${local.phase}-${data.aws_caller_identity.current.account_id}"
}

resource "aws_dynamodb_table" "app" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PK"
  range_key    = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  attribute {
    name = "GSI1PK"
    type = "S"
  }

  attribute {
    name = "GSI1SK"
    type = "S"
  }

  attribute {
    name = "GSI2PK"
    type = "S"
  }

  attribute {
    name = "GSI2SK"
    type = "S"
  }

  global_secondary_index {
    name            = "GSI1"
    hash_key        = "GSI1PK"
    range_key       = "GSI1SK"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "GSI2"
    hash_key        = "GSI2PK"
    range_key       = "GSI2SK"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = local.phase == "prod"
  }

  tags = {
    Name        = var.table_name
    Project     = var.project_name
    Phase       = local.phase
    ManagedBy   = "terraform"
    ManagedVia  = "aws"
    DataSurface = "dynamodb"
  }
}

resource "aws_s3_bucket" "assets" {
  bucket        = local.bucket_name
  force_destroy = var.force_destroy

  tags = {
    Name        = local.bucket_name
    Project     = var.project_name
    Phase       = local.phase
    ManagedBy   = "terraform"
    ManagedVia  = "aws"
    DataSurface = "s3"
  }
}

resource "aws_s3_bucket_versioning" "assets" {
  bucket = aws_s3_bucket.assets.id

  versioning_configuration {
    status = local.phase == "prod" ? "Enabled" : "Suspended"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "assets" {
  bucket = aws_s3_bucket.assets.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "assets" {
  bucket = aws_s3_bucket.assets.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = var.public_read_enabled ? false : true
  restrict_public_buckets = var.public_read_enabled ? false : true
}

resource "aws_s3_bucket_cors_configuration" "assets" {
  bucket = aws_s3_bucket.assets.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE"]
    allowed_origins = var.cors_allowed_origins
    expose_headers  = ["ETag"]
    max_age_seconds = 3600
  }
}

resource "aws_s3_bucket_policy" "public_read" {
  count  = var.public_read_enabled ? 1 : 0
  bucket = aws_s3_bucket.assets.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = ["s3:GetObject"]
        Resource  = ["${aws_s3_bucket.assets.arn}/*"]
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.assets]
}
