---
name: implement
description: 확정된 migration-plan을 그대로 구현한다. sonnet 모델 기반 migration-implementer sub-agent에 위임된다. plan 항목이 많으면 도메인 단위로 분할 호출한다.
---

# 구현

확정된 migration-plan을 그대로 구현한다.

## 인자

`<module-id>` — `docs/legacy-project.yaml`의 `modules[].id`.

## 실행 방식

이 skill은 `migration-implementer` sub-agent(**sonnet 모델**)에 위임된다.
plan의 "모듈 구조" 항목 수가 5개를 초과하는 등 분량이 큰 경우, 도메인 단위로 sub-agent를 추가 분할한다.

## 절차

1. `.migration-artifacts/{module-id}/migration-plan.md`가 존재하고 사용자 승인을 받은 상태인지 확인한다.
2. plan의 "모듈 구조" 섹션을 읽고, 분할 전략을 결정한다.
   - 5개 이하면 단일 implementer로 진행
   - 5개 초과면 도메인 단위(데이터 → 도메인 → API → UI 등)로 분할
3. 각 implementer sub-agent를 순차 또는 병렬로 호출한다. 각 sub-agent에는 다음만 전달한다:
   - 담당할 파일/구간
   - target-context.md
   - 해당 구간에 관련된 plan의 일부
4. 각 sub-agent 종료 후 lint/type-check 결과를 받는다. 실패가 있으면 즉시 동일 sub-agent에 수정 작업을 추가 위임한다.
5. plan과 다르게 구현해야 하는 사유가 발견되면 즉시 멈추고 사용자에게 보고한다 (plan 단계로 회귀 가능).
6. 모든 구현이 완료되면 변경 파일 목록을 사용자에게 보고한다.

## 산출물

- 타겟 코드베이스의 코드 변경
- (선택적) `.migration-artifacts/{module-id}/implementation-notes.md` — plan 대비 의도된 차이가 있을 경우만

## 제약

- legacy 소스를 절대 수정하지 않는다.
- plan에 없는 새 ADR/컨벤션을 만들지 않는다. 새 결정이 필요하면 멈추고 보고한다.
- 컴파일 오류·타입 오류·lint 오류가 남은 채로 완료 보고하지 않는다.
- 명세 체크리스트를 직접 검증하지 않는다. verify 단계의 책임이다.
