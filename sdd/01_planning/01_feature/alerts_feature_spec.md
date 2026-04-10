# alerts feature spec

- 작성 버전: 1.0.0

## 1. Purpose

`alerts` bounded context가 제공하는 운영 알람 feed와 읽음 처리 기능을 구현 기준으로 정리한다.

## 2. Scope

- 포함 범위:
  - admin surface의 운영 알람 목록 조회
  - 알람 단건 읽음 처리와 전체 읽음 처리
- 제외 범위:
  - email, SMS, push 같은 외부 발송 인프라
  - 주문/배송/재고 도메인 내부의 원인 계산 로직 자체

## 3. Actor Summary

| Actor | Description | Appears In |
| --- | --- | --- |
| `Admin Operator` | admin 서비스에서 운영 이벤트와 예외 상황을 확인하고 알람 읽음 상태를 관리하는 운영 관리자다. | `ALR-F001`, `ALR-F002`, `ALR-F003` |

## 4. Bounded Context Summary

| Item | Value |
| --- | --- |
| Domain Code | `ALR` |
| Bounded Context | Alert Center |
| Primary Backend Owner | `server/contexts/alerts` |
| Related Context | `orders`, `shipping`, `inventory`, `support` |
| Main Entry Contract | `GET /api/v1/alerts`, `POST /api/v1/alerts/{alert_id}/read`, `POST /api/v1/alerts/read-all` |

## 5. Aggregate / Model Snapshot

| Aggregate / Model | Role |
| --- | --- |
| `AlertRecord` | 운영 알람 저장 모델 |
| `AlertItem` | 알람 feed 응답 모델 |
| `AlertsPayload` | unread count와 목록을 묶은 응답 모델 |
| `AlertReadResult` | 단건 읽음 처리 결과 |
| `AlertsReadAllResult` | 전체 읽음 처리 결과 |

## 6. Use Case Matrix

| Feature Code | Use Case | Actor | Bounded Context | Aggregate / Model | Type | Preconditions | Domain Outcome | Invariant / Business Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ALR-F001` | 운영 알람 feed를 조회한다 | Admin Operator | Alert Center | `AlertsPayload`, `AlertItem`, `AlertRecord` | Query | 관리자 토큰이 유효하고 alert bootstrap 데이터가 존재해야 한다 | unread count와 최신 운영 알람 목록을 반환한다 | feed 조회는 알람 읽음 상태를 변경하지 않는다 |
| `ALR-F002` | 운영 알람 1건을 읽음 처리한다 | Admin Operator | Alert Center | `AlertReadResult`, `AlertRecord` | Command | 관리자 토큰이 유효하고 요청한 `alert_id`가 존재해야 한다 | 선택한 알람의 `read` 상태가 `true`가 된다 | 존재하지 않는 `alert_id`면 `404`를 반환한다 |
| `ALR-F003` | 운영 알람 전체를 읽음 처리한다 | Admin Operator | Alert Center | `AlertsReadAllResult`, `AlertRecord` | Command | 관리자 토큰이 유효하고 alert bootstrap 데이터가 존재해야 한다 | 미읽음 알람이 모두 읽음 상태로 갱신된다 | 이미 읽은 알람은 중복 변경하지 않는다 |

## 7. Notes

- `alerts`는 admin dashboard의 보조 read model이 아니라 독립 운영 피드로 취급한다.
- 원인 도메인이 무엇이든 admin이 소비하는 알람 표현과 읽음 상태는 `alerts` context가 소유한다.
