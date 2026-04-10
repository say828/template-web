# build ast runtime tree governance

- Owner: Codex
- Status: active

## Scope

- In scope:
  - `sdd/03_build` service summary를 실제 템플릿 runtime assembly 기준으로 재정렬한다.
  - Claude/Codex/Ralph 하네스가 동일한 current-state build reading 규칙을 따르도록 canonical policy를 추가한다.
  - `scripts/dev/audit_sdd_build_ast.py`를 템플릿 정본 gate로 유지한다.
  - provider-first infra baseline과 build/runtime/toolchain 문서 간의 current-state drift를 줄인다.
- Out of scope:
  - 템플릿 앱/서버의 기능 요구사항 자체 변경
  - 제품별 downstream branding이나 credential 값 추가

## Assumptions

- template repo의 `sdd/03_build`는 clone 이후 downstream repo가 그대로 이어받는 current-state 설명 문서다.
- AST-style build 문서는 모든 관계를 하나의 트리에 과적재하지 않고, 주 runtime chain과 cross-cutting contract를 분리해 설명한다.
- agentic harness는 repo-local path와 generic scaffold만 포함하고 실제 run 산출물은 commit 대상이 아니다.

## Acceptance Criteria

- [x] `scripts/dev/audit_sdd_build_ast.py`가 `ast_similarity=10`, `implementation_traceability=10`, `human_agent_readability=10`을 반환한다.
- [x] `mobile`, `web`, `admin`, `landing` service summary가 실제 `main.tsx -> AuthProvider -> BrowserRouter -> App -> ProtectedRoute/shell -> route leaf` 체인을 반영한다.
- [x] `README`, `AGENTS`, `CLAUDE`, toolchain policy가 `.agent`, role agent, skill alias, AST current-state 규칙을 같이 설명한다.
- [x] template infra 문서는 provider-first baseline(`aws/data`, `aws/domain`, `openstack/server`)을 current canonical split으로 설명한다.

## Execution Checklist

- [x] 기존 템플릿의 agentic/toolchain/AST 누락 축을 정리한다.
- [x] `.agent` Ralph scaffold와 Claude/Codex alias/role surface를 추가한다.
- [x] AST audit script와 plan/build/verify current-state 문서를 추가한다.
- [x] service build summary를 runtime tree 기준으로 재작성한다.
- [x] infra current-state 문서를 provider-first baseline으로 갱신한다.
- [x] root compose baseline을 provider-first runtime split까지 더 일반화할 추가 필요 여부를 follow-up으로 평가한다.

## Work Log

- 2026-03-19: `templates`가 starter scaffold로는 충분하지만 `passv`/`palcar`에서 검증된 agentic harness, AST build governance, provider-first infra split이 빠져 있어 canonical repo로 승격이 필요하다고 정리했다.
- 2026-03-19: `.agent` Ralph scaffold, Claude role agent surface, Codex alias skill, OTRO validation helper 문서를 정본에 추가하기로 결정했다.
- 2026-03-19: `sdd/03_build/01_feature/service/*.md`를 실제 템플릿 runtime composition 기준으로 다시 쓰고 AST gate로 검증하는 흐름을 고정했다.
- 2026-03-19: infra current-state는 기존 `openstack/dev|prod` 설명에 더해 `aws/data`, `aws/domain`, `openstack/server` provider-first split을 canonical baseline으로 반영했다.
- 2026-03-19: AST gate와 `terraform validate` 3종이 모두 통과해 canonical template upgrade의 구조적 baseline을 고정했다.

## Validation

- `python3 scripts/dev/audit_sdd_build_ast.py --write .agent/sdd-build-ast-audit.json`
- `rg -n "Ralph|iteration|Current Build Note|2026-" sdd/03_build -g '*.md'`
- `terraform -chdir=infra/terraform/aws/data init -backend=false && terraform -chdir=infra/terraform/aws/data validate`
- `terraform -chdir=infra/terraform/aws/domain init -backend=false && terraform -chdir=infra/terraform/aws/domain validate`
- `terraform -chdir=infra/terraform/openstack/server init -backend=false && terraform -chdir=infra/terraform/openstack/server validate`
