# Build Governance

## Purpose

- `sdd/03_build/`는 실제 구현 결과를 사람이 빠르게 읽을 수 있게 정리하는 루트다.
- `02_plan`이 무엇을 할지 관리한다면, `03_build`는 무엇으로 어떻게 구현했는지를 정리한다.

## Canonical Rule

- `sdd/03_build/`의 durable section은 `sdd/02_plan/`의 top-level 구조를 그대로 따른다.
- feature 구현 요약은 `sdd/03_build/01_feature/` 아래 service 또는 domain 단위의 큰 범주 build summary로 유지한다.
- screen 구현 요약은 `sdd/03_build/02_screen/<service>/` 아래 screen별 durable build summary로 유지한다.
- architecture, delivery, validation harness처럼 장기 유지가 필요한 요약은 대응되는 section 번호 아래에 둔다.
- build summary는 TODO보다 상세해야 하며, 최소한 다음을 포함한다:
  - 어떤 planning 산출물을 현재 문서가 흡수하는지
  - 구현된 범위
  - 실제 사용한 모듈/컴포넌트/자산/계약
  - 현재 구현 형태 요약
  - 현재 사용자/운영자 관점에서 보이는 동작
- build summary 본문은 현재 구현 상태만 설명하고, 일시적 작업 순서나 시행착오는 SDD에 별도 누적하지 않는다.

## Overwrite Rule

- `sdd/03_build`는 dated execution history를 보관하지 않는다.
- 같은 feature, screen, architecture, delivery 영역의 후속 작업이 생기면 기존 build summary 파일을 덮어써서 최종 일관성만 유지한다.

## Sections

- `01_feature/`: 기능별 구현 요약
- `02_screen/`: 화면별 구현 요약
- `03_architecture/`: 저장해둘 가치가 있는 구조/거버넌스 구현 요약
- `06_iac/`: 배포/런타임 delivery 요약
- `07_integration/`: 연동 구현 요약
- `08_nonfunctional/`: 비기능 구현 요약
- `10_test/`: 반복 사용되는 검증 harness/validation surface 요약
