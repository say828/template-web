# OpenStack Terraform

OpenStack provider는 공용 축으로 두되, canonical compute baseline은 `server/` root를 우선한다.

구조:

- `modules/environment_host`: OpenStack Docker host 공통 module
- `server/`: Aspace/OpenStack backend compute canonical root
- `dev/`: DEV(개발계)용 Terraform root
- `prod/`: PROD용 Terraform root

원칙:

- canonical delivery split에서는 `openstack/server`가 backend compute를 담당하고, `aws/domain`과 `aws/data`가 외곽 surface를 담당한다.
- DEV(개발계)와 PROD는 state를 분리한다.
- compose 자동 기동이 필요하면 각 환경 root의 `compose_env_content`에 대응 환경의 `.env` 전체를 넣는다.
- 네트워크를 공유하려면 `create_network=false`와 `network_id`/`subnet_id`를 사용한다.

사용:

```bash
cd infra/terraform/openstack/server
cp zz_aspace.auto.tfvars.example.json zz_aspace.auto.tfvars.json
terraform init -backend=false
terraform validate

cd infra/terraform/openstack/dev
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform validate
terraform plan

cd ../prod
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform validate
terraform plan
```
