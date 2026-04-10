# user feature spec

- 작성 버전: 1.1.0

## 1. Purpose

`user` bounded context가 제공하는 사용자 디렉터리 조회와 상태 변경 기능을 구현 기준으로 정리한다.

## 2. Scope

- 포함 범위:
  - admin surface에서 사용자 목록/상세 조회
  - 사용자 운영 상태 변경 command
- 제외 범위:
  - 로그인, 세션 발급, credential 검증
  - end-user 자기 프로필 수정 같은 self-service profile workflow

## 3. Actor Summary

| Actor | Description | Appears In |
| --- | --- | --- |
| `Admin Operator` | admin 서비스에서 사용자 디렉터리를 조회하고 운영 상태를 변경하는 관리자다. | `USR-F001`, `USR-F002`, `USR-F003` |

## 4. Bounded Context Summary

| Item | Value |
| --- | --- |
| Domain Code | `USR` |
| Bounded Context | User Directory |
| Primary Backend Owner | `server/contexts/user` |
| Related Context | `auth` |
| Main Entry Contract | `GET /api/v1/users`, `GET /api/v1/users/{user_id}`, `PATCH /api/v1/users/{user_id}/status` |

## 5. Aggregate / Model Snapshot

| Aggregate / Model | Role |
| --- | --- |
| `UserRecord` | profile 저장 모델 |
| `UserSummary` | 사용자 목록 응답 모델 |
| `UserDetail` | 단일 사용자 상세 응답 모델 |
| `UpdateUserStatusCommand` | 사용자 상태 전이 명령 |

## 6. Use Case Matrix

| Feature Code | Use Case | Actor | Bounded Context | Aggregate / Model | Type | Preconditions | Domain Outcome | Invariant / Business Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `USR-F001` | 사용자 summary 목록을 조회한다 | Admin Operator | User Directory | `UserSummary`, `UserRecord` | Query | 관리자 토큰이 유효하고 사용자 bootstrap 데이터가 존재해야 한다 | 사용자 목록을 반환한다 | 목록 행은 `id`, `name`, `email`, `role`, `status`를 유지한다 |
| `USR-F002` | 단일 사용자 상세를 조회한다 | Admin Operator | User Directory | `UserDetail`, `UserRecord` | Query | 관리자 토큰이 유효하고 요청한 `user_id`가 저장소에 존재해야 한다 | timezone과 last login이 포함된 상세를 반환한다 | 존재하지 않는 `user_id`면 `404 User not found`를 반환한다 |
| `USR-F003` | 사용자의 운영 상태를 변경한다 | Admin Operator | User Directory | `UpdateUserStatusCommand`, `UserDetail`, `UserRecord` | Command | 관리자 토큰이 유효하고 요청한 `user_id`가 저장소에 존재해야 한다 | 대상 사용자의 `status`가 새 값으로 갱신된다 | 존재하지 않는 `user_id`면 `404 User not found`를 반환한다 |

## 7. Notes

- `user`는 profile directory context이고 credential hash를 소유하지 않는다.
- 인증 credential은 `auth` context가 별도 bootstrap 저장소로 관리한다.
