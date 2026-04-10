output "table_name" {
  value       = aws_dynamodb_table.app.name
  description = "Active application DynamoDB table."
}

output "bucket_name" {
  value       = aws_s3_bucket.assets.bucket
  description = "Active application S3 bucket."
}

output "bucket_public_url" {
  value       = "https://s3.${var.aws_region}.amazonaws.com"
  description = "Public S3 endpoint base used by the current backend."
}
