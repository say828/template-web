# Account And Access

## Covered Planning Artifacts

- `sdd/01_planning/01_feature/auth_feature_spec.md`
- `sdd/01_planning/01_feature/user_feature_spec.md`

## Implemented Scope

- 인증과 사용자 baseline은 `auth`, `user` context로 분리되어 있다.
- 세션 발급, current user 조회, admin user surface 같은 핵심 access 흐름은 backend context와 frontend typed API 조합으로 구성된다.

## Implementation Shape

- backend owner는 `server/contexts/auth`, `server/contexts/user`다.
- frontend surface는 `client/web`, `client/admin`, `client/mobile`에서 공통 auth/session contract를 소비한다.

## Current Behavior

- 템플릿은 로그인, current user, basic account 관리 예시를 current baseline으로 제공한다.
