# template runtime delivery

## Covered Planning Artifact

- `sdd/02_plan/06_iac/template_runtime_delivery.md`

## Structure Tree

- template runtime delivery
  - root compose baseline
    - 4개 frontend surface
    - `server` HTTP runtime
    - 기본 `postgres`
    - optional DB profile: `mysql`, `mariadb`, `mongo`
  - dedicated host overlay
    - `infra/compose/dev.yml`
    - `infra/compose/prod.yml`
  - provider-first delivery topology
    - `infra/terraform/aws/domain`
    - `infra/terraform/openstack/server`
    - `infra/terraform/aws/data`

## Cross-Cutting Links

- root `compose.yml`은 템플릿 저장소의 canonical dev-focused runtime baseline이자 초기 검증 진입점이다.
- `infra/compose/dev.yml`, `infra/compose/prod.yml`은 dedicated DEV(개발계)/PROD host layout을 위한 overlay다.
- remote delivery topology는 `AWS edge/domain -> OpenStack backend compute -> AWS data plane` current split을 따른다.
- CI workflow는 current compose/runtime baseline과 provider-first Terraform skeleton을 함께 검증한다.

## Key Modules And Contracts

- `compose.yml`
- `.env.example`
- `server/Dockerfile.dev`
- `server/docker-entrypoint.sh`
- `client/landing/Dockerfile.dev`
- `client/web/Dockerfile.dev`
- `client/mobile/Dockerfile.dev`
- `client/admin/Dockerfile.dev`
- `infra/compose/dev.yml`
- `infra/compose/prod.yml`
- `infra/compose/.env.dev.example`
- `infra/compose/.env.prod.example`
- `infra/terraform/README.md`
- `infra/terraform/aws/data/`
- `infra/terraform/aws/domain/`
- `infra/terraform/openstack/server/`
- `.github/workflows/ci.yml`
- `.github/workflows/frontend-parity.yml`
