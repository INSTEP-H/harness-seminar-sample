---
name: image
description: 나노바나나로 카드 raw 이미지를 생성하고, 이어서 텍스트·로고를 합성해 9:16 4프레임 PNG를 만든다. tarot-image-generator와 frame-composer 두 sub-agent를 순차 호출한다.
---

# Image (raw 생성 → 합성)

## 사용

```
/image <topic-slug>
```

## 실행 방식

이 skill은 두 단계로 나뉘어 실행된다.

1. **`tarot-image-generator` sub-agent**: nanobanana로 raw 이미지(카드 뒷면, 미리보기 5장, 확대 카드) 생성.
2. **`frame-composer` sub-agent**: raw 이미지에 draft의 텍스트와 브랜드 로고를 합성해 4개의 9:16 PNG 프레임을 만든다.

## 사전 점검

- `nanobanana` MCP가 사용 가능한지 확인. 미가용 시 단계를 중단하고 사용자에게 보고.
- 합성 도구 가용성 확인 (`magick` / `convert` / Pillow / sharp 중 하나). 미가용 시 보고.

## 절차

1. `.content-artifacts/{topic-slug}/brief.md`, `draft.md`가 존재하는지 확인.
2. **Stage A: raw 이미지 생성**
   - `tarot-image-generator` sub-agent 호출.
   - 결과(`images/raw/*.png` + `image-prompts.md`)를 사용자에게 보여준다.
   - 사용자 피드백(특정 카드 재생성 / 컨셉 변경 / 수락)에 따라 반복.
3. **Stage B: 프레임 합성**
   - `frame-composer` sub-agent 호출.
   - 결과(`images/composed/frame-{1..4}.png`)를 사용자에게 보여준다.
   - 사용자 피드백(텍스트 위치 / 폰트 크기 / 로고 / 색상 — 가능한 범위 안에서) 반영.
4. 사용자 수락 후 다음 skill로 진행 가능 신호.

## 산출물 경로

```
.content-artifacts/{topic-slug}/images/raw/card-back.png
.content-artifacts/{topic-slug}/images/raw/card-preview-{1..5}.png
.content-artifacts/{topic-slug}/images/raw/card-revealed.png
.content-artifacts/{topic-slug}/images/composed/frame-{1..4}.png
.content-artifacts/{topic-slug}/images/image-prompts.md
```

## 제약

- nanobanana MCP만 사용 (다른 이미지 도구 임의 시도 금지).
- visual-style.md의 색·구도·금지 키워드 규칙 준수.
- composed 결과는 1080×1920이며 safe_zone 내에 텍스트·로고가 들어가야 한다.
- raw에 텍스트를 박지 않는다 (합성은 frame-composer의 책임).
