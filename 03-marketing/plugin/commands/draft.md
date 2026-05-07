# Draft (본문 초안)

확정된 brief를 입력받아 채널 무관 단일 본문 초안을 작성한다.

## 사용법

```
/mafia-marketing:draft <topic-slug>
```

## 실행 방식

이 skill은 sub-agent에 위임하여 실행한다.
브랜드 톤은 plugin/CLAUDE.md를 통해 항상 적용되며, 추가 디테일은 brand-voice.yaml에서 참조한다.

## 절차

1. `.content-artifacts/{topic-slug}/brief.md`가 존재하는지 확인한다.
2. **sub-agent를 호출**하여 다음을 수행한다:
   - brief, brand-voice.yaml, content-adr.yaml을 읽는다.
   - 채널 무관 단일 본문(약 600자 이내)을 작성한다. 채널별 변환은 format 단계의 책임.
   - 후크 → 본론 → CTA 순으로 구성한다.
   - 시그니처 표현(brand-voice.signature_phrasings) 활용을 적극 검토한다.
   - 작성 후 self-check: brand-voice.forbidden 항목을 모두 회피했는가?
3. 초안을 사용자에게 제시한다. 모호한 의도(예: 후크 강도, 시그니처 사용 여부)를 함께 묻는다.
4. 사용자 피드백을 반영하여 확정한다.

## 산출물 경로

```
.content-artifacts/{topic-slug}/draft.md
```

## 문서 구조

```markdown
# Draft — {topic-slug}

## 본문 (단일, 채널 무관)
{후크 첫 줄}

{본론}

{CTA}

## 작성 메모
- 사용한 시그니처 표현: ...
- 후크 강도: 강 / 중 / 약
- 톤 검증 self-check: PASS / 의문점

## 대안 후크 (선택)
- 더 약한 버전: ...
- 더 강한 버전: ...
```

## 제약

- 핵심 메시지는 brief의 `key_message`와 동일해야 한다. 임의 확장 금지.
- 이모지를 절대 사용하지 않는다 (content-adr ADR-001).
- CTA는 본문 마지막에만 배치한다 (content-adr ADR-003).
- 첫 줄은 도발형 후크여야 한다 (content-adr ADR-002).
- 브랜드명 표기는 공식 표기 3종(바이브마피아클럽, VIBE MAFIA CLUB, VMC) 중에서만 사용한다 (content-adr ADR-004).
