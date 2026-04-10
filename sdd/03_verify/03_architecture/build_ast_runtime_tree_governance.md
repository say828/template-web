# build ast runtime tree governance

## Verification Target

- `templates` AST-style build/runtime-tree governance

## Gate Commands

- `python3 scripts/dev/audit_sdd_build_ast.py --write .agent/sdd-build-ast-audit.json`
- `rg -n "Ralph|iteration|Current Build Note|2026-" sdd/03_build -g '*.md'`

## Latest Known Status

- status: pass
- primary command: `python3 scripts/dev/audit_sdd_build_ast.py --write .agent/sdd-build-ast-audit.json`
- machine-readable result: `.agent/sdd-build-ast-audit.json`
- scores: `ast_similarity=10`, `implementation_traceability=10`, `human_agent_readability=10`
- finding summary: residual finding 없음, `all_ten=true`
- supporting check: `rg -n "Ralph|iteration|Current Build Note|2026-" sdd/03_build -g '*.md'` returned no matches
- supporting infra checks:
  - `terraform -chdir=infra/terraform/aws/data init -backend=false && terraform -chdir=infra/terraform/aws/data validate`
  - `terraform -chdir=infra/terraform/aws/domain init -backend=false && terraform -chdir=infra/terraform/aws/domain validate`
  - `terraform -chdir=infra/terraform/openstack/server init -backend=false && terraform -chdir=infra/terraform/openstack/server validate`

## Residual Risk

- runtime entrypoint나 shell structure가 바뀌면 service summary와 audit needle을 함께 갱신하지 않으면 AST 점수가 어긋난다.
- downstream repo가 template를 복제한 뒤 role agent나 skill alias만 가져가고 policy를 생략하면 build current-state 규칙이 약해질 수 있다.
