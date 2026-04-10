# Screen Build Summary Rule

## Canonical Rule

- screen 구현 결과는 screen별 overwrite-only durable build summary 파일로 관리한다.
- planning service split을 그대로 따라 `sdd/03_build/02_screen/<service>/` 아래에 둔다.
- screen summary는 현재 구현 상태만 설명하고, dated execution history를 별도 섹션으로 두지 않는다.

## Location

- 예:
  - `sdd/03_build/02_screen/mobile/MOB-S001_example.md`
  - `sdd/03_build/02_screen/web/WEB-S001_example.md`

## Recommended Sections

- covered planning artifact
- implemented scope
- implementation shape
- key modules/assets/contracts
- current user-visible behavior

## Template

- [`_screen_build_template.md`](_screen_build_template.md)
