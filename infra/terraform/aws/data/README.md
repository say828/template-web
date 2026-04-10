# Terraform Data (template)

이 스택은 provider-first template layout에서 generic data plane skeleton을 제공한다.

- DynamoDB single-table
- S3 asset bucket

Downstream 저장소는 clone 후 `table_name`, `bucket_prefix`, `cors_allowed_origins`, `project_name`을 현재 서비스에 맞게 즉시 교체한다.

## Manual

```bash
terraform -chdir=infra/terraform/aws/data init
terraform -chdir=infra/terraform/aws/data plan \
  -var "phase=dev" \
  -var "project_name=example-service" \
  -var "table_name=example-service"
```
