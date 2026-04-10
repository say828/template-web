# SDD Governance

## Purpose

- `sdd/`는 템플릿 레포의 canonical delivery system이다.
- 모든 SDD 산출물은 현재 기준의 최종 일관성만 설명한다.

## Final-Only Rule

- `sdd/` 안에는 날짜별 히스토리, archive, release log, gate log 같은 누적 기록을 두지 않는다.
- 같은 대상의 후속 작업은 새 문서를 만들지 않고 기존 durable 문서를 덮어써 갱신한다.
- raw runtime log, backend log, infrastructure log는 SDD가 아니라 해당 운영 시스템의 역할이다.

## Section Map

- `01_planning/`: 현재 canonical spec과 source reference
- `02_plan/`: 에이전트의 current executable plan
- `03_build/`: 현재 구현 요약
- `03_verify/`: 현재 retained verification summary
- `05_operate/`: 현재 delivery status와 runbook
- `99_toolchain/`: SDD를 유지하는 생성기, 자동화, 정책 문서
