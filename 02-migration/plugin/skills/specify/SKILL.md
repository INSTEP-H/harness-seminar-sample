---
name: specify
description: 레거시 코드를 read-only로 분석하여 기능 명세(legacy-spec.md)를 작성한다. migration-specifier sub-agent에 위임된다.
---

# 레거시 명세 추출

레거시 코드를 read-only로 분석하여 기능 명세(작업 명세서)를 작성한다.

## 인자

`<module-id>` — `docs/legacy-project.yaml`의 `modules[].id`.

## 실행 방식

이 skill은 `migration-specifier` sub-agent에 위임된다.

## 절차

1. `<module-id>`가 `docs/legacy-project.yaml`의 `modules[].id`에 존재하는지 확인한다.
2. **`migration-specifier` sub-agent를 호출**하여 다음을 수행한다:
   - 레거시 paths의 모든 소스를 읽고 외부 계약·도메인 규칙·데이터 모델·UI 동작·외부 의존을 추출
   - 발견된 기능을 verify에서 그대로 쓸 수 있는 체크리스트 형태로 정리
   - 코드만으로는 의도가 모호한 지점은 별도 섹션에 정리
3. 초안과 함께 **모호한 지점(Q-)**을 사용자에게 제시한다.
4. 사용자 피드백을 반영하여 확정한다.
5. 확정된 문서를 산출물 경로에 저장한다.

## 산출물 경로

```
.migration-artifacts/{module-id}/legacy-spec.md
```

## 제약

- 레거시 소스는 read-only. 절대 수정하지 않는다.
- 사용처가 보이지 않는 코드도 일단 명세에 포함한다 ("사용처 미확인" 표기).
