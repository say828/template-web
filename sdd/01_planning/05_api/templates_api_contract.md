# templates server contract

- 작성 버전: 1.0.0

## Purpose

현재 server runtime이 제공하는 HTTP contract를 구현 기준으로 정리한다.

## 1. HTTP Endpoint Matrix

| Method | Path | Domain | Purpose | Response |
| --- | --- | --- | --- | --- |
| `GET` | `/health` | health | root health probe | `{"status":"ok"}` |
| `GET` | `/api/v1/status` | health | API health/status probe | `{"service":"template-server","status":"healthy"}` |
| `POST` | `/api/v1/auth/login` | auth | credential 로그인과 token 발급 | `AuthToken` |
| `GET` | `/api/v1/auth/me` | auth | bearer token 기반 현재 사용자 조회 | `AuthenticatedUser` |
| `GET` | `/api/v1/users` | user | 사용자 summary 목록 조회 | `list[UserSummary]` |
| `GET` | `/api/v1/users/{user_id}` | user | 단일 사용자 상세 조회 | `UserDetail` |
| `PATCH` | `/api/v1/users/{user_id}/status` | user | 사용자 상태 변경 | `UserDetail` |
| `GET` | `/api/v1/catalog/products` | catalog | 공개/운영 상품 목록 조회 | `list[ProductSummary]` |
| `GET` | `/api/v1/catalog/products/{product_id}` | catalog | 단일 상품 상세 조회 | `ProductDetail` |
| `POST` | `/api/v1/catalog/products` | catalog | 상품 생성 | `ProductDetail` |
| `PUT` | `/api/v1/catalog/products/{product_id}` | catalog | 상품 수정 | `ProductDetail` |
| `PATCH` | `/api/v1/catalog/products/{product_id}/status` | catalog | 상품 상태 변경 | `ProductDetail` |
| `GET` | `/api/v1/inventory/levels` | inventory | 재고 레벨 목록 조회 | `list[InventoryLevel]` |
| `GET` | `/api/v1/inventory/levels/{sku}/{location_id}` | inventory | 단일 재고 레벨 조회 | `InventoryLevel` |
| `POST` | `/api/v1/inventory/levels/{sku}/{location_id}/adjustments` | inventory | 재고 증감 조정 | `InventoryMutationReceipt` |
| `POST` | `/api/v1/inventory/levels/{sku}/{location_id}/reservations` | inventory | 재고 선점 | `InventoryMutationReceipt` |
| `POST` | `/api/v1/inventory/levels/{sku}/{location_id}/releases` | inventory | 재고 선점 해제 | `InventoryMutationReceipt` |
| `PUT` | `/api/v1/inventory/levels/{sku}/{location_id}` | inventory | 재고 절대값 재설정 | `InventoryMutationReceipt` |
| `GET` | `/api/v1/orders/overview` | orders | web dashboard overview 조회 | `OrderOverview` |
| `GET` | `/api/v1/orders` | orders | web order table row 조회 | `list[OrderSummary]` |
| `POST` | `/api/v1/orders` | orders | 주문 생성 | `OrderRecord` |
| `PATCH` | `/api/v1/orders/{order_id}/status` | orders | 주문 상태 전이 | `OrderStatusTransition` |
| `GET` | `/api/v1/orders/admin/overview` | orders | admin dashboard 운영 overview 조회 | `AdminOrderOverview` |
| `GET` | `/api/v1/orders/admin/queue` | orders | admin queue table row 조회 | `list[AdminQueueItem]` |
| `GET` | `/api/v1/shipping/overview` | shipping | mobile 배송 overview 조회 | `ShippingOverview` |
| `GET` | `/api/v1/shipping/shipments` | shipping | shipment 목록 조회 | `list[ShipmentSummary]` |
| `PATCH` | `/api/v1/shipping/shipments/{shipment_id}/status` | shipping | 배송 상태 전이 | `ShipmentStatusTransition` |
| `GET` | `/api/v1/alerts` | alerts | admin 운영 알람 feed 조회 | `AlertsPayload` |
| `POST` | `/api/v1/alerts/{alert_id}/read` | alerts | 운영 알람 1건 읽음 처리 | `AlertReadResult` |
| `POST` | `/api/v1/alerts/read-all` | alerts | 운영 알람 전체 읽음 처리 | `AlertsReadAllResult` |
| `GET` | `/api/v1/support/faqs` | support | admin FAQ 목록 조회 | `list[SupportFaq]` |
| `POST` | `/api/v1/support/faqs` | support | FAQ 생성 | `SupportFaqRecord` |
| `PATCH` | `/api/v1/support/faqs/{faq_id}/visibility` | support | FAQ visibility 변경 | `SupportFaqRecord` |
| `GET` | `/api/v1/fulfillment/overview` | fulfillment | mobile dashboard 운영 overview 조회 | `FulfillmentOverview` |
| `GET` | `/api/v1/fulfillment/board` | fulfillment | mobile fulfillment board 조회 | `FulfillmentBoardPayload` |
| `PATCH` | `/api/v1/fulfillment/tasks/{task_id}/status` | fulfillment | fulfillment task 상태 전이 | `FulfillmentTaskStatusTransition` |

## 2. Auth Contract

- 인증 방식: `Authorization: Bearer <token>`
- login 입력: `email`, `password`
- login 성공 시 `access_token`, `token_type`, `user_id` 반환
- `auth/me`는 유효 token subject를 `AuthenticatedUser`로 해석
- `users`, `catalog` command, `inventory`, `orders`, `shipping`, `alerts`, `support`, `fulfillment`는 보호된 contract다

## 3. Error Baseline

- invalid credential: `401 Invalid credentials`
- invalid token: `401 Invalid token`
- forbidden role: `403 Forbidden`
- missing resource:
  - HTTP: `404 ... not found`
- conflict:
  - duplicate catalog slug: `409 Catalog product slug already exists`
  - invalid inventory mutation: `409 ...`

## 4. Frontend Binding Notes

- `client/web`
  - `/`는 `GET /api/v1/orders/overview`를 소비한다.
  - `/orders`는 `GET /api/v1/orders`를 소비한다.
- `client/admin`
  - `/`는 `GET /api/v1/orders/admin/overview`를 소비한다.
  - admin shell과 dashboard는 `GET /api/v1/alerts`를 운영 알람 source로 사용한다.
  - `/queue`는 `GET /api/v1/orders/admin/queue`를 소비한다.
  - `/support`는 `GET /api/v1/support/faqs`를 소비한다.
- `client/mobile`
  - `/`는 `GET /api/v1/fulfillment/overview`를 소비한다.
  - `/fulfillment`는 `GET /api/v1/fulfillment/board`를 소비한다.
  - `/shipping`은 `GET /api/v1/shipping/overview`, `GET /api/v1/shipping/shipments`를 소비한다.
- `client/landing`
  - `/`와 `/workspace`는 `GET /api/v1/catalog/products`를 live catalog surface로 사용한다.
- auth flow는 네 app 모두 `POST /api/v1/auth/login`과 `GET /api/v1/auth/me`를 유지한다.

## 5. Stack Notes

- HTTP: `FastAPI 0.116.x + Uvicorn 0.35.x`
- Compose runtime: `server`
