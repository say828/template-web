# Screen TODO Rule

## Common Rule

- 이 폴더는 `sdd/02_plan` 아래에서 에이전트의 현재 개발 계획을 관리한다.
- 다른 `02_plan` 폴더와 동일하게 `README.md + durable TODO 파일`만 유지하고, dated plan history는 두지 않는다.
- 개발계가 있는 화면 작업은 `구현 -> build -> DEV(개발계) 배포 -> DEV 검수 -> 같은 TODO 파일 갱신`을 기본 루틴으로 둔다.

## Canonical Rule

- 화면 계획은 service별 durable TODO 파일로 관리한다.
- `01_feature`와 동일하게 날짜별 작업 문서를 계속 추가하지 않는다.
- 같은 service 파일 안에서 화면코드 기준으로 계속 갱신한다.
- mobile source key인 `APP_###`는 파일명이 아니라 문서 내부 field로만 기록한다.
- 과거 screen plan 문서는 별도 보관하지 않고, 현재 기준 README와 service TODO만 유지한다.

## Location

- 서비스별 화면 TODO는 `sdd/02_plan/02_screen/` root에 둔다.
- 예:
  - `sdd/02_plan/02_screen/mobile_todos.md`
  - `sdd/02_plan/02_screen/web_todos.md`

## Naming

- 파일명은 날짜 prefix를 쓰지 않는다.
- 권장 형식: `{service}_todos.md`

## Minimum Sections

- service summary
- shared constraints or baseline
- screen items
- delivery phases or backlog
- latest verification references

## Template

- [`_screen_todo_template.md`](_screen_todo_template.md)
