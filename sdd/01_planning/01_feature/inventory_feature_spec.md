# inventory feature spec

- 작성 버전: 1.1.0

## 1. Purpose

`inventory` bounded context가 제공하는 재고 조회와 관리자 재고 조정 기능을 구현 기준으로 정리한다.

## 2. Scope

- 포함 범위:
  - SKU/거점 단위 재고 read model과 관리자 재고 mutation command
  - 수동 조정, 선점, 해제, 절대값 설정 같은 inventory 내부 상태 변경
- 제외 범위:
  - 주문/이행 context가 자동으로 일으키는 재고 orchestration
  - 창고 배차, 입고, 출고 작업 계획의 상세 workflow

## 3. Actor Summary

| Actor | Description | Appears In |
| --- | --- | --- |
| `Admin Operator` | admin 서비스에서 재고 현황을 조회하고 조정, 선점, 해제, 재설정 같은 운영 명령을 수행하는 관리자다. | `INV-F001`, `INV-F002`, `INV-F003`, `INV-F004`, `INV-F005`, `INV-F006` |

## 4. Bounded Context Summary

| Item | Value |
| --- | --- |
| Domain Code | `INV` |
| Bounded Context | Inventory Availability |
| Primary Backend Owner | `server/contexts/inventory` |
| Related Context | `auth`, `catalog`, `orders` |
| Main Entry Contract | `GET /api/v1/inventory/levels`, `GET /api/v1/inventory/levels/{sku}/{location_id}`, `POST /api/v1/inventory/levels/{sku}/{location_id}/adjustments`, `POST /api/v1/inventory/levels/{sku}/{location_id}/reservations`, `POST /api/v1/inventory/levels/{sku}/{location_id}/releases`, `PUT /api/v1/inventory/levels/{sku}/{location_id}` |

## 5. Aggregate / Model Snapshot

| Aggregate / Model | Role |
| --- | --- |
| `InventoryLevelRecord` | SKU-거점별 재고 원본 |
| `InventoryLevel` | 재고 조회 응답 모델 |
| `AdjustInventoryCommand` | cycle count 등 수동 증감 명령 |
| `ReserveInventoryCommand` | 주문 선점 명령 |
| `ReleaseInventoryCommand` | 선점 해제 명령 |
| `SetInventoryLevelCommand` | 절대값 설정 명령 |
| `InventoryMutationReceipt` | 재고 조정 결과 응답 |

## 6. Use Case Matrix

| Feature Code | Use Case | Actor | Bounded Context | Aggregate / Model | Type | Preconditions | Domain Outcome | Invariant / Business Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `INV-F001` | 재고 레벨 목록을 조회한다 | Admin Operator | Inventory Availability | `InventoryLevel`, `InventoryLevelRecord` | Query | 관리자 토큰이 유효하고 inventory bootstrap 데이터가 존재해야 한다 | SKU, 상품, 거점, 상태 기준 재고 레벨 목록을 반환한다 | `status`는 `available_to_sell`과 `reorder_point` 계산 결과로 결정된다 |
| `INV-F002` | 단일 SKU/거점 재고 상세를 조회한다 | Admin Operator | Inventory Availability | `InventoryLevel`, `InventoryLevelRecord` | Query | 관리자 토큰이 유효하고 요청한 `sku/location_id` 조합이 존재해야 한다 | 선택한 재고 레벨의 가용 재고와 재주문 여부를 반환한다 | 존재하지 않는 조합이면 `404 Inventory level not found`를 반환한다 |
| `INV-F003` | 재고를 증감 조정한다 | Admin Operator | Inventory Availability | `AdjustInventoryCommand`, `InventoryMutationReceipt`, `InventoryLevelRecord` | Command | 관리자 토큰이 유효하고 요청한 재고 레벨이 존재해야 한다 | `on_hand`가 증감되고 조정 영수증을 반환한다 | delta는 0일 수 없고, 조정 후 `on_hand`는 `reserved`보다 작아질 수 없다 |
| `INV-F004` | 재고를 선점한다 | Admin Operator | Inventory Availability | `ReserveInventoryCommand`, `InventoryMutationReceipt`, `InventoryLevelRecord` | Command | 관리자 토큰이 유효하고 요청한 재고 레벨이 존재해야 한다 | `reserved` 수량이 증가한다 | 선점 수량은 가용 재고를 초과할 수 없다 |
| `INV-F005` | 선점된 재고를 해제한다 | Admin Operator | Inventory Availability | `ReleaseInventoryCommand`, `InventoryMutationReceipt`, `InventoryLevelRecord` | Command | 관리자 토큰이 유효하고 요청한 재고 레벨이 존재해야 한다 | `reserved` 수량이 감소한다 | 해제 수량은 현재 `reserved`를 초과할 수 없다 |
| `INV-F006` | 재고 절대값을 재설정한다 | Admin Operator | Inventory Availability | `SetInventoryLevelCommand`, `InventoryMutationReceipt`, `InventoryLevelRecord` | Command | 관리자 토큰이 유효하고 요청한 재고 레벨이 존재해야 한다 | `on_hand`, `reserved`, `safety_stock`, `reorder_point`가 새 값으로 설정된다 | `reserved`는 `on_hand`보다 클 수 없다 |

## 7. Notes

- inventory는 현재 admin 전용 운영 컨텍스트다.
- order/fulfillment에서 직접 inventory mutation을 일으키는 orchestration은 아직 없고, template baseline에서는 admin command로 먼저 노출한다.
