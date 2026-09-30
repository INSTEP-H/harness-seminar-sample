---
name: seminar-migration-explore
description: 타겟 코드베이스의 컨벤션·관련 ADR·재사용 가능한 코드를 수집하여 target-context.md를 작성한다. migration-explorer sub-agent에 위임된다.
---

> 원저작: VIBE MAFIA CLUB (https://github.com/vibemafiaclub/harness-seminar-sample). 라이선스는 원본 README의 License 절(MIT) 그대로입니다. 아래 원문과 저작권 표기는 손대지 않았습니다. 컨벤져스 키트용으로 스킬 이름만 바꿔 옮겼습니다.

# 타겟 컨텍스트 수집

타겟 코드베이스의 컨벤션·관련 ADR·재사용 가능한 코드를 수집하여 참고 자료집을 작성한다.

## 인자

`<module-id>` — `docs/legacy-project.yaml`의 `modules[].id`.

## 실행 방식

이 skill은 `migration-explorer` sub-agent에 위임된다.

## 절차

1. `<module-id>`의 `legacy-spec.md`가 존재하는지 확인한다. 없으면 먼저 `specify` skill을 실행하라고 안내한다.
2. **`migration-explorer` sub-agent를 호출**하여 다음을 수행한다:
   - `target-conventions.yaml`에서 stacks/영역 기반 필터링
   - `target-adr.yaml`에서 stacks 1차 + context/decision 2차 판단으로 관련 ADR 추출
   - 신규 코드베이스에서 재사용 가능한 모듈·인프라·라이브러리 검색
   - 레거시 명세와 ADR이 부분 충돌하는 지점 정리
3. 초안과 함께 **충돌·모호 지점(C-)**을 사용자에게 제시한다.
4. 사용자 피드백을 반영하여 확정한다.
5. 확정된 문서를 산출물 경로에 저장한다.

## 산출물 경로

```
.migration-artifacts/{module-id}/target-context.md
```

## 제약

- 모든 추출 항목에 출처(파일 경로 또는 ADR id)를 명시한다.
- "비슷해 보이는" 정도의 모듈은 재사용 가능 항목으로 추천하지 않는다.
