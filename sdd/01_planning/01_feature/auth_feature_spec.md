# auth feature spec

- 작성 버전: 1.1.0

## 1. Purpose

`auth` bounded context가 제공하는 인증과 현재 세션 해석 기능을 구현 기준으로 정리한다.

## 2. Scope

- 포함 범위:
  - 이메일/비밀번호 기반 로그인과 bearer token 기반 현재 세션 해석
  - `auth_accounts.json`이 소유하는 credential 검증과 공통 session contract
- 제외 범위:
  - 사용자 프로필 조회/변경과 role 관리
  - 로그인 이후 서비스별 route 분기나 client-side token 저장 방식

## 3. Actor Summary

| Actor | Description | Appears In |
| --- | --- | --- |
| `Web User` | web 서비스에서 주문/운영 기능에 접근하기 위해 인증 세션을 발급받는 사용자다. | `AUT-F001` |
| `Mobile Operator` | mobile 서비스에서 이행 작업을 수행하기 위해 로그인하는 현장 운영자다. | `AUT-F001` |
| `Admin Operator` | admin 서비스에서 카탈로그, 재고, 사용자 운영 명령을 수행하기 위해 관리자 세션을 발급받는 주체다. | `AUT-F001` |
| `Landing Member` | landing 서비스에서 회원 전용 자원이나 개인화 동작을 사용하기 위해 로그인하는 사용자다. | `AUT-F001` |
| `Authenticated Client` | 이미 bearer token을 보유한 frontend runtime 또는 HTTP client로 현재 세션 사용자 해석을 요청하는 주체다. | `AUT-F002` |

## 4. Bounded Context Summary

| Item | Value |
| --- | --- |
| Domain Code | `AUT` |
| Bounded Context | Authentication & Session |
| Primary Backend Owner | `server/contexts/auth` |
| Related Context | `server/contexts/user` |
| Main Entry Contract | `POST /api/v1/auth/login`, `GET /api/v1/auth/me` |

## 5. Aggregate / Model Snapshot

| Aggregate / Model | Role |
| --- | --- |
| `LoginCommand` | 로그인 명령 입력 모델 |
| `AuthToken` | bearer token 응답 모델 |
| `AuthAccountRecord` | 인증 계정 저장 모델 |
| `AuthenticatedUser` | 현재 세션 사용자 응답 모델 |

## 6. Use Case Matrix

| Feature Code | Use Case | Actor | Bounded Context | Aggregate / Model | Type | Preconditions | Domain Outcome | Invariant / Business Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `AUT-F001` | 이메일/비밀번호로 로그인하고 access token을 발급한다 | Web User, Mobile Operator, Admin Operator, Landing Member | Authentication & Session | `LoginCommand`, `AuthToken`, `AuthAccountRecord` | Command | 이메일과 비밀번호가 전달되고, 인증 계정 저장소에 해당 사용자가 존재해야 한다 | access token과 `user_id`가 발급된다 | credential이 일치하지 않으면 `401 Invalid credentials`를 반환한다 |
| `AUT-F002` | bearer token으로 현재 세션 사용자를 해석한다 | Authenticated Client | Authentication & Session | `AuthToken`, `AuthenticatedUser`, `AuthAccountRecord` | Query | 유효한 bearer token이 전달되고 token subject가 인증 계정 저장소에 존재해야 한다 | 현재 사용자 summary를 반환한다 | token이 위조되었거나 subject 사용자가 없으면 `401 Invalid token`을 반환한다 |

## 7. Notes

- `auth`는 `auth_accounts.json` bootstrap을 소유하며 `user` profile 저장과 credential 저장을 분리한다.
- 인증 성공 이후 권한별 화면 분기는 frontend service에서 처리하고, backend는 공통 session contract만 제공한다.
