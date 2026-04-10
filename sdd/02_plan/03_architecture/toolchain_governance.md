# toolchain governance

- Owner: Codex
- Status: active

## Scope

- In scope:
  - `sdd/99_toolchain` 아래 자동화 도구와 policy 문서의 current rule 유지
  - Playwright exactness runner/manifest를 local screen regression의 canonical gate로 유지
  - skill/tooling path와 proof artifact path 정렬
  - local Claude/Codex `sdd` skill의 canonical path와 실제 저장소 구조 정렬
  - `sdd` skill의 rollout gate를 explicit deployment scope 기준으로 제한
  - 존재하지 않는 template builder file을 required canonical path처럼 안내하지 않도록 정리
  - 프로젝트 루트에서 `sdd` skill을 설명하는 단일 entrypoint 문서 유지
  - 루트 `SDD_SKILL.md`가 workflow, `sdd/` 구조, flow별 설명까지 포함하도록 확장
  - 루트 `SDD_SKILL.md`가 toolchain, visual fidelity, exactness, functional alignment 구조까지 설명하도록 확장
  - 루트 `SDD_SKILL.md`가 `sdd` 스킬의 trigger, non-use case, governance, section map, schema parity, regression, rollout, completion gate까지 포함하도록 확장
  - ignored 상태였던 durable local scaffold/config를 template-tracked asset으로 승격
- Out of scope:
  - 개별 서비스 구현

## Acceptance Criteria

- [x] skill/tooling 관련 경로가 current SDD 구조를 가리킨다.
- [x] proof artifact 예시도 final-only verify structure를 따른다.
- [x] toolchain 설명은 현재 workflow rule만 남긴다.
- [x] 화면명세 기반 정적 자산은 canonical `스펙에셋빌더` 선행 추출 rule을 current workflow로 유지한다.
- [x] 회귀 검수 범위 선택 rule이 policy, toolchain, skill, SDD test 문서에 공통 반영된다.
- [x] `.claude/skills/sdd-dev/SKILL.md`의 Codex canonical path가 실제 `.codex/skills/sdd/` 구조를 가리킨다.
- [x] `sdd` skill은 rollout이 explicit scope일 때만 DEV/PROD/rollback gate를 completion bar로 해석한다.
- [x] 디자인 가이드 builder 안내는 현재 저장소에 실제로 존재하는 automation inventory 기준으로만 적는다.
- [x] 프로젝트 루트에서 `sdd` skill 용도와 canonical path를 빠르게 확인할 수 있는 단일 markdown entrypoint가 있다.
- [x] `SDD_SKILL.md`는 요약 수준을 넘어서 workflow, folder structure, flow별 역할을 명확하게 설명한다.
- [x] `SDD_SKILL.md`는 toolchain 역할과 visual fidelity / exactness / 기능 정합성 구조를 명확하게 설명한다.
- [x] `SDD_SKILL.md`는 `sdd` 스킬의 거의 전체 해설서 수준으로 trigger, artifact rule, rollout gate, completion gate까지 설명한다.
- [x] durable local scaffold/config 파일은 tracked asset으로 승격되고, generated/cache artifact는 계속 ignore된다.
- [x] Playwright screen exactness는 ad-hoc CLI가 아니라 `sdd/99_toolchain/01_automation/` wrapper/manifest 기준으로 실행한다.

## Execution Checklist

- [x] stale verify/build path를 current path로 교체한다.
- [x] toolchain README와 design note를 current governance와 정렬한다.
- [x] reusable template path를 final-only 구조에 맞춘다.
- [x] screen-spec static asset extraction rule을 skill과 toolchain 문서에 공통 반영한다.
- [x] regression verification rule을 policy, skill, toolchain, test planning에 공통 반영한다.
- [x] Claude `sdd-dev` alias가 stale `.codex/skills/sdd-dev/` 경로를 참조하지 않도록 정리한다.
- [x] Codex/Claude `sdd` skill에서 rollout gate를 explicit deployment scope 조건으로 정리한다.
- [x] 존재하지 않는 `screen_design_guide_builder.py`를 template canonical file처럼 적지 않도록 수정한다.
- [x] 루트에 `sdd` skill 요약 문서를 추가하고 canonical source를 명시한다.
- [x] 루트 `SDD_SKILL.md`에 workflow 단계, section 역할, flow별 상세 설명을 보강한다.
- [x] 루트 `SDD_SKILL.md`에 toolchain, parity/proof, exactness, functional alignment 설명을 추가한다.
- [x] 루트 `SDD_SKILL.md`에 trigger rule, non-use case, governance, section routing, schema parity, regression, completion gate 설명을 추가한다.
- [x] `.claude/settings.local.json`, `.agent/sdd-build-ast-audit.json`, `.agent/runs/README.md`를 tracked asset으로 승격한다.
- [x] `node_modules`, `dist`, `.venv`, `.terraform`, cache 계열은 generated/local artifact로 계속 제외한다.
- [x] Playwright exactness suite registry와 runner를 toolchain canonical entrypoint로 편입한다.
- [x] screen template가 suite id와 canonical runner command를 기본 항목으로 가진다.

