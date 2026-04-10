# template runtime delivery verification

## Status

- pass

## Retained Checks

- `rg -n "canonical dev-focused|dedicated host|AWS edge/domain|compose.yml" README.md infra/compose/README.md sdd/02_plan/06_iac/template_runtime_delivery.md sdd/03_build/06_iac/template_runtime_delivery.md sdd/99_toolchain/README.md sdd/99_toolchain/02_policies/compose-runtime-baseline-policy.md`
  - pass
  - root compose baseline과 dedicated overlay positioning이 target docs에서 같은 표현으로 유지된다.
- `rg -n '/home/sh/Documents/Github/templates/' . -g '*.md'`
  - pass
  - canonical template docs에 절대 filesystem 링크가 남아 있지 않다.
- `docker compose --env-file .env.example -f compose.yml config`
  - pass
- `docker compose --env-file infra/compose/.env.dev.example -f infra/compose/dev.yml config`
  - pass
- `docker compose --env-file infra/compose/.env.prod.example -f infra/compose/prod.yml config`
  - pass
- `docker compose --env-file .env.example -f compose.yml build server client-landing client-web client-mobile client-admin`
  - pass
- `SERVER_HTTP_PORT=38080 CLIENT_LANDING_PORT=33000 CLIENT_WEB_PORT=33001 CLIENT_MOBILE_PORT=33002 CLIENT_ADMIN_PORT=34000 docker compose --env-file .env.example -f compose.yml up -d postgres server client-landing client-web client-mobile client-admin`
  - pass
  - root compose baseline이 high-port override에서도 `postgres + server + 4 clients`를 모두 기동했다.
- `curl -sf http://127.0.0.1:38080/health`
  - pass
  - backend health 응답은 `{"status":"ok"}`였다.
- `SERVER_HTTP_PORT=38080 CLIENT_LANDING_PORT=33000 CLIENT_WEB_PORT=33001 CLIENT_MOBILE_PORT=33002 CLIENT_ADMIN_PORT=34000 docker compose --env-file .env.example -f compose.yml down`
  - pass
- `terraform -chdir=infra/terraform/aws/data init -backend=false && terraform -chdir=infra/terraform/aws/data validate`
  - pass
- `terraform -chdir=infra/terraform/aws/domain init -backend=false && terraform -chdir=infra/terraform/aws/domain validate`
  - pass
- `terraform -chdir=infra/terraform/openstack/server init -backend=false && terraform -chdir=infra/terraform/openstack/server validate`
  - pass
- `git diff --check -- README.md infra/compose/README.md sdd/02_plan/06_iac/template_runtime_delivery.md sdd/03_build/06_iac/template_runtime_delivery.md sdd/03_verify/06_iac/template_runtime_delivery.md sdd/99_toolchain/README.md sdd/99_toolchain/02_policies/compose-runtime-baseline-policy.md sdd/99_toolchain/02_policies/convention-storage-policy.md`
  - pass

## Residual Risk

- root compose service graph나 remote overlay 역할이 다시 바뀌면 README, IaC summary, toolchain policy를 같은 턴에 다시 맞춰야 한다.
