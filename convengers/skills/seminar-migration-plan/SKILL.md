---
name: seminar-migration-plan
description: 레거시 명세·유스케이스·타겟 컨텍스트를 입력받아 마이그레이션 구현 계획서(mermaid 다이어그램 포함)를 작성한다. opus 모델 기반 migration-planner sub-agent에 위임된다.
---

> 원저작: VIBE MAFIA CLUB (https://github.com/vibemafiaclub/harness-seminar-sample). 라이선스는 원본 README의 License 절(MIT) 그대로입니다. 아래 원문과 저작권 표기는 손대지 않았습니다. 컨벤져스 키트용으로 스킬 이름만 바꿔 옮겼습니다.

# 마이그레이션 구현 계획서 작성

레거시 명세, 유스케이스, 타겟 컨텍스트를 입력받아 구현 계획서를 작성한다. 이 단계가 전체 파이프라인의 품질을 가장 크게 좌우한다.

## 인자

`<module-id>` — `docs/legacy-project.yaml`의 `modules[].id`.

## 실행 방식

이 skill은 `migration-planner` sub-agent(**opus 모델**)에 위임된다.
설계 단계에서 모델 비용을 절감하지 않는 이유는 "설계는 고성능 모델, 구현은 효율 모델" 정책에 따른 것이다.

## 절차

1. 다음 산출물이 모두 존재하는지 확인한다. 없으면 선행 skill을 안내한다.
   - `.migration-artifacts/{module-id}/legacy-spec.md`
   - `.migration-artifacts/{module-id}/use-cases.md`
   - `.migration-artifacts/{module-id}/target-context.md`
2. **`migration-planner` sub-agent를 호출**하여 다음을 수행한다:
   - migration-policy의 `approach`에 따른 계획 작성 (1to1 vs redesign)
   - 데이터 모델 매핑 → 도메인 → 외부 계약 → UI → 인증 순으로 설계
   - **use-cases.md의 모든 UC를 신규 파일/엔드포인트에 매핑**
   - 선행조건·위험 요소·테스트 전략 명시
   - 결정 트레이드오프 정리
   - **mermaid 다이어그램 3종 필수 작성**: 아키텍처(graph), 데이터 흐름(sequence), 모듈 의존성(graph)
3. 초안과 함께 **결정 트레이드오프 / 위험 요소 / 선행조건**을 사용자에게 제시한다.
4. `migration-policy.review.human_signoff_required`가 true이면 사용자 승인 없이 implement 단계로 진행하지 않는다.
5. 사용자 피드백을 반영하여 확정한다.
6. 확정된 문서를 산출물 경로에 저장한다.

## 산출물 경로

```
.migration-artifacts/{module-id}/migration-plan.md
```

## 제약

- use-cases.md의 모든 UC는 100% 매핑되어야 한다. 누락이 있으면 작성을 중단하고 사용자에게 보고한다.
- ADR/Convention 인용 시 id를 명시한다.
- 구현 디테일(변수명·로컬 분할)은 plan에 적지 않는다. plan은 구조·계약·매핑에 집중한다.
- mermaid 다이어그램은 텍스트로 명확히 읽을 수 있어야 한다. 노드명에 한글 가능, 화살표 라벨에 호출 의미 명시.
