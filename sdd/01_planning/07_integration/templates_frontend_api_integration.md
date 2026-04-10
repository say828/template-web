# templates frontend api integration

- 작성 버전: 1.0.0

## Purpose

현재 frontend와 backend의 실제 연결 지점을 정리한다.

## 1. Shared Integration Rule

- 네 개의 frontend 모두 공통 `auth` contract를 사용한다.
- `POST /api/v1/auth/login`으로 access token을 발급받고 로컬 storage에 저장한다.
- `GET /api/v1/auth/me`로 초기 세션을 복원한다.

## 2. Service Coupling Summary

| Service | Real Backend Coupling | Note |
| --- | --- | --- |
| web | `auth`, `orders` | dashboard overview와 orders table을 live contract에 연결 |
| admin | `auth`, `orders`, `alerts`, `support` | overview/queue/support surface와 alerts drawer를 live contract에 연결 |
| mobile | `auth`, `fulfillment`, `shipping` | dashboard overview와 fulfillment/shipping surface를 live contract에 연결 |
| landing | `auth`, `catalog` | home/workspace에서 catalog products를 읽어 public/protected surface를 구성 |

## 3. Coupling Detail

- web
  - bearer session은 기존 `AuthProvider`가 유지한다.
  - page load 시 `orders/overview`, `orders`를 fetch하고 search는 client-side filter로 처리한다.
- admin
  - protected route는 그대로 유지한다.
  - dashboard는 `orders/admin/overview`와 `alerts`를 병렬 fetch한다.
  - queue, support, alerts drawer는 개별 page-level effect로 fetch한다.
- mobile
  - overview와 board payload는 mobile shell 진입 후 fetch한다.
  - status/tone badge는 response의 string field를 frontend palette에 매핑한다.
  - board route는 `/fulfillment`다.
  - shipping route는 `/shipping`이고 shipment status feed를 별도 fetch한다.
- landing
  - public home에서도 `catalog/products`를 읽어 live catalog proof를 보여준다.
  - protected workspace는 auth user summary와 catalog product grid를 함께 노출한다.

## 4. Known Gaps

- web/admin은 아직 catalog/inventory command surface를 직접 소비하지 않는다.
- order 생성, fulfillment 전이, shipping 전이, support create/update, alerts read는 backend contract로 존재하지만 frontend action UI는 baseline 최소 액션 중심이다.
- landing은 catalog read를 public/protected दोनों surface에 재사용하지만 category/detail 분해까지는 아직 없다.
