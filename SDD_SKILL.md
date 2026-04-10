# SDD Skill

이 문서는 프로젝트 루트에서 `sdd` 스킬을 빠르게 이해하기 위한 안내서다. 목적은 "한 줄 요약"이 아니라, 이 스킬이 강제하는 개발 방식, `sdd/` 폴더 구조, 각 단계에서 무엇을 남겨야 하는지까지 한 번에 설명하는 것이다.

정본은 아래 문서다.

- Codex canonical skill: `.codex/skills/sdd/SKILL.md`
- Codex section map: `.codex/skills/sdd/references/section-map.md`
- Claude canonical workflow: `.claude/skills/sdd-dev/SKILL.md`
- Claude alias: `.claude/skills/sdd/SKILL.md`
- Claude alias: `.claude/skills/sdd-development/SKILL.md`

## 한 줄 정의

`sdd` 스킬은 "코드를 먼저 고치고 나중에 문서를 맞추는" 방식이 아니라, `sdd/`를 설계와 실행의 단일 delivery system으로 보고 planning -> plan -> build -> verify -> operate를 current-state artifact로 유지하게 만드는 개발 스킬이다.

## 왜 필요한가

일반적인 저장소에서는 요구사항, 설계, 작업 계획, 구현 결과, 검증 결과가 여러 위치에 흩어지기 쉽다. `sdd` 스킬은 이 문제를 막기 위해 다음을 강제한다.

- 요구사항과 설계는 `sdd/01_planning`에서 확인한다.
- 지금 당장 수행 중인 작업 계획은 `sdd/02_plan`에 적는다.
- 실제 구현 결과는 `sdd/03_build`에 남긴다.
- 검증 근거와 residual risk는 `sdd/03_verify`에 남긴다.
- 실제 배포와 운영 결과가 있었을 때만 `sdd/05_operate`를 갱신한다.

즉, 이 스킬의 핵심은 "코드 변경" 자체가 아니라 "코드 변경을 설명하고 검증 가능한 current-state trail"을 같이 만드는 것이다.

## 언제 쓰는가

다음 조건이면 기본적으로 `sdd` 스킬 대상이다.

- 저장소가 `sdd/01_planning`, `02_plan`, `03_build`, `03_verify`, `05_operate` 구조를 사용한다.
- 사용자가 구현, 수정, 리팩토링, 테스트, 배포, 화면 작업처럼 실제 개발 지시를 한다.
- 결과물이 코드 변경만으로 끝나면 안 되고, durable plan/build/verify 기록이 남아야 한다.

반대로 다음 경우에는 보통 `sdd` 스킬 대상이 아니다.

- 단순 질의응답만 있는 경우
- 일회성 로컬 디버깅처럼 durable artifact가 필요 없는 경우
- 저장소가 `sdd/`를 canonical 문서 시스템으로 쓰지 않는 경우

## 어떤 요청이 `sdd` 스킬을 트리거하는가

실제 운용에서는 아래 같은 요청이 `sdd` 스킬 트리거로 해석된다.

- 개발해
- 작업해
- 구현해
- 수정해
- 고쳐
- 리팩토링해
- 테스트해
- 배포해
- 화면명세서
- 화면설계서
- 화면 설계
- 화면
- 화면 스펙
- UI
- 디자인
- 디자인 가이드
- screen spec
- screen design

즉 "코드를 바꾸고 그 결과를 durable artifact로 남겨야 하는 개발 요청"이면 기본적으로 `sdd` 스킬 영역이라고 보면 된다.

## `sdd` 스킬이 아닌 경우를 더 구체적으로 말하면

아래는 `sdd` 스킬을 굳이 쓰지 않는 쪽에 가깝다.

- 단순 설명 요청
- 레포를 변경하지 않는 리뷰성 질의
- 임시 로컬 조사
- 결과를 `sdd/`에 남길 필요가 없는 실험

다만 이 구분은 "코드를 몇 줄 바꾸느냐"가 아니라 "current-state delivery trail이 필요한가"로 판단한다.

## 이 스킬이 보는 정본과 우선순위

