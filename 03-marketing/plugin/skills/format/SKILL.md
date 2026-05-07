---
name: format
description: reels와 instagram 캡션을 채널 규칙에 맞게 변환·정리한다. reels는 프레임 시퀀스 메타, instagram은 피드 캡션 본문/해시태그를 산출한다.
---

# Format (채널별 변환)

## 사용

```
/format <topic-slug>
```

## 실행 방식

reels 채널과 instagram 캡션 두 산출물을 만든다. 단순 변환이 많아 메인 컨텍스트에서 처리하거나, 각각 sub-agent로 위임할 수 있다.

## 절차

1. `.content-artifacts/{topic-slug}/draft.md`, `brief.md`, `images/composed/`가 모두 존재하는지 확인.
2. **reels.md 작성**:
   - reels-templates의 프레임별 `duration_sec`을 default로 사용. brief에 사용자 조정값이 있으면 우선.
   - 총 길이가 channel-formats.reels.duration_sec_total_max(default 18) 이하인지 확인. 초과 시 호출자에게 보고.
   - 합성 프레임 경로, BGM 경로, TTS 사용 여부를 메타로 포함.
3. **instagram.md 작성**:
   - draft의 F1 question + F3 reading_body 일부 발췌를 캡션 본문 후크로 사용 (첫 125자 안에 후크 + 카드 선택 안내).
   - 본문 max_chars 2200 이하로 작성.
   - 해시태그를 end_of_post에 부착 (max 30개). 도메인 + 카테고리(brief.category 기반) + 일반 운세 태그 조합.
4. 두 산출물을 사용자에게 묶어서 제시.

## 산출물 경로

```
.content-artifacts/{topic-slug}/formatted/reels.md
.content-artifacts/{topic-slug}/formatted/instagram.md
```

## reels.md 구조

```markdown
# Reels — {topic-slug}

## 프레임 시퀀스
| n | role | duration | frame file |
|---|---|---|---|
| 1 | hook | 2.5s | images/composed/frame-1.png |
| 2 | selection | 3s | images/composed/frame-2.png |
| 3 | reveal | 6s | images/composed/frame-3.png |
| 4 | cta | 2.5s | images/composed/frame-4.png |

## 총 길이
14.0s (max 18s)

## 오디오
- bgm: ~/Music/calm-piano-loop.mp3 (-18dB)
- tts: 비활성

## 메타
- aspect_ratio: 9:16
- canvas: 1080x1920
- frame_template: pick-a-card
```

## instagram.md 구조

```markdown
# Instagram Caption — {topic-slug}

## 본문
{후크 첫 줄 — F1 question 변형}

{본문 — F3 reading_body 일부 + 안내 문구}

{CTA — F4 cta_text와 동일 의도, 캡션 어조에 맞게 다듬음}

## 해시태그
#타로 #오늘의운세 #카드뽑기 #감성타로 #...

## 메타
- 글자 수: 1284 / 2200
- 해시태그 수: 18 / 30
- 후크 첫 줄: ✓ (125자 안에 위치)
```

## 제약

- max_chars / max_count를 초과하지 않는다.
- 캡션 본문이 reels 영상의 메시지와 어긋나지 않게 한다 (reading_body의 일부를 활용).
- 광고 직설 표현 금지 (ADR-002).
- reels.md의 duration_sec_total은 channel-formats의 max를 초과하지 않는다.
