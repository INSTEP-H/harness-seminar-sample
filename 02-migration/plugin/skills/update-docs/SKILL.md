---
name: update-docs
description: docs/legacy-project.yaml, migration-policy.yaml, target-conventions.yaml, target-adr.yaml 4개 yaml에 항목을 추가/수정/삭제한다. 인자로 대상 문서를 지정할 수 있다.
---

# 문서 업데이트 (legacy-project / migration-policy / target-conventions / target-adr)

`docs/`의 4개 yaml 파일에 항목을 추가/수정/삭제한다.

## 인자

- `legacy` — legacy-project.yaml (모듈 정의 등)
- `policy` — migration-policy.yaml (방침)
- `convention` — target-conventions.yaml
- `adr` — target-adr.yaml

인자 없이 호출하면 모든 문서를 함께 검토한다.

## 공통: 컨텍스트 분석 우선 원칙

어떤 문서를 업데이트하든, 지금까지의 작업 내용(특히 최근 마이그레이션 산출물)을 먼저 읽고 분석한다. **기존 문서 4개도 모두 먼저 읽고 분석해야 한다.**

1. `docs/legacy-project.yaml`, `docs/migration-policy.yaml`, `docs/target-conventions.yaml`, `docs/target-adr.yaml`을 모두 읽는다.
2. 현재 작업의 의사결정과 기존 항목을 대조하여 다음을 판단한다:
   - **충돌 항목**: 새 결정이 기존 항목과 모순되는가?
   - **연쇄 수정**: 한 문서의 변경이 다른 문서의 항목에도 영향을 미치는가?
     - 예: migration-policy의 `approach`를 redesign → 1to1로 바꾸면, target-adr의 일부 적용이 불가능해질 수 있음
     - 예: target-adr에 새 결정이 추가되면, target-conventions의 일부 항목이 폐기될 수 있음
   - **폐기 대상**: 이번 변경으로 더 이상 유효하지 않은 항목이 있는가?
3. 분석 결과 추가/수정/삭제할 항목을 사용자에게 **변경 제안 목록**으로 정리하여 제시한다.
   - MUST / RECOMMENDED 등급으로 나누어 제안.
4. 사용자가 최종 결정한 내용을 반영한다.

## legacy-project 업데이트 절차

1. `docs/legacy-project.yaml`을 읽고, 새로 발견한 모듈/screens를 추가한다.
2. 모듈 정의 시 다음 스키마를 따른다:
   ```yaml
   - id: {module-id}
     description: ...
     legacy_paths: [...]
     ui:
       screens:
         - name: {screen_name}
           path: {url-path}
   ```
3. `legacy_paths`가 다른 모듈과 겹치지 않는지 확인한다 (겹치면 어느 모듈 책임인지 명시).

## migration-policy 업데이트 절차

1. `docs/migration-policy.yaml`을 읽는다.
2. 변경하려는 정책 키(`approach`, `dead_code.policy`, `api_compatibility.preserve_external_contract` 등)가 기존 산출물에 끼치는 영향을 분석한다.
3. 영향이 있는 module은 plan을 다시 검토해야 함을 사용자에게 알린다.
4. 변경을 반영한다.

## target-conventions 업데이트 절차

1. `docs/target-conventions.yaml`을 읽는다.
2. `docs/target-adr.yaml`도 함께 읽고 충돌 여부를 확인한다.
3. 변경 제안 목록을 사용자에게 제시한다 (MUST / RECOMMENDED).
4. 사용자 요청에 따라 항목을 추가/수정/삭제한다.
5. 항목 작성 시 다음 스키마를 따른다:
   ```yaml
   - id: {카테고리}-{번호}    # GEN, TS, NEXT, MIG 등
     rule: ...
     stacks: [...]
   ```

## target-adr 업데이트 절차

1. `docs/target-adr.yaml`을 읽는다.
2. `docs/target-conventions.yaml`도 함께 읽고 모순되는 convention 규칙이 있는지 확인한다.
3. 변경 제안 목록을 사용자에게 제시한다.
4. 항목 작성 시 다음 스키마를 따른다:
   ```yaml
   - id: ADR-{번호}
     title: ...
     status: adopted | deprecated | superseded
     date: YYYY-MM-DD
     stacks: [...]
     context: |
       (구체적인 상황 서술 — 아래 가이드라인 참조)
     decision: ...
     consequence: ...
   ```
5. **context 작성 가이드라인:**
   - context만 읽고도 "왜 이 결정이 필요했는가"를 구체적으로 연상할 수 있어야 한다.
   - 나쁜 예: "에러 처리가 산발적이라 비일관적"
   - 좋은 예: "각 서비스에서 임의 형식으로 에러를 반환하고 있어 프론트엔드가 엔드포인트별 핸들러를 따로 작성해야 했고, 토스트 같은 공통 UI를 만들 수 없었다."
6. context가 불충분하다고 판단되면 사용자에게 구체화 방안을 요청한다.
7. 변경 내용을 사용자에게 확인받는다.