`sdd` 스킬은 아무 문서나 동등하게 보지 않는다. 우선순위가 있다.

1. 저장소 정책과 실행 규칙
   - `AGENTS.md`
   - `sdd/99_toolchain/02_policies/`
2. skill 원문
   - `.codex/skills/sdd/SKILL.md`
   - `.claude/skills/sdd-dev/SKILL.md`
3. section map과 automation inventory
   - `.codex/skills/sdd/references/section-map.md`
   - `sdd/99_toolchain/01_automation/README.md`
4. 실제 작업별 planning / plan / verify baseline
   - `sdd/01_planning/...`
   - `sdd/02_plan/...`
   - `sdd/02_plan/10_test/...`

루트 `SDD_SKILL.md`는 설명서다. 실제 강제 규칙이 충돌하면 skill 원문과 policy가 우선이다.

## 이 스킬이 강제하는 전체 워크플로우

### 1. Planning 확인

작업 전 먼저 `sdd/01_planning`에서 현재 설계와 요구사항을 확인한다. 여기서 중요한 점은 "필요한 planning만 읽는다"는 것이다. 모든 planning을 다 읽는 게 아니라, 이번 변경이 feature인지, screen인지, architecture인지, data인지에 따라 필요한 부분만 확인한다.

이 단계의 목적은 다음과 같다.

- 현재 구현이 기존 설계와 충돌하는지 확인
- 이번 변경이 실제로 어느 문서 section에 속하는지 결정
- 구현 전에 drift를 먼저 드러내기

### 2. 실행 계획 수립

그 다음 `sdd/02_plan/<section>/`에 현재 작업 계획을 만든다. 이 문서는 작업이 끝난 뒤 쓰는 회고가 아니라, 작업 전에 정렬하기 위한 실행 문서다.

일반적으로 plan에는 아래가 들어간다.

- scope: 이번 작업 범위
- assumptions: 현재 가정
- acceptance criteria: 완료 판단 기준
- execution checklist: 실제 실행 순서
- current notes: 진행 중 판단과 변경점
- validation: 어떤 근거로 끝났다고 볼지

좋은 `sdd` plan은 "무엇을 바꿀지"보다 "무엇을 확인해야 끝나는지"가 분명하다.
같은 turn에서 작업을 완료할 계획이면 checklist나 acceptance criteria에 `정합성 체크 -> main 반영 -> work branch 삭제` 단계도 분리해서 둔다.

### 3. 계획 기준 구현

코드 작업은 plan과 planning artifact가 충분히 맞춰진 뒤 시작한다. 이 단계에서 스킬은 단순 구현만 요구하지 않는다. 필요하면 asset builder, design guide builder, regression baseline, schema 검증 기준 같은 toolchain도 함께 사용하도록 강제한다.

즉 구현 단계의 핵심은 다음이다.

- 코드만 바꾸지 않는다.
- 변경에 필요한 generator, builder, contract, schema 관점도 같이 본다.
- shared surface 영향이 있으면 처음부터 회귀 범위를 넓혀 잡는다.
- 완료된 작업은 work branch 위에만 남겨두지 않는다. 관련 정합성 체크가 끝나면 `main`에 반영하고 branch를 retire한다.

### 4. Build 기록

구현이 끝나면 `sdd/03_build`에 "무엇을 만들었는지"를 current-state로 남긴다. 이 문서는 작업 로그가 아니라 현재 구현 상태 설명이다.

여기에는 보통 다음이 들어간다.

- 실제 반영된 범위
- 변경된 runtime surface
- 사용한 asset / builder / contract
- 구현 후 현재 동작 방식

즉 `03_build`는 "우리가 무엇을 했는가"보다 "지금 시스템이 어떤 상태인가"를 설명해야 한다.

### 5. Verify 기록

`sdd/03_verify`는 단순히 "테스트 통과"를 적는 곳이 아니다. 어떤 검증을 했는지, 어떤 범위를 확인했는지, 무엇이 아직 residual risk인지 명확하게 남겨야 한다.

중요한 검증 규칙은 다음과 같다.

