---
name: auto
description: 마이그레이션 파이프라인 전체를 오케스트레이션한다. specify → explore → plan(opus) → implement(sonnet) → verify 순으로 진행한다.
---

# 마이그레이션 파이프라인

전체 마이그레이션 파이프라인을 오케스트레이션한다.

## 인자

`<module-id>` — `docs/legacy-project.yaml`의 `modules[].id`와 일치해야 한다.

## 사전 조건

- `docs/legacy-project.yaml`, `docs/migration-policy.yaml`, `docs/target-conventions.yaml`, `docs/target-adr.yaml`이 팀 상황에 맞게 작성되어 있어야 한다.
- `legacy-project.yaml`의 `path`가 가리키는 레거시 repo가 로컬에 존재해야 한다.

## 파이프라인

### Step 1: 상태 점검

1. 인자로 받은 `<module-id>`가 `legacy-project.yaml`의 `modules[].id`에 존재하는지 확인한다. 없으면 사용 가능한 module 목록을 보여주고 중단한다.
2. `legacy-project.yaml`의 `path`가 실제로 존재하는지 확인한다.
3. 사용자에게 다음을 요약해 보여준다:
   - module의 description, legacy_paths
   - migration-policy의 approach, api_compatibility, visual_regression 설정
   - base branch (기본: `main`)
4. `.migration-artifacts/{module-id}/` 디렉토리를 생성한다.

### Step 2: Specify (레거시 명세 추출)

1. **`migration-specifier` sub-agent를 호출**하여 `specify` skill을 실행한다.
2. sub-agent는 레거시 코드를 read-only로 분석하여 `legacy-spec.md` 초안을 작성한다.
3. 초안과 함께 **모호한 지점(Q-)**을 사용자에게 제시한다.
4. 사용자 피드백을 반영하여 `legacy-spec.md`를 확정한다.
5. 산출물을 `.migration-artifacts/{module-id}/legacy-spec.md`에 저장한다.

### Step 3: Explore (타겟 컨텍스트 수집)

1. **`migration-explorer` sub-agent를 호출**하여 `explore` skill을 실행한다.
2. sub-agent는 target-conventions, target-adr, 신규 코드베이스를 조회하여 `target-context.md` 초안을 작성한다.
3. 초안과 함께 **충돌·모호 지점(C-)**을 사용자에게 제시한다.
4. 사용자 피드백을 반영하여 `target-context.md`를 확정한다.
5. 산출물을 `.migration-artifacts/{module-id}/target-context.md`에 저장한다.

### Step 4: Plan (구현 계획서)

1. **`migration-planner` sub-agent를 호출**하여 `plan` skill을 실행한다. 이 sub-agent는 **opus 모델을 사용한다.**
2. sub-agent는 legacy-spec + target-context + migration-policy를 입력으로 받아 `migration-plan.md` 초안을 작성한다.
3. 초안과 함께 **결정 트레이드오프 / 위험 요소 / 선행조건**을 사용자에게 제시한다.
4. `migration-policy.review.human_signoff_required`가 true이면 **사용자 승인 없이 다음 단계로 진행하지 않는다.**
5. 사용자 피드백을 반영하여 `migration-plan.md`를 확정한다.
6. 산출물을 `.migration-artifacts/{module-id}/migration-plan.md`에 저장한다.

### Step 5: Implement (구현)

1. **`migration-implementer` sub-agent를 호출**하여 `implement` skill을 실행한다. 이 sub-agent는 **sonnet 모델을 사용한다.**
2. plan의 "모듈 구조" 항목 수가 많으면(권장: 5개 초과), 도메인 단위로 sub-agent를 추가 분할하여 병렬·순차 구현한다.
3. 각 구현 sub-agent는 작업 종료 후 lint/type-check 결과를 호출자에 보고한다.
4. plan과 다르게 구현해야 하는 사유가 발견되면 즉시 멈추고 사용자에게 보고한다 (Step 4로 회귀 가능).

### Step 6: Verify (검증)

1. **`migration-verifier` sub-agent를 호출**하여 `verify` skill을 실행한다.
2. sub-agent는 legacy-spec의 기능 체크리스트와 (UI 모듈인 경우) 시각 회귀를 모두 수행한다.
3. `verification-report.md`를 `.migration-artifacts/{module-id}/`에 저장한다.
4. **사용자 확인 없이 자동으로 진행한다.** 다만 FAIL이 있는 경우 결과를 사용자에게 강조해 보고한다.
5. FAIL 항목이 있으면 사용자에게 다음 옵션을 제시한다:
   - implementer를 다시 호출하여 수정
   - 의도된 차이로 판정하고 plan에 기록한 뒤 종료

### 완료

파이프라인이 완료되면 산출물 경로의 전체 파일 목록과 verify 최종 상태를 사용자에게 보고한다.
