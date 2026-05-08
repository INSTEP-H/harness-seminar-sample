---
name: draft
description: 확정된 brief를 입력받아 reels 프레임별 카피(F1 question / F2 question_full / F3 reading_body / F4 cta_text)를 작성한다.
---

# Draft (프레임별 카피)

## 사용

```
/draft <topic-slug>
```

## 실행 방식

이 skill은 `content-drafter` sub-agent에 위임된다.
브랜드 톤은 `plugin/CLAUDE.md`를 통해 항상 적용되며, 디테일은 brand-voice.yaml + reading-style.md를 참조한다.

## 절차

1. `.content-artifacts/{topic-slug}/brief.md`가 존재하는지 확인.
2. **`content-drafter` sub-agent 호출**:
   - brief, reels-templates의 해당 템플릿, brand-voice, content-adr, reading-style, tarot-cards를 읽는다.
   - 각 프레임의 text_slot을 모두 채운다.
   - F3 reading_body는 reading-style.md §2의 4단 구조(상태 호명 → 카드 의미 → 변화·조언 → 닫는 문장)로 작성. 250~320자.
   - 작성 후 self-check (reading-style.md §5).
3. 사용자에게 초안을 제시. 모호한 의도(톤 강도, 시그니처 사용 여부) 함께 묻는다.
4. 사용자 피드백 반영하여 확정.

## 산출물 경로

```
.content-artifacts/{topic-slug}/draft.md
```

## 제약

- 핵심 메시지는 brief.question_full과 일관되어야 한다. 임의 확장 금지.
- 이모지·강한 단정·점쟁이 클리셰·광고 직설 회피 (brand-voice + content-adr).
- text_slot의 max_chars (reels-templates.yaml) 초과 금지.
- self-check 항목을 모두 통과한 결과만 사용자에게 제시한다.