- edited target만 확인하고 끝내지 않는다.
- direct, upstream, downstream, shared surface를 선택해서 회귀 범위를 잡는다.
- 자동화가 없으면 manual/command 검증이라도 current-state로 남긴다.
- persistence 영향이 있으면 실제 schema 상태도 확인 대상으로 본다.

### 6. Operate 기록

`sdd/05_operate`는 모든 작업에서 항상 쓰는 폴더가 아니다. 실제 배포나 운영 후속이 범위에 있을 때만 갱신한다.

이 단계의 핵심은 다음이다.

- 배포가 없었는데 운영 문서를 허위로 채우지 않는다.
- DEV/PROD rollout이 실제 범위면 deploy 결과와 운영 baseline을 남긴다.
- rollback이 있었다면 trigger와 결과를 같이 남긴다.

## 문서 거버넌스와 산출물 원칙

`sdd` 스킬은 단순히 "폴더를 나눠 쓴다"가 아니라, 문서의 성격 자체를 강하게 규정한다.

- `sdd/`는 history archive가 아니라 current-state artifact tree다.
- 같은 주제 문서는 누적 로그보다 현재 상태를 덮어쓰며 유지한다.
- 날짜별 메모를 계속 쌓는 방식은 기본 원칙이 아니다.
- plan/build/verify/operate는 채팅 로그가 아니라 레포 안 문서로 남아야 한다.
- `sdd/`가 있으면 병렬 `docs/` 트리를 만들지 않는다.

즉 문서는 "과거 기록 저장소"보다 "지금 시스템 상태의 정본"으로 유지해야 한다.

## Branch Retirement 규칙

`agentic-dev`에서 work branch는 임시 통합 공간이지 완료 상태의 보관 위치가 아니다.

1. task-fit work branch에서 구현하고 origin branch까지 push한다.
2. 관련 build/test/verify 정합성 체크를 최종 상태 기준으로 다시 실행한다.
3. 최종 변경을 `main`과 `origin/main`에 반영한다.
4. `main`이 DEV 배포 baseline이면 그 커밋 기준으로 `DEV(개발계)` 반영과 검증을 수행한다.
5. local work branch와 remote work branch를 삭제한다. 사용자가 유지하라고 명시한 경우만 예외다.

최소 정합성 체크는 다음 세 가지다.

- 관련 canonical 검증 명령이 최신 변경 기준으로 다시 통과했는가
- branch/worktree가 commit 가능한 상태로 정리됐는가
- 전달하려는 최종 변경이 실제로 `main`에 포함됐는가

## 각 artifact에서 반드시 분리해야 하는 것

`sdd` 스킬은 planning, plan, build, verify, operate를 서로 다른 역할로 본다.

- planning: 원래 요구사항과 설계
- plan: 이번 작업의 실행 계획
- build: 실제 구현 결과와 현재 상태
- verify: 검증 근거와 residual risk
- operate: 실제 배포/운영 결과

이 구분이 흐려지면 흔히 이런 문제가 생긴다.

- planning 문서에 구현 로그가 섞임
- build 문서에 테스트 통과 여부만 적음
- verify 문서에 실제 검증 근거 없이 pass만 적음
- operate 문서에 배포도 안 했는데 상태를 써버림

`sdd` 스킬은 이 섞임을 막으려는 구조다.

## `sdd/` 폴더 구조 설명

`sdd/`는 날짜별 히스토리를 쌓는 공간이 아니라 current-state delivery tree다. 즉, 같은 주제의 문서를 계속 덮어쓰며 최신 상태를 유지하는 구조다.

### `sdd/01_planning`

설계와 요구사항의 원천 문서를 둔다. 구현 전에 먼저 보는 영역이다.

- `01_feature`: domain 또는 service 수준 기능 정의
- `02_screen`: 화면 명세, PDF, screen asset planning
- `03_architecture`: runtime 구조, 경계, governance
- `04_data`: 데이터 모델과 관계
- `05_api`: API 계약
- `06_iac`: 인프라/배포 설계
- `07_integration`: 외부 연동 정의
- `08_nonfunctional`: 성능, 안정성, 운영 제약
- `09_security`: 보안 posture와 control planning
- `10_test`: 테스트 전략

