---
name: pick-topic
description: 도메인 주제 풀에서 30일 내 미사용 + 바이럴 시그널이 좋은 주제 후보를 추려 사용자에게 제시한다. 사용자가 고른 주제를 topic-history에 기록한다.
---

# Pick Topic

발행할 주제를 선정하는 skill.
중복 주제로 인한 팔로워 피로(ADR-004)를 방지하기 위해 직전 30일 발행 이력을 자동으로 회피한다.

## 사용

```
/pick-topic
```

## 실행 방식

이 skill은 `topic-curator` sub-agent에 위임된다.

## 절차

1. **`topic-curator` sub-agent 호출**:
   - `docs/domain-knowledge/topic-pool.yaml` 읽기
   - `docs/topic-history.yaml` 읽기
   - 30일 쿨다운 필터 적용 (ADR-004)
   - 무작위 셔플 후 viral_signals 점수로 정렬
   - 상위 3~5개 후보 제시
2. 사용자에게 후보를 제시하고 선택받는다.
3. `topic-slug`을 함께 결정한다 (default: `{YYYY-MM-DD}-{topic-id}`).
4. `.content-artifacts/{topic-slug}/topic.md`에 결과 저장.
5. `docs/topic-history.yaml`에 append.

## 산출물 경로

```
.content-artifacts/{topic-slug}/topic.md
```

## 제약

- 직전 30일 사용된 topic_id를 default로 추천하지 않는다.
- 사용자가 강제로 동일 주제를 선택할 경우 명시적 override가 필요하다.
- topic-pool에 등록되지 않은 임의 주제를 추천하지 않는다 (사용자가 직접 추가하려면 `update-docs pool`을 안내한다).
