# architecture document governance

## Covered Planning Artifacts

- `sdd/02_plan/03_architecture/architecture_document_governance.md`

## Implemented Scope

- `03_architecture` planning root를 공통 아키텍처와 특화 아키텍처를 함께 담는 구조로 정리했다.
- architecture planning이 `frontend`, `backend`, `infra`, `tech-research` split을 사용할 수 있게 맞췄다.
- 데이터 모델링은 `04_data` 경계로 분리된다는 점을 planning 문서에 반영했다.

## Implementation Shape

- 공통 구조 문서 [`architecture_document_structure.md`](../../01_planning/03_architecture/architecture_document_structure.md)에서 architecture 범위와 문서 구조를 고정했다.
- `frontend/`, `backend/`, `infra/`, `tech-research/` 하위 README를 추가해 특화 문서의 canonical 위치를 만들었다.
- `04_data` README/INDEX는 데이터 모델링 planning root라는 경계를 설명하도록 맞췄다.

## Key Modules And Contracts

- [`sdd/01_planning/03_architecture/README.md`](../../01_planning/03_architecture/README.md)
- [`sdd/01_planning/03_architecture/INDEX.md`](../../01_planning/03_architecture/INDEX.md)
- [`sdd/01_planning/03_architecture/architecture_document_structure.md`](../../01_planning/03_architecture/architecture_document_structure.md)
- [`sdd/01_planning/04_data/README.md`](../../01_planning/04_data/README.md)
- [`sdd/02_plan/03_architecture/architecture_document_governance.md`](../../02_plan/03_architecture/architecture_document_governance.md)

## Current Behavior

- architecture planning은 root common docs와 specialized subfolders를 함께 갖는 구조로 정리돼 있다.
- 데이터 모델링은 architecture 문서가 아니라 `04_data` planning root에서 다루도록 경계가 고정됐다.
