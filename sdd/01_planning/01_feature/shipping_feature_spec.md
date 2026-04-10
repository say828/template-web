# shipping feature spec

- 작성 버전: 1.0.0

## 1. Purpose

`shipping` bounded context가 제공하는 배송 추적 overview와 shipment 상태 전이 기능을 구현 기준으로 정리한다.

## 2. Scope

- 포함 범위:
  - mobile/operator surface에서 배송 현황 overview와 shipment 목록 조회
  - shipment 상태 전이와 마지막 배송 이벤트 갱신
- 제외 범위:
  - 외부 택배사 webhook, 실시간 위치 추적, 고객 알림 발송
  - 결제 승인이나 재고 선점 같은 upstream orchestration

## 3. Actor Summary

| Actor | Description | Appears In |
| --- | --- | --- |
| `Mobile Operator` | mobile 서비스에서 출고 이후 배송 상태를 추적하고 shipment 진행 상태를 갱신하는 운영자다. | `SHP-F001`, `SHP-F002`, `SHP-F003` |

## 4. Bounded Context Summary

| Item | Value |
| --- | --- |
| Domain Code | `SHP` |
| Bounded Context | Shipping Operations |
| Primary Backend Owner | `server/contexts/shipping` |
| Related Context | `orders`, `fulfillment` |
| Main Entry Contract | `GET /api/v1/shipping/overview`, `GET /api/v1/shipping/shipments`, `PATCH /api/v1/shipping/shipments/{shipment_id}/status` |

## 5. Aggregate / Model Snapshot

| Aggregate / Model | Role |
| --- | --- |
| `ShipmentRecord` | 배송 원본 저장 모델 |
| `ShippingOverview` | 배송 overview 응답 모델 |
| `ShipmentSummary` | 배송 목록 응답 모델 |
| `UpdateShipmentStatusCommand` | 배송 상태 전이 명령 |
| `ShipmentStatusTransition` | 배송 상태 전이 결과 |

## 6. Use Case Matrix

| Feature Code | Use Case | Actor | Bounded Context | Aggregate / Model | Type | Preconditions | Domain Outcome | Invariant / Business Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SHP-F001` | 배송 overview를 조회한다 | Mobile Operator | Shipping Operations | `ShippingOverview`, `ShipmentRecord` | Query | 인증 토큰이 유효하고 shipment bootstrap 데이터가 존재해야 한다 | 배송 중, 지연, 오늘 완료 건수와 carrier 현황을 반환한다 | overview 집계는 shipment 원본을 변경하지 않는다 |
| `SHP-F002` | 배송 shipment 목록을 조회한다 | Mobile Operator | Shipping Operations | `ShipmentSummary`, `ShipmentRecord` | Query | 인증 토큰이 유효하고 shipment bootstrap 데이터가 존재해야 한다 | 배송 목록과 최신 이벤트를 반환한다 | 목록 행은 `shipment_id`, `order_id`, `carrier`, `status`, `eta`를 유지한다 |
| `SHP-F003` | 배송 상태를 갱신한다 | Mobile Operator | Shipping Operations | `UpdateShipmentStatusCommand`, `ShipmentStatusTransition`, `ShipmentRecord` | Command | 인증 토큰이 유효하고 요청한 `shipment_id`가 존재해야 한다 | shipment의 `status`, `last_event`, 선택적 `eta`가 갱신된다 | 존재하지 않는 `shipment_id`면 `404`를 반환한다 |

## 7. Notes

- `shipping`은 출고 이후 배송 추적 책임을 `fulfillment`에서 분리해 downstream delivery 상태만 소유한다.
- 고객-facing tracking 경험은 아직 포함하지 않고 operator/mobile surface만 baseline으로 제공한다.
