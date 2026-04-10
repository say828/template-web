# Planning Index

- [01_feature/INDEX.md](./01_feature/INDEX.md)
- [02_screen/INDEX.md](./02_screen/INDEX.md)
- [03_architecture/INDEX.md](./03_architecture/INDEX.md)
- [04_data/INDEX.md](./04_data/INDEX.md)
- [05_api/README.md](./05_api/README.md)
- [06_iac/README.md](./06_iac/README.md)
- [07_integration/README.md](./07_integration/README.md)
- [08_nonfunctional/README.md](./08_nonfunctional/README.md)
- [09_security/README.md](./09_security/README.md)
- [10_test/README.md](./10_test/README.md)

## Structure Rule

- `01_feature`, `02_screen`는 실제 서비스 표면(`web`, `mobile`, `admin`, `landing`) 기준으로 유지한다.
- `03_architecture` 이후는 서비스별 실산출물이 없으면 common-first로 유지한다.
- `03_architecture`는 공통 문서를 먼저 두고 필요 시 `frontend/`, `backend/`, `infra/`, `tech-research/`로 세분화한다.
- 데이터 모델링은 `04_data`에서 다루고 architecture 문서에는 중복 기록하지 않는다.
