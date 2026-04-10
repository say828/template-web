# Automation Toolchain

`01_automation`은 screen spec 생성, capture asset 수집, parity harness 실행, Playwright exactness orchestration, recipe 기반 정적 자산 생성을 위한 자동화 자산을 둔다.

## Scope

- screen spec capture script
- screen spec PDF generator
- parity harness
- Playwright exactness runner / suite registry
- generator manifest
- asset recipe builder
- regression verification scope selection rule

## Screen Spec Rule

- feature code: `DOMAIN-FNNN`
- screen code: `SERVICE-SNNN`
- desktop capture 기준 visible area: `1710x951`
- 기본 capture viewport: `1690x940`
- capture mode: `viewport-first`

## Canonical Tools

- [screen_spec_manifest.py](./screen_spec_manifest.py)
- [capture_screen_assets.mjs](./capture_screen_assets.mjs)
- [build_screen_spec_pdf.py](./build_screen_spec_pdf.py)
- [spec_asset_builder.py](./spec_asset_builder.py)
- [build_asset_recipes.py](./build_asset_recipes.py)
- [playwright_exactness_manifest.py](./playwright_exactness_manifest.py)
- [run_playwright_exactness.py](./run_playwright_exactness.py)

## Storage Rule

- generated runtime asset은 각 구현 repo 경로에 둔다.
- planning 산출물은 `sdd/01_planning/02_screen/assets/` 아래에 둔다.
- generator와 manifest는 `sdd/99_toolchain/01_automation/`에 둔다.
- Playwright harness source는 repo 상황에 따라 `research/agent-browser/pocs/playwright-dev-e2e/` 같은 runtime location에 둘 수 있지만, canonical invocation과 suite registry는 `sdd/99_toolchain/01_automation/`이 소유한다.

## Regression Verification Rule

- toolchain은 builder/harness를 제공하더라도 direct target만 확인하고 종료하는 흐름을 허용하지 않는다.
- `sdd` 작업은 `sdd/02_plan/10_test/regression_verification.md`를 기준으로 direct, upstream, downstream, shared surface를 선택한다.
- parity harness나 build check는 회귀 검수의 일부일 뿐이고, 실제 완료 기준은 선택한 regression surface 전체에 대한 retained evidence다.
- Playwright exactness suite가 있는 surface는 `run_playwright_exactness.py`를 canonical local gate로 사용한다.
- shared route, shell, auth/session, shared component, API/data contract, generated asset, builder output 변경은 adjacent consumer까지 검수 범위를 넓힌다.
- 아직 자동화가 없는 회귀 surface는 command/manual verification으로 메우고, automation gap은 `sdd/03_build`, `sdd/03_verify`에 residual risk로 남긴다.
- Browser Use나 수동 시각 점검은 Playwright exactness gate를 대체하지 않고 보강/진단 용도로만 사용한다.

## Asset Recipe Rule

- 정적 디자인 자산 추출의 canonical tool name은 `스펙에셋빌더`다.
- generic 실행 파일은 `[spec_asset_builder.py](./spec_asset_builder.py)`다.
- `[build_asset_recipes.py](./build_asset_recipes.py)`는 기존 호출 호환용 wrapper다.
- 화면명세서에 있는 icon, logo, illustration, 기타 재사용 가능한 static asset은 먼저 `스펙에셋빌더`로 추출한 뒤 구현 코드에서 사용한다.
- reusable asset planning 문서는 `sdd/01_planning/02_screen/assets/` 아래에 둔다.
- 프로젝트별 규칙은 Python manifest에서 `ASSET_RECIPES` 리스트로 선언한다.
- 각 recipe는 `source`, `crop_box`, `transparent_white_threshold`, `trim`, `output`, `children`을 조합해 재사용 가능한 SVG/PNG 자산을 생성한다.
- `--verify-exact`를 사용하면 generated output이 source crop과 픽셀 단위로 동일한지 검증한다.
- builder로 표현 가능한 자산을 수동 redraw나 screenshot crop으로 대체하지 않는다.
- 수동 예외가 필요하면 plan/build/verify 문서에 source, 예외 사유, 최종 자산 경로를 함께 남긴다.
- 예시 manifest는 [`../03_templates/asset_recipe_manifest.example.py`](../03_templates/asset_recipe_manifest.example.py)에 둔다.
- 예시 generated output은 [`../03_templates/generated_assets/README.md`](../03_templates/generated_assets/README.md) 경로를 사용한다.

## Playwright Exactness Rule

- Playwright exactness의 canonical registry는 [playwright_exactness_manifest.py](./playwright_exactness_manifest.py)다.
- canonical runner는 [run_playwright_exactness.py](./run_playwright_exactness.py)다.
- downstream repo는 suite source를 runtime location에 둘 수 있지만, retained command는 wrapper 기준으로 남긴다.
- suite id, spec file, target screen batch, artifact path는 durable current-state로 관리한다.
- screen 작업의 기본 local exactness gate는 다음 순서를 따른다.
  - design guide / asset / screen spec baseline 확인
  - `python3 sdd/99_toolchain/01_automation/run_playwright_exactness.py --suite <suite-id> --base-url <url>`
  - 필요하면 `--api-base-url`, `--browser`, `--grep`를 추가한다.
  - 실행 결과와 artifact path를 `sdd/03_verify` current summary에 기록한다.
- 시작점 예시는 [`../03_templates/playwright_exactness_manifest.example.py`](../03_templates/playwright_exactness_manifest.example.py)를 따른다.
