# regression verification

## Status

- pass

## Retained Checks

- `sdd/02_plan/10_test/regression_verification.md`가 current regression scope baseline으로 추가됐다.
- `AGENTS.md`, `.codex/skills/sdd/SKILL.md`, `sdd/99_toolchain/01_automation/README.md`가 direct-only verification 금지와 selected regression surface 기록 규칙을 함께 유지한다.
- `sdd/03_build/10_test/regression_verification.md`가 template workflow 반영 상태를 current-state로 설명한다.
- screen exact automation gate가 Playwright인 경우 suite id, toolchain runner command, artifact path를 retained check에 함께 남긴다.

## Residual Risk

- regression scope selection은 아직 자동 selector가 없어서 문서 규칙과 reviewer 판단에 의존한다.
