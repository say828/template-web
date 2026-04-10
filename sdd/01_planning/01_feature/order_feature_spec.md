# order feature spec

- 작성 버전: 1.1.0

## 1. Purpose

`orders` bounded context가 제공하는 web 주문 현황과 관리자 운영 큐 기능을 구현 기준으로 정리한다.

## 2. Scope

- 포함 범위:
  - web 주문 overview/list read model과 주문 생성, 상태 전이 command
  - admin 주문 overview/queue read model
- 제외 범위:
  - 외부 결제 게이트웨이 정산이나 배송사 연동
  - 비동기 이벤트 버스 기반 후속 orchestration

## 3. Actor Summary

| Actor | Description | Appears In |
| --- | --- | --- |
| `Web User` | web 서비스에서 주문 현황을 조회하고 신규 주문 생성이나 주문 상태 갱신을 수행하는 운영 사용자다. | `ORD-F001`, `ORD-F002`, `ORD-F003`, `ORD-F004` |
| `Admin Operator` | admin 서비스에서 주문 KPI와 운영 큐를 모니터링하는 관리자다. | `ORD-F005`, `ORD-F006` |

## 4. Bounded Context Summary

| Item | Value |
| --- | --- |
| Domain Code | `ORD` |
| Bounded Context | Order Operations |
| Primary Backend Owner | `server/contexts/orders` |
| Related Context | `auth`, `catalog`, `fulfillment` |
| Main Entry Contract | `GET /api/v1/orders/overview`, `GET /api/v1/orders`, `POST /api/v1/orders`, `PATCH /api/v1/orders/{order_id}/status`, `GET /api/v1/orders/admin/overview`, `GET /api/v1/orders/admin/queue` |

## 5. Aggregate / Model Snapshot

| Aggregate / Model | Role |
| --- | --- |
| `OrderRecord` | bootstrap 기반 주문 원본 |
| `OrderOverview` | web dashboard 요약 읽기 모델 |
| `OrderSummary` | web orders 목록 읽기 모델 |
| `CreateOrderCommand` | 주문 생성 명령 |
| `UpdateOrderStatusCommand` | 주문 상태 전이 명령 |
| `OrderStatusTransition` | 주문 상태 전이 결과 |
| `AdminOrderOverview` | 관리자 운영 요약 읽기 모델 |
| `AdminQueueItem` | 관리자 거래 큐 읽기 모델 |

## 6. Use Case Matrix

| Feature Code | Use Case | Actor | Bounded Context | Aggregate / Model | Type | Preconditions | Domain Outcome | Invariant / Business Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ORD-F001` | web 주문 overview를 조회한다 | Web User | Order Operations | `OrderOverview`, `OrderRecord` | Query | 인증 토큰이 유효하고 주문 bootstrap 데이터가 존재해야 한다 | 주문 카드, 최근 활동, 선택 주문 상세를 함께 반환한다 | overview는 최근 활동 3건과 선택 주문 1건을 항상 포함한다 |
| `ORD-F002` | web 주문 목록을 조회한다 | Web User | Order Operations | `OrderSummary`, `OrderRecord` | Query | 인증 토큰이 유효하고 주문 bootstrap 데이터가 존재해야 한다 | 주문 목록을 반환한다 | 목록 행은 `id`, `product_name`, `customer_name`, `status`를 유지한다 |
| `ORD-F003` | 신규 주문을 생성한다 | Web User | Order Operations | `CreateOrderCommand`, `OrderRecord` | Command | 인증 토큰이 유효하고 제품, 고객, 판매자, 금액 정보가 전달되어야 한다 | 새 `OrderRecord`가 생성되어 목록과 overview에 반영된다 | 새 주문은 문자열 ID를 부여받고 `Pending`과 `Queued`를 기본 상태로 사용한다 |
| `ORD-F004` | 주문의 결제/이행 상태를 변경한다 | Web User | Order Operations | `UpdateOrderStatusCommand`, `OrderStatusTransition`, `OrderRecord` | Command | 인증 토큰이 유효하고 요청한 `order_id`가 존재해야 한다 | 주문의 `status`, `fulfillment_status`, `stage`가 변경된다 | 존재하지 않는 `order_id`면 `404`를 반환한다 |
| `ORD-F005` | 관리자용 주문 overview를 조회한다 | Admin Operator | Order Operations | `AdminOrderOverview`, `OrderRecord` | Query | 관리자 토큰이 유효하고 주문 bootstrap 데이터가 존재해야 한다 | 관리자 KPI와 stage 현황을 반환한다 | admin surface는 web surface와 다른 운영형 read model을 사용한다 |
| `ORD-F006` | 관리자용 거래 큐를 조회한다 | Admin Operator | Order Operations | `AdminQueueItem`, `OrderRecord` | Query | 관리자 토큰이 유효하고 주문 bootstrap 데이터가 존재해야 한다 | 주문별 운영 큐 행을 반환한다 | 큐 행은 `order_id`, `product_name`, `customer_name`, `status`, `sla`를 유지한다 |

## 7. Notes

- `orders`는 web surface와 admin surface에 서로 다른 read model을 제공한다.
- 운영 알람 feed는 별도 `alerts` context가 소유하고, `orders`는 주문 자체 read/write 모델만 유지한다.
- template baseline의 주문 상태 전이는 내부 mutation semantics까지만 다루며 외부 결제/이벤트 연동은 포함하지 않는다.
