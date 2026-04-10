# templates

제품으로 바로 수렴 가능한 client/server 템플릿 모음이자 downstream 저장소가 그대로 복제하는 canonical template repo다.

포함 템플릿:

- [landing](./client/landing): 마케팅/브랜드 랜딩 패턴
- [web](./client/web): 일반 제품형 웹 앱 shell, dashboard/list/detail 패턴
- [mobile](./client/mobile): 다국어/현장 업무형 모바일 IN workspace 패턴
- [admin](./client/admin): 운영 콘솔형 shell, sidebar/topbar/drawer/table 패턴
- [server](./server): HTTP 기반 hexagonal/DDD 서버 패턴

공통 원칙:

- 프론트엔드는 `pnpm workspace + React + Vite + Tailwind` 기반
- `shadcn/ui-style` primitive를 직접 포함
- 제품 DOM은 유지하고, 스타일 조정값은 `theme.ts` + CSS custom properties로 노출
- proof/spec 전용 DOM 복제 대신 fixture data + parameter surface로 정렬
- `server`는 hexagonal architecture 기준으로 `contracts + application + domain + infrastructure`를 사용
- `landing`, `web`, `mobile`, `admin`은 실제 `/api/v1/auth/login`과 `/api/v1/auth/me`를 사용하는 기준 템플릿이다.
- runtime baseline은 루트 `compose.yml`을 기준으로 유지하고, 여기서 4개 frontend surface, `server`, 기본 `postgres`, optional DB profile을 함께 올린다.
- agentic baseline은 `.claude`, `.codex`, `.agent`를 함께 유지하고 downstream repo가 role agent, skill alias, Ralph harness를 그대로 가져가도록 설계한다.
- `sdd/03_build`는 단순 구현 목록이 아니라 실제 runtime assembly를 따라 읽는 AST-style current-state 설명을 기준으로 유지한다.

SDD / delivery 원칙:

- 설계, 계획, 구현, 검증, 운영 문서는 모두 `sdd/`가 canonical root다.
- `sdd/`는 history 누적이 아니라 current-state durable 문서만 유지한다.
- `02_plan`은 에이전트의 현재 개발 계획을 관리하고, feature는 `<domain>_todos.md`, screen은 `<service>_todos.md`로 유지한다.
- retained verification summary는 `sdd/03_verify`를 canonical root로 사용한다.
- 템플릿 runtime baseline은 root `compose.yml` dev-focused stack이고, dedicated host용 DEV(개발계)/PROD compose overlay는 `infra/compose/`에 둔다.
- current canonical delivery split은 `AWS edge/domain -> OpenStack backend compute -> AWS data plane`이다.
- DEV(개발계) 반영이 필요한 작업은 `build -> main push -> DEV deploy -> DEV verify` 순서를 기본으로 사용한다.

문서:

- [UI Contract Projection](./sdd/99_toolchain/01_automation/ui-contract-projection.md): 스킬/CLI 공통 projection 계약
- [Infra Compose](./infra/compose/README.md): root compose baseline과 dedicated DEV(개발계)/PROD compose overlay
- [Terraform Layout](./infra/terraform/README.md): provider-first canonical infra layout
- [OpenStack Terraform](./infra/terraform/openstack/README.md): OpenStack compute baseline
- [AST Build Governance](./sdd/02_plan/03_architecture/build_ast_runtime_tree_governance.md): `sdd/03_build` runtime-tree governance

설치형 scaffold:

```bash
npx agentic-dev init my-app --template web
cd my-app
cp .env.example .env
npm install -g pnpm
pnpm install
cd client/web
npx playwright install chromium
npm run ui:parity:bootstrap
```

설치 프로세스:

1. `npx agentic-dev init my-app --template web`
   - `client/web`와 함께 `server`, `.claude`, `.codex`, `.agent`, `sdd`, `infra`, `scripts`를 scaffold한다.
2. `cp .env.example .env`
   - 로컬 runtime 기본 환경값을 준비한다.
3. `pnpm install`
   - workspace dependency를 설치한다.
4. `cd client/web && npx playwright install chromium`
   - parity/proof에서 사용하는 브라우저를 설치한다.
5. `npm run ui:parity:bootstrap`
   - 첫 parity bootstrap을 실행한다.

CLI가 하는 일:

- 선택한 frontend template 하나를 `client/<template>`로 설치
- `server`, `.claude`, `.codex`, `.agent`, `sdd`, `infra`, `scripts`를 함께 설치
- 선택한 template에 맞게 `compose.yml`, `pnpm-workspace.yaml`, `repo-contract.json`을 정렬

Parity 명령:

- `npm run ui:parity:init`
  - repo contract alias, parity contract, route-gap 산출물을 초기화한다.
- `npm run ui:parity:bootstrap`
  - `init -> build -> preview -> materialize reference -> plan_audit gate -> proof gate`를 한 번에 실행한다.
- `npm run ui:parity:proof`
  - 기존 parity contract를 기준으로 proof만 다시 실행한다.

주요 parity 산출물:

- contract: `sdd/02_plan/10_test/templates/ui_parity_web_contract.yaml`
- route-gap report: `sdd/02_plan/99_generated/from_planning/ui_parity/`
- verification summary: `sdd/03_verify/10_test/ui_parity/`
- preview log: `sdd/03_verify/10_test/ui_parity/web-preview.log`

GitHub token 운영:

- 실제 token 값은 repo 파일에 저장하지 않는다.
- GitHub CLI나 자동화는 `GH_TOKEN` 또는 별도 wrapper가 있다면 `AGENTIC_GITHUB_TOKEN` 같은 환경변수에서 읽도록 운영한다.
- 이미 대화나 로그에 노출된 token은 재사용하지 않고 즉시 폐기 후 새로 발급하는 것이 맞다.


개발용 compose baseline:

```bash
cp .env.example .env
docker compose up --build
```

기본 compose 포트:

- `client/landing`: `3000`
- `client/web`: `3001`
- `client/mobile`: `3002`
- `client/admin`: `4000`
- `server/http`: `8000`

기본 로그인 계정:

- `admin@example.com` / `<CHANGE_ME>`
- `operator@example.com` / `<CHANGE_ME>`

DB adapter 전환:

- 기본: `SERVER_DATABASE_BACKEND=postgres`
- 선택 가능: `postgres`, `mysql`, `mariadb`, `mongodb`, `memory`
- optional DB 컨테이너는 compose profile로 포함돼 있다:
  - `docker compose --profile mysql up --build`
  - `docker compose --profile mariadb up --build`
  - `docker compose --profile mongo up --build`

Agentic baseline:

- `.claude/agents/`: Claude role agent prompt surface
- `.claude/skills/sdd`: Claude SDD canonical skill
- `.codex/skills/SKILL.md`: Codex root skill index
- `.codex/skills/sdd/`: Codex SDD canonical skill
- `.agent/ralph.sh`, `.agent/ralph-supervisor.sh`: bounded Ralph loop runner