이 폴더의 역할은 "해야 할 일의 원형"을 보여주는 것이다.

### `sdd/02_plan`

현재 실행 중인 개발 계획을 둔다. 이 스킬에서 가장 중요한 작업 문서 영역이다.

- feature 작업이면 보통 `01_feature/<domain>_todos.md`
- screen 작업이면 보통 `02_screen/<service>_todos.md`
- cross-cutting work면 architecture, test, iac 같은 section 문서를 사용

이 폴더의 역할은 "이번 작업을 어떻게 끝낼 것인가"를 설명하는 것이다.

### `sdd/03_build`

구현 결과와 현재 반영 상태를 요약한다.

- `01_feature`: 기능 구현 결과
- `02_screen`: 화면 구현 결과
- `03_architecture`: 구조/거버넌스 반영 결과
- `06_iac`: 배포/런타임 구성 결과
- `10_test`: harness, verification tooling 상태

이 폴더의 역할은 "지금 구현이 어떤 상태인가"를 설명하는 것이다.

### `sdd/03_verify`

검증 근거와 residual risk를 current-state로 남긴다.

- `01_feature`: 기능 검증
- `02_screen`: 화면 검증
- `03_architecture`: 구조/거버넌스 검증
- `06_iac`: delivery/runtime 검증
- `10_test`: harness 결과, retained validation reference

이 폴더의 역할은 "무엇을 어떻게 확인했는가"를 설명하는 것이다.

### `sdd/05_operate`

실제 운영/배포 결과가 있을 때만 사용한다.

- `01_runbooks`: 운영 절차
- `02_delivery_status`: 현재 배포 상태, live baseline, monitoring, residual risk

이 폴더의 역할은 "실제 배포 후 현재 운영 상태가 무엇인가"를 설명하는 것이다.

### `sdd/99_toolchain`

`sdd` 워크플로우를 지탱하는 automation, policy, template를 둔다.

- `01_automation`: builder, capture, harness, manifest
- `02_policies`: toolchain 규칙 정본
- `03_templates`: reusable template asset

이 폴더의 역할은 "문서와 구현을 연결하는 실행 도구와 규칙"을 제공하는 것이다.

## section map을 실제 작업에 연결하는 법

section map은 단순 참고표가 아니라 "이번 작업이 어디에 기록돼야 하는가"를 결정하는 기준이다.

예를 들면 다음과 같다.

- 기능 요구사항이 바뀌면 `01_planning/01_feature`와 `02_plan/01_feature`를 본다.
- 화면 정렬이 핵심이면 `01_planning/02_screen`, `02_plan/02_screen`, `03_build/02_screen`, `03_verify/02_screen` 축으로 간다.
- shared governance나 skill rule 정리는 `03_architecture` 축으로 간다.
- schema/API/integration 변화가 크면 data/api/integration planning과 verify를 함께 본다.
- rollout이 실제 범위면 `05_operate`까지 completion trail에 들어온다.

즉 section map은 문서 저장 위치 안내가 아니라, 어떤 검토와 어떤 증거가 필요한지까지 결정하는 라우팅 규칙이다.

## Toolchain을 어떻게 봐야 하는가

`sdd` 스킬에서 toolchain은 부가 기능이 아니다. planning 문서와 실제 구현을 연결하는 실행 계층이다. 즉, 사람이 문서를 읽고 손으로 해석만 하는 것이 아니라, 가능한 부분은 builder, harness, manifest, capture tool로 구조화해서 drift를 줄이는 것이 목표다.

toolchain을 구성하는 주요 축은 다음과 같다.

- spec generator: screen spec PDF, manifest, reference asset을 만든다.
- asset builder: 화면명세 기반 정적 자산을 재사용 가능한 runtime asset으로 만든다.
- capture tooling: reference 화면이나 proof input을 수집한다.
- parity harness: 실제 구현과 reference를 비교하는 자동화 surface를 제공한다.
- policy: 어떤 tool을 언제 써야 하는지, 어떤 결과를 completion evidence로 볼지 정한다.

