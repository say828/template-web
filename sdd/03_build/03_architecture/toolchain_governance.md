# toolchain governance

## Covered Planning Artifact

- `sdd/02_plan/03_architecture/toolchain_governance.md`

## Implemented Scope

- toolchain policy 정본에 regression verification rule을 추가했다.
- Playwright exactness runner/manifest를 local screen exactness의 canonical toolchain entrypoint로 추가했다.
- `AGENTS.md`, `.codex/skills/sdd/SKILL.md`, `sdd/99_toolchain/01_automation/README.md`가 같은 회귀 검수 기준을 공유한다.
- reusable asset planning root를 `sdd/01_planning/02_screen/assets/`로 정리하고, local Codex/Claude `sdd` skill에 같은 path를 반영했다.
- `sdd/02_plan/10_test`, `sdd/03_build/10_test`, `sdd/03_verify/10_test`에 regression verification current-state 문서를 추가했다.
- `.claude/skills/sdd-dev/SKILL.md`의 stale Codex canonical path를 현재 `.codex/skills/sdd/` 구조로 교체했다.
- `.codex/skills/sdd/SKILL.md`와 `.claude/skills/sdd-dev/SKILL.md`에서 DEV/PROD rollout gate를 explicit deployment scope 조건으로 제한했다.
- 디자인 가이드 builder 안내는 고정 file path 대신 `sdd/99_toolchain/01_automation/README.md`와 실제 존재하는 builder inventory 기준으로 정리했다.
- 프로젝트 루트에 `SDD_SKILL.md`를 추가해 `sdd` skill의 용도, canonical path, 핵심 guardrail을 한 파일에서 요약했다.
- `SDD_SKILL.md`를 확장해 workflow 단계, `sdd/` folder structure, feature/screen/architecture/data/test/operate flow 설명을 명시적으로 정리했다.
- `SDD_SKILL.md`를 추가 확장해 toolchain, visual fidelity, exactness, functional alignment를 builder/harness/contract 관점으로 설명했다.
- `SDD_SKILL.md`를 다시 확장해 trigger, non-use case, artifact governance, section routing, schema parity, regression verification, rollout, completion gate까지 포함하는 루트 해설서로 정리했다.
- ignored 상태였던 `.claude/settings.local.json`, `.agent/sdd-build-ast-audit.json`, `.agent/runs/README.md`를 template-tracked asset으로 승격했다.
- generated/cache 성격의 `node_modules`, `dist`, `.venv`, `.terraform`, runtime run output은 ignore 유지 대상으로 명시했다.

## Implementation Shape

- 정책 정본은 `sdd/99_toolchain/02_policies/regression-verification-policy.md`에 둔다.
- 실행 요약은 `AGENTS.md`, skill rule은 `.codex/skills/sdd/SKILL.md`와 `.claude/skills/sdd/SKILL.md`, toolchain entry는 `sdd/99_toolchain/01_automation/README.md`가 담당한다.
- Playwright suite registry는 `playwright_exactness_manifest.py`, canonical runner는 `run_playwright_exactness.py`가 담당한다.
- 회귀 검수는 direct/upstream/downstream/shared surface selection을 retained SDD workflow로 유지한다.
- local Claude alias는 현재 Codex canonical skill path를 stale alias path 없이 직접 가리킨다.
- rollout은 `sdd/05_operate` 존재만으로 자동 요구되지 않고, explicit deployment scope 또는 저장소 completion policy가 있을 때만 gate가 열린다.
- 루트 entrypoint 문서는 입문 설명을 담당하고, canonical 판단 기준은 local skill 원문과 toolchain policy가 담당한다.
- 루트 entrypoint 문서는 visual proof와 functional proof를 분리해서 설명하고, 둘 다 retained evidence가 필요하다는 점을 명시한다.
- 루트 entrypoint 문서는 skill 전체 mental model을 설명하고, 실제 강제 rule은 canonical skill/policy 문서가 담당한다.
- local-only scaffold 중 downstream repo가 그대로 재사용해야 하는 파일은 ignore 예외로 승격하고, generated artifact는 계속 배제한다.
- screen template는 suite id, canonical runner command, artifact path를 기본 항목으로 요구한다.
