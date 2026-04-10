# repository governance

## Covered Planning Artifact

- `sdd/02_plan/03_architecture/repository_governance.md`

## Implemented Scope

- 템플릿 저장소는 `server`, `client`, `infra`, `.github`, `.codex`, `sdd`를 기준으로 유지된다.
- SDD는 final-only delivery system으로 동작한다.
- planning data modeling root는 `04_data`로 유지된다.
- screen build summary는 `03_build/02_screen/<service>/` split을 기준으로 유지된다.

## Implementation Shape

- backend는 hexagonal + DDD domain split을 사용한다.
- frontend는 4개 service app split을 사용한다.
- automation과 repo-local skill은 `sdd/99_toolchain`과 `.codex/skills`에 함께 정리된다.
