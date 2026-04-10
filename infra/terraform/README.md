# Template Terraform Layout

`templates`의 canonical Terraform 구조는 provider-first 기준으로 정리한다.

```text
infra/terraform/
  aws/
    data/       # generic DynamoDB single-table + S3 asset bucket skeleton
    domain/     # Route53 + ACM + CloudFront edge skeleton
  openstack/
    server/     # Aspace/OpenStack backend compute skeleton
    dev/        # lower-level environment root starter
    prod/       # lower-level environment root starter
```

## Current Policy

- public entry와 edge는 `aws/domain`이 담당한다.
- application data plane은 필요 시 `aws/data` skeleton을 clone 후 repository-specific shape로 구체화한다.
- backend compute는 `openstack/server`에서 Aspace/OpenStack 기준으로 관리한다.
- `openstack/dev`, `openstack/prod`는 lower-level starter root로 남겨 두되 canonical split 설명은 `openstack/server`를 우선한다.

## Manual Validation

```bash
terraform -chdir=infra/terraform/aws/data init -backend=false
terraform -chdir=infra/terraform/aws/data validate

terraform -chdir=infra/terraform/aws/domain init -backend=false
terraform -chdir=infra/terraform/aws/domain validate

terraform -chdir=infra/terraform/openstack/server init -backend=false
terraform -chdir=infra/terraform/openstack/server validate
```
