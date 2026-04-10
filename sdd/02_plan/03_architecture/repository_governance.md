# repository governance

- Owner: Codex
- Status: active

## Scope

- In scope:
  - `main` canonical branch 운영
  - repo path와 주요 문서 구조 정합성 유지
  - SDD final-only 원칙 유지
- Out of scope:
  - 서비스별 feature/screen 상세 TODO

## Acceptance Criteria

- [x] `main`을 정본 브랜치로 유지한다.
- [x] repo 경로와 주요 문서는 현재 `client/*`, `server/*`, `sdd/*` 구조를 기준으로 설명한다.
- [x] plan/build/verify/operate는 dated history 없이 durable 문서만 유지한다.

## Execution Checklist

- [x] branch 운영 원칙을 현재 방식으로 고정한다.
- [x] repo 주요 경로 기준을 `client/*`, `server/*`, `sdd/*` 구조로 고정한다.
- [x] SDD final-only 원칙을 반영한다.

## Current Notes

- `main`을 canonical branch로 유지하는 규칙을 사용한다.
- 템플릿 frontend 경로는 `client/web`, `client/admin`, `client/mobile`, `client/landing` 기준이다.
- SDD는 최종 일관성 문서만 유지하고, raw 운영 로그는 runtime logging system에 남긴다.
- data modeling 계획 루트는 `sdd/01_planning/04_data`와 `sdd/02_plan/04_data`를 기준으로 유지한다.

## Validation

- current references:
  - `AGENTS.md`
  - `sdd/03_build/03_architecture/repository_governance.md`
  - `sdd/03_verify/03_architecture/repository_governance.md`
