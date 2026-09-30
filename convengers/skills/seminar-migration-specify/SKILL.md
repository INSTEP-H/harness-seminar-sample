---
name: seminar-migration-specify
description: 레거시 코드를 read-only로 분석하여 기능 명세(legacy-spec.md)와 유스케이스 문서(use-cases.md)를 작성한다. migration-specifier sub-agent에 위임된다.
---

> 원저작: VIBE MAFIA CLUB (https://github.com/vibemafiaclub/harness-seminar-sample). 라이선스는 원본 README의 License 절(MIT) 그대로입니다. 아래 원문과 저작권 표기는 손대지 않았습니다. 컨벤져스 키트용으로 스킬 이름만 바꿔 옮겼습니다.

# 레거시 명세 추출

레거시 코드를 read-only로 분석하여 두 가지 산출물을 작성한다:

- `legacy-spec.md` — 외부 계약·도메인 규칙·데이터 모델·UI·외부 의존을 망라한 narrative 명세
- `use-cases.md` — 사용자 관점의 유스케이스 표 + 상세. **검증 단계가 그대로 가져다 쓰는 기준 문서**

## 인자

`<module-id>` — `docs/legacy-project.yaml`의 `modules[].id`.

## 실행 방식

이 skill은 `migration-specifier` sub-agent에 위임된다.

## 절차

1. `<module-id>`가 `docs/legacy-project.yaml`의 `modules[].id`에 존재하는지 확인한다.
2. **`migration-specifier` sub-agent를 호출**하여 다음을 수행한다:
   - 레거시 paths의 모든 소스를 읽고 외부 계약·도메인 규칙·데이터 모델·UI 동작·외부 의존을 추출
   - 추출한 내용을 narrative spec(`legacy-spec.md`)으로 정리
   - 모든 사용자 관점 행위를 유스케이스(UC-001, UC-002, ...)로 쪼개 `use-cases.md`로 정리
   - 코드만으로는 의도가 모호한 지점은 별도 섹션에 정리
3. 두 초안과 함께 **모호한 지점(Q-)**을 사용자에게 제시한다.
4. 사용자 피드백을 반영하여 확정한다.
5. 확정된 두 문서를 산출물 경로에 저장한다.

## 산출물 경로

```
.migration-artifacts/{module-id}/legacy-spec.md
.migration-artifacts/{module-id}/use-cases.md
```

## 제약

- 레거시 소스는 read-only. 절대 수정하지 않는다.
- 사용처가 보이지 않는 코드도 일단 명세에 포함한다 ("사용처 미확인" 표기).
- `use-cases.md`의 UC-ID는 verify 단계와 1:1 매핑된다. 한 번 부여한 ID는 변경하지 않는다.
- legacy-spec과 use-cases는 같은 사실을 다른 관점으로 본 문서다. 서로 모순되어선 안 된다.
