# OpenStack DEV

DEV(개발계) 전용 Terraform root다.

사용:

```bash
cd infra/terraform/openstack/dev
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform validate
terraform plan
```

메모:

- 기본 compose 파일은 `infra/compose/dev.yml`이다.
- cloud-init 자동 기동을 쓰려면 `compose_env_content`에 `infra/compose/.env.dev` 전체를 넣는다.
