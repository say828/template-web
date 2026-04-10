# Regression Verification Policy

## Purpose

템플릿 저장소에서도 회귀 검수 범위를 direct target에 한정하지 않고, retained current-state workflow로 고정한다.

## Rules

- `sdd` 작업은 direct target verification만으로 완료 처리하지 않는다.
- 회귀 검수 범위는 `sdd/02_plan/10_test/regression_verification.md`를 기준으로 direct, upstream, downstream, shared surface까지 선택한다.
- shared route, shell, auth/session, component, contract, generated asset, builder output을 변경한 경우 adjacent consumer와 shared surface를 함께 검수한다.
- Playwright exactness suite가 있는 screen/local UI surface는 `sdd/99_toolchain/01_automation/run_playwright_exactness.py`를 canonical local gate로 사용한다.
- direct `npx playwright test ...` 호출은 디버깅 예외로만 쓰고, retained verification command는 toolchain wrapper 기준으로 남긴다.
- 자동화가 없는 회귀 surface는 가능한 command/manual verification으로 대체하고, automation gap은 residual risk로 남긴다.
- 선택한 회귀 검수 범위, 실행한 check, 생략 사유, residual risk는 `sdd/02_plan`, `sdd/03_build`, `sdd/03_verify`에 current-state로 유지한다.

## Canonical References

- `AGENTS.md`
- `.codex/skills/sdd/SKILL.md`
- `sdd/99_toolchain/01_automation/README.md`
- `sdd/02_plan/10_test/regression_verification.md`
