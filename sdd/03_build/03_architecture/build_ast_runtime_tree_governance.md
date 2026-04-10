# build ast runtime tree governance

## Covered Planning Artifact

- `sdd/02_plan/03_architecture/build_ast_runtime_tree_governance.md`

## Implemented Scope

- `scripts/dev/audit_sdd_build_ast.py`가 템플릿 `sdd/03_build` current-state를 AST-style runtime tree 기준으로 점수화한다.
- service build summary는 `main.tsx -> AuthProvider -> BrowserRouter -> App -> ProtectedRoute/shell -> route leaf -> backend contract leaf` 순서로 다시 정렬했다.
- `.agent`, `.claude/agents`, `.claude/skills/sdd*`, `.codex/skills/SKILL.md`, `.codex/skills/sdd`를 canonical agentic surface로 추가했다.
- infra baseline은 `aws/data`, `aws/domain`, `openstack/server` provider-first split을 기준으로 문서와 Terraform skeleton을 유지한다.

## Key Modules And Contracts

- `scripts/dev/audit_sdd_build_ast.py`
- `.agent/ralph.sh`
- `.agent/ralph-supervisor.sh`
- `.claude/agents/`
- `.claude/skills/sdd/SKILL.md`
- `.claude/skills/sdd-development/SKILL.md`
- `.codex/skills/SKILL.md`
- `.codex/skills/sdd/SKILL.md`
- `infra/terraform/README.md`