중요한 점은 toolchain이 planning을 대체하지는 않는다는 것이다. planning은 여전히 사람이 결정해야 하고, toolchain은 그 결정을 반복 가능하고 검증 가능한 형태로 만든다.

## Screen 작업에서 `sdd` 스킬이 특별히 더 엄격한 이유

screen 작업은 겉보기엔 CSS 수정처럼 보여도 실제로는 다음을 동시에 맞춰야 하기 때문이다.

- 명세와 시각 정렬
- route/shell/shared component 구조
- 화면 내 상태 변화
- navigation
- backend/API 연결
- regression surface

그래서 `sdd` 스킬은 screen 작업을 leaf component 편집으로 보지 않는다. 최소한 `app entry -> route -> shell -> section -> component -> leaf` 흐름을 실제 runtime tree로 확인해야 한다.

또한 screen 작업에서 "UI만 먼저"는 기본 완료 조건이 아니다. 기능이 있는 화면이면 functional alignment까지 같이 맞아야 한다.

## Visual Fidelity를 맞추는 구조

`sdd`에서 visual fidelity는 "대충 비슷해 보인다"가 아니라, 화면명세와 실제 runtime tree가 얼마나 정렬되어 있는지를 관리하는 구조다. 이 구조는 보통 아래 순서로 맞춘다.

1. screen spec 또는 design source를 planning에서 확인한다.
2. 필요한 정적 자산이 있으면 `spec_asset_builder.py` 같은 canonical asset builder로 먼저 추출한다.
3. repo에 design guide builder가 있으면 spacing, typography, density, hierarchy 기준을 먼저 확보한다.
4. route -> shell -> section -> component -> leaf 순서의 실제 runtime tree를 확인한다.
5. parity harness나 proof check로 reference와 구현을 비교한다.
6. 차이가 남으면 build/verify 문서에 mismatch와 residual risk를 남긴다.

즉 visual fidelity는 CSS만 맞추는 문제가 아니라 다음 네 층을 함께 맞추는 문제다.

- reference source: 명세 PDF, 캡처 자산, design source
- generated design artifacts: asset builder, design guide builder output
- runtime composition: route, shell, shared component, leaf control
- verification evidence: proof, parity, screenshot, semantic extraction

## Exactness를 맞추는 구조

`sdd`에서 exactness는 "검수자가 보기엔 비슷함"이 아니라, 가능한 경우 reference와 generated/runtime output 사이 차이를 최대한 줄이고 그 근거를 retained artifact로 남기는 것이다.

exactness는 보통 아래처럼 계층적으로 판단한다.

- asset exactness: source crop과 generated asset이 같은지
- layout exactness: spacing, alignment, density, hierarchy가 guide와 맞는지
- content exactness: copy, label, state text, navigation text가 spec과 맞는지
- route exactness: 실제 렌더 경로가 의도한 route/shell tree와 맞는지
- proof exactness: parity harness가 reference 대비 허용 가능한 차이 안에 있는지

이때 exactness를 만드는 구조는 다음과 같다.

- builder exactness: `--verify-exact` 같은 옵션으로 generated asset이 source와 동일한지 확인
- harness exactness: parity/proof harness로 구현 결과를 reference와 비교
- runtime-tree exactness: edited leaf만 보지 않고 top-down tree 전체를 확인
- retained evidence exactness: "맞췄다"는 말이 아니라 어떤 기준과 어떤 output으로 확인했는지 남김

즉 exactness는 subjective approval이 아니라, source -> generated artifact -> runtime -> proof까지 이어지는 체인으로 관리한다.

## 기능 정합성을 맞추는 구조

`sdd`에서 기능 정합성은 UI가 보이는 모습만 맞는 것으로 끝나지 않는다. 화면이 spec과 비슷해도 실제 동작, API 계약, persistence, session, downstream effect가 다르면 완료로 보지 않는다.

기능 정합성을 맞추는 구조는 보통 다음과 같다.