## Current Notes

- toolchain은 `sdd/99_toolchain/01_automation`, `02_policies`, `03_templates` current split을 따른다.
- Playwright local exactness는 `run_playwright_exactness.py`와 `playwright_exactness_manifest.py`를 canonical entrypoint로 사용한다.
- screen 작업은 가능하면 `npx playwright test ...`를 직접 쓰지 않고 toolchain runner를 통해 suite id 기준으로 실행한다.
- proof artifact는 `sdd/03_verify/10_test/ui_parity/` current path를 기준으로 관리한다.
- toolchain 정책 문서의 정본은 `sdd/99_toolchain/02_policies`에 둔다.
- skill/tooling 사용 여부는 개별 dated memo가 아니라 현재 workflow rule로만 유지한다.
- 화면명세서의 icon/image/logo 등 재사용 가능한 정적 자산은 `spec_asset_builder.py` 또는 wrapper를 먼저 사용해 추출하고, 수동 재작성은 builder가 표현하지 못하는 경우에만 예외로 허용한다.
- reusable asset planning root는 `sdd/01_planning/02_screen/assets/`이고, local Codex/Claude `sdd` skill도 같은 경로 기준으로 유지한다.
- 회귀 검수는 direct target-only 확인으로 끝내지 않고, `sdd/02_plan/10_test/regression_verification.md` 기준으로 selected surface를 retained current-state로 남긴다.
- Claude `sdd-dev` canonical asset reference는 현재 저장소의 `.codex/skills/sdd/` path를 기준으로 맞춘다.
- rollout, DEV/PROD gate, rollback rule은 사용자가 배포를 요청했거나 저장소의 current policy/plan이 rollout을 completion bar로 올린 경우에만 강제한다.
- 디자인 가이드 builder reference는 실제 존재하는 automation inventory를 기준으로 적고, 없는 file path를 canonical prerequisite처럼 고정하지 않는다.
- 루트 `SDD_SKILL.md`는 단순 요약이 아니라 입문용 설명 문서로 유지하되, canonical rule은 local skill 원문과 toolchain policy에 둔다.
- 루트 `SDD_SKILL.md`는 builder/harness/policy가 visual fidelity, exactness, 기능 정합성을 어떻게 연결하는지까지 설명한다.
- 루트 `SDD_SKILL.md`는 skill 원문을 읽기 전에 전체 mental model을 잡는 해설서 역할을 하도록 유지한다.
- `.claude/settings.local.json`은 local permission preset이지만 현재 템플릿이 재사용하는 scaffold로 승격한다.
- `.agent/sdd-build-ast-audit.json`과 `.agent/runs/README.md`는 Ralph/AST scaffold의 durable template asset으로 승격한다.
- generated output인 `dist`, `node_modules`, `.venv`, `.terraform`, cache, runtime run output은 계속 template commit 대상에서 제외한다.

## Validation

- current references:
  - `AGENTS.md`
  - `.codex/skills/sdd/SKILL.md`
  - `.claude/skills/sdd/SKILL.md`
  - `.claude/skills/sdd-dev/SKILL.md`
  - `.claude/settings.local.json`
  - `.agent/sdd-build-ast-audit.json`
  - `.agent/runs/README.md`
  - `SDD_SKILL.md`
  - `sdd/01_planning/02_screen/assets/README.md`
  - `sdd/99_toolchain/01_automation/README.md`
  - `sdd/99_toolchain/01_automation/playwright_exactness_manifest.py`
  - `sdd/99_toolchain/01_automation/run_playwright_exactness.py`
  - `sdd/02_plan/10_test/verification_strategy.md`
  - `sdd/03_verify/10_test/verification_harness.md`
  - `sdd/99_toolchain/02_policies/regression-verification-policy.md`
  - `sdd/02_plan/10_test/regression_verification.md`
