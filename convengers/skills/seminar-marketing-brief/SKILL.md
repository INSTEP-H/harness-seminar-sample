---
name: seminar-marketing-brief
description: 선정된 주제로 발행할 릴스의 frame_template, card_concept, selected_card_index, CTA, BGM 사용 여부를 사용자와 함께 확정한다. 작업 명세서를 만든다.
---

> 원저작: VIBE MAFIA CLUB (https://github.com/vibemafiaclub/harness-seminar-sample). 라이선스는 원본 README의 License 절(MIT) 그대로입니다. 아래 원문과 저작권 표기는 손대지 않았습니다. 컨벤져스 키트용으로 스킬 이름만 바꿔 옮겼습니다.

# Brief (작업 명세서)

선정된 주제 위에 이번 릴스의 구체 디테일을 확정한다.

## 사용

```
/brief <topic-slug>
```

## 실행 방식

메인 컨텍스트에서 사용자와 직접 대화하며 진행한다 (sub-agent 위임 없음).
"에이전트가 이해 못 하는 부분이 있으면 사용자에게 질문하라"는 Clarify 원칙을 강하게 적용한다.

## 절차

1. `.content-artifacts/{topic-slug}/topic.md`가 존재하는지 확인.
2. 다음 항목을 모두 확정할 때까지 사용자에게 질문한다:
   - **frame_template**: 기본 `pick-a-card`. reels-templates.yaml에 등록된 다른 id를 쓰려면 사용자가 명시.
   - **question / question_full**: topic.md의 값을 default로 채우되 사용자가 다듬을 수 있음.
   - **card_concept**: 5장 미리보기 비주얼 분류 (default: 길/물가/꽃/실내/도시 — visual-style.md). 다른 분류 원하면 5개 명시.
   - **selected_card_index**: F3에 reveal될 카드 번호 (1~5). 비워 두면 draft 단계에서 narrative에 가장 잘 맞는 카드를 sub-agent가 선택.
   - **selected_card_meaning**: 그 카드의 타로 카드 의미 (예: The Star). draft가 reading-style에 맞춰 풀어 씀.
   - **cta_intent**: 댓글 트리거 / DM 트리거 중 어느 쪽인지.
   - **bgm**: 기본은 `docs/bgm-pool.yaml`의 `enabled: true` 항목 중 **무작위 1곡 자동 선택**.
     사용자가 곡을 명시한 경우에만 그 값을 우선한다. silent를 원하면 사용자가 명시적으로 `bgm: none`이라고 말해야 한다.
     자동 선택 시 후보군을 사용자에게 보여주고 묻지 않는다 — 그냥 골라 진행한다.
3. 모호한 지점을 사용자에게 다시 던진다. 예:
   - "card_concept을 '길/물가/꽃/실내/도시'로 갈까요, 아니면 다른 결로 만들어볼까요?"
   - "selected_card_index를 미리 정할지, draft에서 자연스럽게 정해지게 둘지?"
4. `brief.md`를 작성한다.

## 산출물 경로

```
.content-artifacts/{topic-slug}/brief.md
```

## 문서 구조

```markdown
# Brief — {topic-slug}

## 주제
- topic_id: love-secret-admirer
- question: 요즘 티 안내고 나를 좋아하는 사람
- question_full: 몰래 날 좋아하는 사람, 직관적으로 끌리는 카드를 선택하세요

## 릴스 구성
- frame_template: pick-a-card
- card_concept: 풍경 (길/물가/꽃/실내/도시)
- selected_card_index: 3
- selected_card_meaning: The Star (정방향)

## CTA
- cta_intent: 댓글 트리거
- 예시 문구: "이 카드들의 해석은 댓글 남겨주시면 보내드릴게요"

## 오디오
- bgm:
    pool_id: santo-and-johnny-and-i-love-her       # docs/bgm-pool.yaml의 id
    title: And I Love Her
    artist: Santo & Johnny
    source_url: https://www.youtube.com/watch?v=EHQYAylvqIo
    hook: { start_sec: 60, duration_sec: 14, fade_in_sec: 0.8, fade_out_sec: 1.5 }
    volume_db: -18
- tts: 비활성

## 참고 / 금지
- 참고: ...
- 금지: ...

## 모호한 지점 (사용자 확인 완료)
- Q-1. ... → 결정: ...
```

## 제약

- 등록되지 않은 frame_template id를 사용하려 하면 거부하고 update-docs 안내.
- card_concept이 5분류로 떨어지지 않으면(예: 4분류) 거부하고 5개로 맞춰 달라고 요청.
- selected_card_index가 명시되면 1~5 범위 검증.
- brief 자체에는 본문 카피를 쓰지 않는다 (draft의 책임).
