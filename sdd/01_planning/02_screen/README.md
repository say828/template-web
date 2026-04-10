# Screen Planning

## Naming

- Folder name: `02_screen`
- Canonical artifact: `{service}_screen_spec.pdf`
- Source-of-truth screen spec files are service based.

## Code Rule

- Screen code format: `{SERVICE}-S{NNN}`
- 각 segment는 고정 길이로 유지한다.

| Segment | Rule | Example |
| --- | --- | --- |
| `SERVICE` | 3-letter uppercase service code | `WEB`, `ADM`, `MOB`, `LND` |
| `TYPE` | screen 식별자 고정값 | `S` |
| `NNN` | 3-digit sequence | `001`, `002` |

## Canonical Output

- [web_screen_spec.pdf](./web_screen_spec.pdf)
- [admin_screen_spec.pdf](./admin_screen_spec.pdf)
- [mobile_screen_spec.pdf](./mobile_screen_spec.pdf)
- [landing_screen_spec.pdf](./landing_screen_spec.pdf)

## Rule

- screen spec은 서비스 surface 기준 산출물이다.
- route, UI block, CTA, interaction, transition은 screen spec PDF 안에서 관리한다.
- build source, capture asset, generator는 `sdd/99_toolchain/01_automation` 아래에 둔다.
- reusable asset planning 산출물은 `sdd/01_planning/02_screen/assets/` 아래에 둔다.
- data 모델링 상세는 `04_data`에서 다루고, architecture/system boundary는 `03_architecture`에서 다룬다.
- screen spec에서 파생되는 로고/일러스트 등 재사용 자산은 generic asset recipe generator로 재생성 가능해야 한다.

## Toolchain

- generic asset recipe generator (`스펙에셋빌더`): [`spec_asset_builder.py`](../../99_toolchain/01_automation/spec_asset_builder.py)
- compatibility wrapper: [`build_asset_recipes.py`](../../99_toolchain/01_automation/build_asset_recipes.py)
- example recipe manifest: [`asset_recipe_manifest.example.py`](../../99_toolchain/03_templates/asset_recipe_manifest.example.py)
- asset planning root example: [`assets/README.md`](assets/README.md)
