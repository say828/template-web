# support feature spec

- 작성 버전: 1.1.0

## 1. Purpose

`support` bounded context가 제공하는 관리자 FAQ/support 관리 기능을 구현 기준으로 정리한다.

## 2. Scope

- 포함 범위:
  - admin surface에서 FAQ/support 항목 목록 조회
  - FAQ 작성과 visibility 변경 command
- 제외 범위:
  - end-user 문의 inbox나 대화형 support workflow
  - notification, ticket assignment 같은 별도 support operations

## 3. Actor Summary

| Actor | Description | Appears In |
| --- | --- | --- |
| `Admin Operator` | admin 서비스에서 FAQ/support 콘텐츠를 조회하고 등록하거나 공개 상태를 바꾸는 운영 관리자다. | `SUP-F001`, `SUP-F002`, `SUP-F003` |

## 4. Bounded Context Summary

| Item | Value |
| --- | --- |
| Domain Code | `SUP` |
| Bounded Context | Support Content |
| Primary Backend Owner | `server/contexts/support` |
| Related Context | `auth` |
| Main Entry Contract | `GET /api/v1/support/faqs`, `POST /api/v1/support/faqs`, `PATCH /api/v1/support/faqs/{faq_id}/visibility` |

## 5. Aggregate / Model Snapshot

| Aggregate / Model | Role |
| --- | --- |
| `SupportFaq` | FAQ/support 항목 읽기 모델 |
| `SupportFaqRecord` | FAQ 저장/수정 결과 모델 |
| `CreateSupportFaqCommand` | FAQ 작성 명령 |
| `ChangeFaqVisibilityCommand` | FAQ 공개 상태 변경 명령 |

## 6. Use Case Matrix

| Feature Code | Use Case | Actor | Bounded Context | Aggregate / Model | Type | Preconditions | Domain Outcome | Invariant / Business Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SUP-F001` | FAQ/support 목록을 조회한다 | Admin Operator | Support Content | `SupportFaq`, `SupportFaqRecord` | Query | 관리자 토큰이 유효하고 support bootstrap 데이터가 존재해야 한다 | 질문과 visibility가 포함된 FAQ 목록을 반환한다 | admin support surface는 질문 목록과 visibility를 같은 read model로 유지한다 |
| `SUP-F002` | FAQ 항목을 새로 등록한다 | Admin Operator | Support Content | `CreateSupportFaqCommand`, `SupportFaqRecord` | Command | 관리자 토큰이 유효하고 question, answer가 전달되어야 한다 | 새 FAQ 레코드가 생성되어 목록에 추가된다 | 새 FAQ는 문자열 ID와 `updated_at`을 갖는다 |
| `SUP-F003` | FAQ 노출 상태를 변경한다 | Admin Operator | Support Content | `ChangeFaqVisibilityCommand`, `SupportFaqRecord` | Command | 관리자 토큰이 유효하고 요청한 `faq_id`가 존재해야 한다 | FAQ의 `visibility`가 새 값으로 갱신된다 | 존재하지 않는 `faq_id`면 `404`를 반환한다 |

## 7. Notes

- 현재 `support`는 FAQ 중심 운영 content context이고, create/visibility change만 command surface로 제공한다.
