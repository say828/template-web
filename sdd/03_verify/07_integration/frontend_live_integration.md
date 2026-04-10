# frontend live integration verification

## Status

- pass

## Retained Checks

- service app split과 backend domain owner 매핑이 current integration baseline으로 유지된다.
- parity tooling reference path는 stable current path를 사용한다.
- `client/mobile/src/lib/useSpeechRecognitionInput.ts` shared utility가 template mobile build/typecheck에 포함된다.

## Residual Risk

- app별 adapter/contract path가 바뀌면 parity tooling 경로도 함께 갱신해야 한다.
- browser speech recognition support와 permission UX는 template utility만으로 보장되지 않으므로, 실제 consumer screen에서 별도 verify가 필요하다.
