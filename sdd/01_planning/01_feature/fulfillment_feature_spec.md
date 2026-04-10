# fulfillment feature spec

- 작성 버전: 1.1.0

## 1. Purpose

`fulfillment` bounded context가 제공하는 모바일 운영 overview와 task board 기능을 구현 기준으로 정리한다.

## 2. Scope

- 포함 범위:
  - mobile 서비스의 fulfillment overview, board, note read model
  - fulfillment task 상태 전이 command
- 제외 범위:
  - route 최적화나 배차 같은 고도화 계획
  - fulfillment 외부 context를 직접 갱신하는 orchestration

## 3. Actor Summary

| Actor | Description | Appears In |
| --- | --- | --- |
| `Mobile Operator` | mobile 서비스에서 현장 이행 작업을 수행하며 task 현황을 보고 상태를 갱신하는 운영자다. | `FUL-F001`, `FUL-F002`, `FUL-F003` |

## 4. Bounded Context Summary

| Item | Value |
| --- | --- |
| Domain Code | `FUL` |
| Bounded Context | Fulfillment Operations |
| Primary Backend Owner | `server/contexts/fulfillment` |
| Related Context | `auth`, `orders`, `inventory` |
| Main Entry Contract | `GET /api/v1/fulfillment/overview`, `GET /api/v1/fulfillment/board`, `PATCH /api/v1/fulfillment/tasks/{task_id}/status` |

## 5. Aggregate / Model Snapshot

| Aggregate / Model | Role |
| --- | --- |
| `FulfillmentTaskRecord` | 이행 task 원본 |
| `FulfillmentOverview` | 모바일 dashboard overview 응답 |
| `FulfillmentBoardPayload` | 모바일 task board 응답 |
| `FulfillmentEvent` | timeline 이벤트 모델 |
| `FulfillmentNote` | 운영 note 모델 |
| `FulfillmentTaskStatusTransitionCommand` | task 상태 전이 명령 |
| `FulfillmentTaskStatusTransition` | task 상태 전이 결과 |

## 6. Use Case Matrix

| Feature Code | Use Case | Actor | Bounded Context | Aggregate / Model | Type | Preconditions | Domain Outcome | Invariant / Business Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `FUL-F001` | 이행 overview를 조회한다 | Mobile Operator | Fulfillment Operations | `FulfillmentOverview`, `FulfillmentTaskRecord`, `FulfillmentEvent` | Query | 인증 토큰이 유효하고 task/event bootstrap 데이터가 존재해야 한다 | throughput, stat, timeline, stage load를 반환한다 | `Blocked`와 `Outbound` 지표는 현재 task 상태 집합으로 계산한다 |
| `FUL-F002` | 이행 board와 note 목록을 조회한다 | Mobile Operator | Fulfillment Operations | `FulfillmentBoardPayload`, `FulfillmentTaskRecord`, `FulfillmentNote` | Query | 인증 토큰이 유효하고 task/note bootstrap 데이터가 존재해야 한다 | task board 목록과 note 목록을 함께 반환한다 | board payload는 `tasks`와 `notes` 두 블록을 항상 함께 반환한다 |
| `FUL-F003` | 이행 task 상태를 전환한다 | Mobile Operator | Fulfillment Operations | `FulfillmentTaskStatusTransitionCommand`, `FulfillmentTaskStatusTransition`, `FulfillmentTaskRecord` | Command | 인증 토큰이 유효하고 요청한 `task_id`가 존재해야 한다 | task의 `status`와 선택적 `stage`가 갱신된다 | 존재하지 않는 `task_id`면 `404`를 반환한다 |

## 7. Notes

- `fulfillment`는 mobile 서비스의 canonical backend surface다.
- 출고 이후 배송 추적과 carrier 진행 상태는 별도 `shipping` context가 소유한다.
- timeline과 notes는 별도 bootstrap source를 사용하지만, screen 단위에서는 fulfillment context가 함께 조합해 반환한다.