1. planning에서 feature requirement, screen behavior, API contract를 확인한다.
2. `sdd/02_plan` acceptance criteria에 상태 변화, navigation, mutation, error handling, auth/session, persistence 조건을 명시한다.
3. 구현 시 mock/local shadow behavior로 얼버무리지 않고 실제 backend/API contract와 연결한다.
4. persistence 영향이 있으면 deployed schema 상태까지 확인한다.
5. verify에서 direct target뿐 아니라 upstream/downstream/shared surface까지 검수한다.

이 구조의 핵심 계약면은 다음과 같다.

- UI contract: 어떤 화면 구조와 상호작용을 보여야 하는가
- navigation contract: 어떤 상태 변화와 이동이 일어나야 하는가
- API contract: 어떤 request/response shape를 가져야 하는가
- data contract: 어떤 schema, column, constraint, default를 전제로 동작하는가
- integration contract: 외부 연동과 shared consumer가 어떤 결과를 기대하는가

즉 functional alignment는 "화면이 동작해 보임"이 아니라 "요구사항, 계약, 스키마, downstream effect가 서로 맞물림"을 의미한다.

## Schema parity와 persistence 작업은 왜 별도 축인가

`sdd` 스킬은 persistence 영향 작업을 일반 코드 수정과 다르게 본다. 이유는 코드상 모델이나 migration 파일이 맞아 보여도, 실제 배포된 DEV/PROD schema가 다를 수 있기 때문이다.

따라서 아래 작업은 schema parity 확인 대상이다.

- model 변경
- migration 추가/수정
- repository / ORM mapping 수정
- SQL 변경
- runtime failure가 schema drift와 연관될 수 있는 경우

이때 필요한 검증은 보통 다음이다.

- migration state 확인
- 실제 table/column/index/constraint/trigger/default 확인
- DEV/PROD 간 drift 여부 기록
- 남은 위험이 있으면 verify에 residual risk로 기록

즉 schema parity는 선택적 추가 검증이 아니라, persistence 영향 작업의 completion 조건 일부다.

## Regression verification은 왜 별도 구조를 갖는가

이 스킬은 "edited file만 확인하고 끝내는" 검수를 명시적으로 금지한다. 그래서 regression verification은 별도 baseline 문서와 current-state trail을 가진다.

핵심 개념은 네 가지다.

- direct: 직접 수정한 표면
- upstream: 이 변경의 상위 흐름
- downstream: 이 변경의 소비자/후속 흐름
- shared: 공용 route, shell, auth/session, component, contract, generated asset, builder output

검증은 단순히 테스트 명령 하나가 아니라, 이 네 범주 중 무엇을 실제로 선택했는지 남기는 일이다. automation이 없으면 범위를 줄이는 게 아니라 manual/command 검증으로 메우고 residual risk를 남긴다.

즉 regression verification의 본질은 "무엇을 테스트했는가"보다 "무엇까지 확인해야 하는 change였는가"를 retained artifact로 명시하는 것이다.

## Build / Verify / Operate에 실제로 무엇을 적어야 하는가

### Build에는

- 구현 범위
- 변경된 runtime surface
- 사용한 builder / contract / asset
- 현재 사용자 관점 동작

### Verify에는

- 실행한 command 또는 retained check
- 검증한 regression surface
- proof / parity / schema / integration 근거
- residual risk

### Operate에는

- 실제 배포 여부
- 어떤 baseline이 live인지
- 어떤 검증으로 deploy를 통과시켰는지
- rollback 또는 follow-up 필요 여부

즉 build는 "상태 설명", verify는 "근거 설명", operate는 "실배포 상태 설명"이다.

## Rollout과 completion gate를 어떻게 해석해야 하는가

`sdd` 스킬은 rollout을 항상 강제하지 않는다. 하지만 rollout이 실제 범위에 들어오면 completion gate가 급격히 엄격해진다.

rollout이 범위일 때 보통 필요한 것은 다음이다.

- 최종 변경이 `main`에 있어야 함
- `origin/main` 또는 저장소 baseline에 push돼야 함
- DEV 배포 및 검증
- PROD가 범위면 PROD 배포 및 동일 검증
- 실패 시 rollback 또는 recovery 기록
- `sdd/05_operate` current-state 업데이트

