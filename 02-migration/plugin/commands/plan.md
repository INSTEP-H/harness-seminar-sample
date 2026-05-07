# 마이그레이션 구현 계획서 작성

레거시 명세와 타겟 컨텍스트를 입력받아 구현 계획서를 작성한다. 이 단계가 전체 파이프라인의 품질을 가장 크게 좌우한다.

## 사용법

```
/mafia-migration:plan <module-id>
```

## 실행 방식

이 skill은 `migration-planner` sub-agent(**opus 모델**)에 위임된다.
설계 단계에서 모델 비용을 절감하지 않는 이유는 "설계는 고성능 모델, 구현은 효율 모델" 정책에 따른 것이다.

## 절차

1. 다음 산출물이 모두 존재하는지 확인한다. 없으면 선행 skill을 안내한다.
   - `.migration-artifacts/{module-id}/legacy-spec.md`
   - `.migration-artifacts/{module-id}/target-context.md`
2. **`migration-planner` sub-agent를 호출**하여 다음을 수행한다:
   - migration-policy의 `approach`에 따른 계획 작성 (1to1 vs redesign)
   - 데이터 모델 매핑 → 도메인 → 외부 계약 → UI → 인증 순으로 설계
   - legacy-spec의 모든 기능 체크리스트를 신규 파일/엔드포인트에 매핑
   - 선행조건·위험 요소·테스트 전략 명시
   - 결정 트레이드오프 정리
3. 초안과 함께 **결정 트레이드오프 / 위험 요소 / 선행조건**을 사용자에게 제시한다.
4. `migration-policy.review.human_signoff_required`가 true이면 사용자 승인 없이 implement 단계로 진행하지 않는다.
5. 사용자 피드백을 반영하여 확정한다.
6. 확정된 문서를 산출물 경로에 저장한다.

## 산출물 경로

```
.migration-artifacts/{module-id}/migration-plan.md
```

## 제약

- legacy-spec의 기능 체크리스트는 100% 매핑되어야 한다. 누락이 있으면 작성을 중단하고 사용자에게 보고한다.
- ADR/Convention 인용 시 id를 명시한다.
- 구현 디테일(변수명·로컬 분할)은 plan에 적지 않는다. plan은 구조·계약·매핑에 집중한다.
