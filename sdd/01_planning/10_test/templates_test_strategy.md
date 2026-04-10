# templates test strategy

- 작성 버전: 1.0.0

## Purpose

template baseline을 유지하기 위한 테스트 전략을 정의한다.

## 1. Backend

- `server/tests/e2e/test_domain_feature_flows.py`
  - `AUT-F001`
  - `AUT-F002`
  - `USR-F001`
  - `USR-F002`
  - `USR-F003`
  - `CAT-F001`
  - `CAT-F003`
  - `CAT-F004`
  - `CAT-F005`
  - `INV-F001`
  - `INV-F002`
  - `INV-F003`
  - `INV-F004`
  - `INV-F005`
  - `INV-F006`
  - `ORD-F001`
  - `ORD-F002`
  - `ORD-F003`
  - `ORD-F004`
  - `ORD-F005`
  - `ORD-F006`
  - `SHP-F001`
  - `SHP-F002`
  - `SHP-F003`
  - `ALR-F001`
  - `ALR-F002`
  - `ALR-F003`
  - `SUP-F001`
  - `SUP-F002`
  - `SUP-F003`
  - `FUL-F001`
  - `FUL-F002`
  - `FUL-F003`
- `server/tests/test_health.py`
  - `HLT-F001`
  - `HLT-F002`
  - auth/user smoke

## 2. Frontend

- `web`, `admin`, `mobile`, `landing`는 각 서비스별 production build를 통과해야 한다.
- screen spec은 `WEB-S001`, `ADM-S001`, `MOB-S001`, `LND-S001` 규칙으로 구현 route와 관련 feature를 함께 검증한다.
- parity harness가 활성화되면 route-gap과 proof artifact를 추가 검증한다.

## 3. CI Gate

- backend: `./.venv/bin/python -m pytest -q` 또는 CI 환경의 `uv run pytest -q`
- frontend: `pnpm build` matrix
- toolchain: `build_screen_spec_pdf.py`, `capture_screen_assets.mjs`, `new_plan.sh` shell validation