즉 rollout이 범위가 아니면 operate는 비워둘 수 있지만, rollout이 범위가 되면 deploy evidence가 없으면 완료로 보기 어렵다.

## 완료 기준을 어떻게 봐야 하는가

이 스킬의 완료 기준은 "코드가 돌아간다"보다 강하다.

최소 완료 상태는 보통 다음과 같다.

- 관련 planning을 확인했음
- `sdd/02_plan`이 현재 작업 기준으로 갱신됨
- `sdd/03_build`가 구현 결과를 설명함
- `sdd/03_verify`가 검증 근거와 residual risk를 설명함
- rollout이 실제로 있었다면 `sdd/05_operate`도 갱신됨

추가로 아래 조건이 붙을 수 있다.

- screen 작업: visual fidelity + exactness + functional alignment 증거
- persistence 작업: schema parity evidence
- shared 영향 작업: widened regression evidence
- rollout 작업: DEV/PROD gate evidence

즉 완료 기준은 작업 종류에 따라 확장되며, `sdd` 스킬은 그 확장 조건을 문서로 남기게 만든다.

## Visual Fidelity, Exactness, 기능 정합성의 관계

세 개는 비슷해 보이지만 역할이 다르다.

- visual fidelity는 화면이 reference와 얼마나 시각적으로 정렬되는가의 문제다.
- exactness는 그 정렬을 얼마나 강한 근거로 증명할 수 있는가의 문제다.
- 기능 정합성은 화면 뒤의 동작과 계약이 실제 요구사항과 맞는가의 문제다.

예를 들어 화면이 visually 유사해도 API contract가 다르면 기능 정합성은 실패다. 반대로 동작은 맞아도 shell, spacing, copy, runtime tree가 spec과 다르면 visual fidelity는 실패다. `sdd` 스킬은 둘 중 하나만 맞는 상태를 완료로 보지 않으려는 구조다.

## 이 저장소에서 이 세 축을 담당하는 실제 구조

- toolchain inventory: `sdd/99_toolchain/01_automation/README.md`
- asset builder: `sdd/99_toolchain/01_automation/spec_asset_builder.py`
- asset recipe wrapper: `sdd/99_toolchain/01_automation/build_asset_recipes.py`
- screen spec generator: `sdd/99_toolchain/01_automation/build_screen_spec_pdf.py`
- capture tooling: `sdd/99_toolchain/01_automation/capture_screen_assets.mjs`
- verification harness baseline: `sdd/03_verify/10_test/verification_harness.md`
- verification strategy baseline: `sdd/02_plan/10_test/verification_strategy.md`
- regression scope baseline: `sdd/02_plan/10_test/regression_verification.md`

## 각 플로우를 더 자세히 설명하면

### Feature 플로우

기능 요구사항이 중심인 작업이다. 보통 feature spec을 확인하고, feature plan을 만들고, 구현 후 feature build와 feature verify를 갱신한다. 화면이 동반되더라도 핵심 변화가 기능 계약이면 feature 중심으로 정리한다.

### Screen 플로우

화면 구조, 카피, 상태, 네비게이션, 시각적 정렬이 중심인 작업이다. screen spec과 asset planning을 먼저 보고, 필요하면 builder를 통해 정적 자산과 디자인 기준을 확보한 뒤 구현한다. 이 플로우에서는 leaf component만 보는 것이 아니라 route, shell, shared component까지 포함한 top-down runtime tree가 중요하다. 또한 visual fidelity와 exactness는 단순 screenshot 비교가 아니라 source asset, generated asset, runtime tree, parity evidence를 함께 맞추는 구조로 본다.

### Architecture 플로우

폴더 구조, runtime boundary, governance, toolchain rule, shared pattern처럼 횡단적인 작업을 다룬다. 코드보다 문서 정렬과 구조 정리가 핵심이 될 수 있고, 이번에 갱신 중인 `toolchain_governance.md` 같은 문서가 여기에 속한다.

### Data / API / Integration 플로우

