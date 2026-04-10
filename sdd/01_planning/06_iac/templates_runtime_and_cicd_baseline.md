# templates runtime and cicd baseline

- 작성 버전: 1.0.0

## Purpose

템플릿 저장소의 root compose runtime baseline과 CI baseline을 정리한다.

## 1. Compose Runtime Baseline

| Surface | Default Port |
| --- | --- |
| landing | `3000` |
| web | `3001` |
| mobile | `3002` |
| admin | `4000` |
| api | `8000` |

## 2. Compose Rule

- root `compose.yml`이 canonical dev-focused runtime baseline이다.
- dedicated host용 DEV(개발계)/PROD overlay는 `infra/compose/dev.yml`, `infra/compose/prod.yml`을 사용한다.
- 환경변수 contract는 `.env.example`을 source-of-truth로 유지한다.

## 3. CI/CD Rule

- 이 레포는 템플릿 저장소이므로 실제 배포를 수행하지 않는다.
- `.github/workflows`는 다음만 책임진다.
  - root compose/overlay config validation
  - backend test
  - frontend build matrix
  - AST build audit와 parity target resolution
  - canonical Terraform skeleton validate

## 4. Delivery Note

- 실제 서비스 레포로 clone된 뒤 DEV/PROD deploy workflow를 추가한다.
- template repo의 workflow는 `검증용 CI`만 유지한다.

## 5. Remote Infra Template Layout

- canonical Terraform split은 `infra/terraform/aws/data`, `infra/terraform/aws/domain`, `infra/terraform/openstack/server`다.
- `infra/terraform/openstack/dev`, `infra/terraform/openstack/prod`는 lower-level starter root로 유지한다.
- 공통 OpenStack host/network/security group 로직은 `infra/terraform/openstack/modules/environment_host`에 둔다.
- DEV(개발계)와 PROD는 별도 Terraform state를 사용한다.
- cloud-init compose 자동 기동은 각 환경 root의 `compose_env_content`와 `deploy_compose_on_boot`로 제어한다.
