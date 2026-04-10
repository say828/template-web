# Terraform Domain (template)

이 스택은 template repo의 AWS 도메인/엣지 skeleton을 제공한다.
Route53 hosted zone은 `root_domain` 기준으로 조회하고, 서비스 FQDN은 기본적으로 `dev.<root_domain>` 또는 `<root_domain>` 규칙으로 계산한다.

## Domain Policy

- DEV(개발계): `dev.<root_domain>`
- PROD: `<root_domain>`
- clone 후 `root_domain`, `service_fqdn`, `target_ip`는 현재 서비스에 맞게 바로 교체한다.

## Manual

```bash
terraform -chdir=infra/terraform/aws/domain init
terraform -chdir=infra/terraform/aws/domain plan \
  -var "phase=dev" \
  -var "root_domain=example.com" \
  -var "target_ip=203.0.113.10"
```
