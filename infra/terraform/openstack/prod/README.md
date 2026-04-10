# OpenStack PROD

PROD 전용 Terraform root다.

사용:

```bash
cd infra/terraform/openstack/prod
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform validate
terraform plan
```

메모:

- 기본 compose 파일은 `infra/compose/prod.yml`이다.
- cloud-init 자동 기동을 쓰려면 `compose_env_content`에 `infra/compose/.env.prod` 전체를 넣는다.
