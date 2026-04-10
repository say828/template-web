# service verification

## Scope

- web, admin, mobile, landing 서비스 surface의 현재 retained verification을 요약한다.

## Current Status

- `web`: pass
- `admin`: pass
- `mobile`: pass
- `landing`: pass

## Retained Checks

- service별 frontend build가 current baseline 검증 surface다.
- typed API contract와 backend domain contract 정합성은 domain verification을 상속한다.
- screen surface 상세는 `03_verify/02_screen/` 기준으로 읽는다.

## Residual Risk

- 실제 서비스 repo에 적용할 때는 각 app별 targeted build와 proof를 다시 재실행해야 한다.
