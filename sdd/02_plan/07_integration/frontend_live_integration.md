# frontend live integration

- Owner: Codex
- Status: active

## Scope

- In scope:
  - web/admin/mobile/landing과 backend domain contract 연결 기준
  - typed API helper와 current live wiring baseline

## Acceptance Criteria

- [x] frontend service split과 backend domain owner 매핑이 current baseline으로 정리된다.
- [x] integration 계획은 service별 live fetch wiring을 현재형으로 설명한다.

## Current Notes

- `web`은 catalog/orders/support 중심 operator surface를 사용한다.
- `admin`은 alerts, catalog, orders 관리 surface를 사용한다.
- `mobile`은 fulfillment, shipping 중심 surface를 사용한다.
- `landing`은 catalog/public read surface를 사용한다.
- `client/mobile/src/lib/useSpeechRecognitionInput.ts`를 template shared utility로 유지해, 화면/입력 컴포저의 browser speech-to-text affordance를 공통 모듈로 시작할 수 있게 한다.

## Validation

- current references:
  - `client/web/src`
  - `client/admin/src`
  - `client/mobile/src`
  - `client/landing/src`
