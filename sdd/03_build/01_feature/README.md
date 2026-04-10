# Feature Build Summary Rule

## Canonical Rule

- feature 구현 결과는 overwrite-only durable build summary 파일로 관리한다.
- planning feature spec이 서비스 legacy 축과 domain canonical 축을 함께 가질 수 있으므로, build summary는 `service/`와 `domain/`의 큰 범주로 묶어 관리한다.
- 새 작업이 생겨도 같은 범주의 구현 설명은 같은 파일을 갱신한다.

## Location

- service-facing summary: `sdd/03_build/01_feature/service/`
- domain-facing summary: `sdd/03_build/01_feature/domain/`

## Recommended Sections

- covered planning artifacts
- implemented scope
- implementation shape
- key modules and contracts
- current runtime or UX behavior
