# regression verification

## Covered Planning Artifact

- `sdd/02_plan/10_test/regression_verification.md`

## Implemented Scope

- regression verification을 direct/upstream/downstream/shared surface selection 기준으로 템플릿 workflow에 반영했다.
- selected regression surface는 `AGENTS.md`, skill, toolchain, test planning 문서와 연결된다.
- automation gap은 scope 축소가 아니라 residual risk 문서화 대상으로 유지한다.

## Implementation Shape

- direct target-only verification 금지 rule을 policy, skill, toolchain entrypoint에 공통 반영했다.
- test harness 문서는 regression surface selection을 대체하지 않고, 선택된 surface를 검증하는 실행 수단으로 정리했다.