저장, 계약, 외부 연동이 핵심일 때 사용한다. 모델 정의, API shape, integration contract를 함께 보고, runtime과 deployed schema가 실제로 맞는지 확인하는 흐름이 중요하다. 특히 persistence 영향 작업은 migration head만으로 끝내지 않는 것이 핵심이다. 이 플로우는 functional alignment의 중심 축으로, UI가 맞아 보여도 계약이나 schema가 다르면 완료로 보지 않는다.

### Test / Verification 플로우

이 플로우는 "테스트 코드를 추가했다"보다 "어떤 검증 surface를 current-state로 보증하는가"에 초점이 있다. regression baseline을 먼저 잡고, automation이 없으면 그 gap 자체를 문서에 residual risk로 남긴다. visual fidelity, exactness, 기능 정합성은 모두 이 verify 플로우에서 retained evidence로 묶여야 한다.

### Operate / Rollout 플로우

배포가 실제 범위일 때만 활성화된다. `sdd` 스킬은 `sdd/05_operate` 폴더가 있다는 이유만으로 자동 배포를 요구하지 않는다. 다만 저장소 정책이 DEV rollout을 completion bar로 두거나 사용자가 명시적으로 배포를 요청하면, 그때는 deploy/verify/operate 기록이 완료 조건으로 올라간다.

## 이 스킬의 중요한 guardrail

- `sdd/`가 있으면 별도 `docs/` 트리를 만들지 않는다.
- planning review 없이 바로 코드부터 수정하지 않는다.
- build/verify/operate evidence를 채팅에만 남기지 않는다.
- 회귀 검수는 edited target-only로 끝내지 않는다.
- builder가 있는 정적 자산을 수동 redraw로 대체하지 않는다.
- local 테스트 통과만으로 schema parity를 가정하지 않는다.
- 배포가 실제 범위가 아니면 operate 문서를 허위로 채우지 않는다.
- rollout이 실제 범위라면 DEV gate와 PROD gate를 임의로 축소하지 않는다.
- visual fidelity는 leaf screenshot만이 아니라 runtime tree와 generated artifact까지 함께 본다.
- exactness는 subjective comment가 아니라 builder/harness/proof evidence로 남긴다.
- 기능 정합성은 mock 연결이나 local shadow state로 완료 처리하지 않는다.

## 자주 생기는 오해

- "문서만 잘 쓰면 된다"
  - 아니다. `sdd`는 코드, 계약, 검증, 운영 증거까지 같이 맞춰야 한다.
- "작은 수정이면 `sdd` 없이 해도 된다"
  - 아니다. current-state trail이 필요한 저장소면 작은 수정도 기본 원칙은 같다.
- "배포 문서 폴더가 있으니 항상 배포해야 한다"
  - 아니다. rollout은 explicit scope 또는 저장소 completion policy가 있을 때만 강제된다.
- "화면이 비슷하면 완료다"
  - 아니다. screen 작업은 functional alignment까지 맞아야 한다.
- "테스트 통과면 schema도 맞다"
  - 아니다. persistence 영향 작업은 real schema evidence가 별도 필요하다.

## 이 문서를 읽는 권장 순서

처음 보는 사람은 보통 아래 순서로 읽으면 된다.

1. 한 줄 정의
2. 언제 쓰는가
3. 전체 워크플로우
4. `sdd/` 폴더 구조 설명
5. Toolchain / fidelity / exactness / 기능 정합성
6. regression / schema parity / rollout / completion gate
7. 실제 정본 문서

## 이 저장소에서 바로 참고할 경로

- 정책 정본: `sdd/99_toolchain/02_policies/`
- automation inventory: `sdd/99_toolchain/01_automation/README.md`
- regression baseline: `sdd/02_plan/10_test/regression_verification.md`
- toolchain governance current-state: `sdd/02_plan/03_architecture/toolchain_governance.md`

## 이 문서의 성격

이 파일은 루트에서 빠르게 읽는 설명서다. 실제 강제 규칙, 예외, completion gate는 skill 원문, `AGENTS.md`, 그리고 `sdd/99_toolchain/02_policies/` 문서를 따른다.
