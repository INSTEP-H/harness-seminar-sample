# Format (채널별 포맷 변환)

draft 본문을 brief에서 확정된 각 채널의 포맷 규칙에 맞게 변환한다.

## 사용법

```
/mafia-marketing:format <topic-slug>
```

## 실행 방식

각 채널별로 별도 sub-agent를 호출한다 (병렬 가능).
각 sub-agent는 자신의 채널 규칙만 받아 컨텍스트를 좁힌 채 작업한다.

## 절차

1. `.content-artifacts/{topic-slug}/draft.md`, `brief.md`가 존재하는지 확인한다.
2. brief의 `channels` 목록을 읽는다.
3. 각 채널에 대해 **sub-agent를 호출**하여 다음을 전달한다:
   - draft.md
   - channel-formats.yaml의 해당 채널 entry만
   - brand-voice.yaml의 forbidden / signature 섹션
4. 각 sub-agent는 다음을 수행한다:
   - `body.max_chars`를 초과하지 않도록 본문을 압축한다. 핵심 메시지는 절대 잃지 않는다.
   - `body.hook_first_line`이 true이면 첫 줄에 후크를 유지한다.
   - `hashtags`를 채널 규칙대로 부착한다 (max_count, placement).
   - `image`가 required이면 image 단계 산출물을 첨부 명시한다.
   - 채널별 특수 규칙(예: LinkedIn의 첫 3줄 노출, X의 thread 처리)을 적용한다.
5. 결과를 `formatted/{channel}.md`에 저장한다.
6. 모든 채널 완료 후 사용자에게 한꺼번에 제시한다.

## 산출물 경로

```
.content-artifacts/{topic-slug}/formatted/threads.md
.content-artifacts/{topic-slug}/formatted/x.md
.content-artifacts/{topic-slug}/formatted/linkedin.md
.content-artifacts/{topic-slug}/formatted/instagram.md
```

## 채널별 출력 구조

```markdown
# {channel display_name} — {topic-slug}

## 본문
{발행에 그대로 복사할 수 있는 형태}

## 첨부 이미지
- images/{channel}-1.{ext}

## 메타
- 글자 수: 287 / 500
- 해시태그 수: 4 / 5
- 후크 첫 줄: ✓
```

## 제약

- max_chars를 초과하지 않는다. 초과 시 sub-agent는 본문을 줄여 다시 작성한다.
- 핵심 메시지(brief.key_message)를 잃지 않는다. 길이 제약을 지키지 못하면 thread화(X) 또는 짧은 보조 글로 분할한다.
- 채널 간 본문이 100% 동일해서는 안 된다 (동일 컨텐츠로 인지되어 노출이 줄어드는 경향). 핵심 메시지는 보존하되 표현 디테일을 채널 톤에 맞춘다.
