---
name: verify
description: 구현 결과를 use-cases.md 기준으로 검증하고, 유스케이스별 ✅/❌/⚠️ 표 + 특이사항 + 최종 보고서를 생성한다. migration-verifier sub-agent에 위임되며 사용자 확인 없이 자동 실행된다.
---

# 검증

구현 결과를 (a) **use-cases.md 기준 유스케이스 검증**과 (b) 시각 회귀로 검증한다. 규칙 기반 단순 비교만 수행하고, 모호한 차이의 최종 판단은 사람에게 위임한다.

## 인자

`<module-id>` — `docs/legacy-project.yaml`의 `modules[].id`.

## 실행 방식

이 skill은 `migration-verifier` sub-agent에 위임되며, **사용자 확인 없이 자동으로 실행된다.**

## 절차

1. 다음 산출물이 모두 존재하는지 확인한다.
   - `.migration-artifacts/{module-id}/legacy-spec.md`
   - `.migration-artifacts/{module-id}/use-cases.md`
   - `.migration-artifacts/{module-id}/migration-plan.md`
2. **`migration-verifier` sub-agent를 호출**하여 다음을 수행한다:

### (a) 유스케이스 기반 검증

- `use-cases.md`의 요약 표를 그대로 가져와 verification-report.md의 최상단 표로 사용한다.
- 각 UC에 대해 plan의 "유스케이스 매핑"을 참고하여 담당 파일/엔드포인트를 식별한다.
- 가능한 검증을 수행하고 다음 셋 중 하나로 표시한다:
  - **✅** — 정상 구현. 검증 근거 보유.
  - **❌** — 미구현·기능 결손·명백한 버그. 검증 근거 보유.
  - **⚠️** — 사용자 확인 필요. 차이는 있으나 의도된 변경일 가능성, 또는 검증 환경 부재.
- 비고 칸에는 상태가 ❌·⚠️인 경우 **간결한 사유**를 적는다 (한 줄).
- 상태가 ❌이거나 ⚠️인 항목은 "특이사항" 섹션에 상세 분석을 추가한다.

### (b) 시각 회귀 (UI 모듈 한정)

`legacy-project.yaml`의 module에 `ui.screens`가 있고 `migration-policy.testing.visual_regression`이 `required_for_ui`인 경우만 수행.

- 레거시·신규 시스템에서 동일 화면을 캡처하고 diff(%)를 계산한다.
- `visual_diff_threshold_pct`를 초과하면 해당 UC를 ❌(또는 ⚠️ — 디자인 변경 의도가 plan에 명시된 경우)로 표시한다.

3. `verification-report.md`를 산출물 경로에 저장한다.
4. ❌가 있는 경우 사용자에게 강조해서 보고한다. 그렇지 않으면 PASS 요약만 보고한다.

## 산출물 경로

```
.migration-artifacts/{module-id}/verification-report.md
```

## 제약

- 임의로 코드를 수정하지 않는다. 검증만 수행한다.
- 검증 도구·데이터셋이 없으면 임의 추론 PASS를 내리지 않는다. ⚠️로 분류하고 부재 사유를 비고에 기록한다.
- "통과로 보임" 같은 모호한 판정을 내리지 않는다. ✅는 검증 근거가 있을 때만 사용한다.
- **최종 판단(의도된 변경인지 vs 진짜 회귀인지)은 사람의 책임이다.** verifier는 차이만 정확히 보고한다.
- use-cases.md의 UC-ID는 그대로 보존한다 (변경 금지).
