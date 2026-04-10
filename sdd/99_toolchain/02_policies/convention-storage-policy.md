# Convention Storage Policy

## Purpose

저장소 전반에서 반복 참조되는 컨벤션, 워크플로우, 실행 규약의 정본 위치를 고정한다.

## Rules

- 공통 컨벤션의 정본은 항상 `sdd/99_toolchain/02_policies`에 저장한다.
- `AGENTS.md`에는 실행 시 반드시 기억해야 할 짧은 핵심 규칙만 둔다.
- `sdd/`는 history 저장소가 아니라 overwrite-only current-state delivery system으로 유지한다.
- `sdd/02_plan`의 active planning은 `01_feature`, `02_screen`, `03_architecture`, `06_iac`, `10_test` 기준 durable 문서를 직접 갱신한다.
- feature 계획은 `<domain>_todos.md`, screen 계획은 `<service>_todos.md` 파일을 single source of truth로 사용한다.
- 컨벤션 관련 변경은 다음 순서를 따른다.
  1. `sdd/99_toolchain/02_policies` 문서를 먼저 수정한다.
  2. 필요한 경우에만 `AGENTS.md`, 런북, 템플릿, 자동화 문서를 최소 범위로 동기화한다.
- 저장소 루트 하네스(`.codex`, `.claude`)는 toolchain 정책을 구현하는 자산으로 취급한다.
- 하네스 사용법, 자동화 진입점, 템플릿화 가능한 예시는 `sdd/99_toolchain/01_automation`에 정리한다.
- Playwright suite registry와 canonical runner도 `sdd/99_toolchain/01_automation`이 소유한다.

## Canonical References

- 워크플로우/배포 규칙: `main-push-before-dev-deploy-policy.md`
- compose/runtime 기준선: `compose-runtime-baseline-policy.md`
- 회귀 검수 규칙: `regression-verification-policy.md`
- 하네스 설명: `../01_automation/harness-layout.md`
