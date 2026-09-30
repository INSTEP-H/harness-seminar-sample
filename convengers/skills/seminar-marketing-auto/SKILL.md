---
name: seminar-marketing-auto
description: 운세 컨텐츠 릴스 자동화 파이프라인 전체를 오케스트레이션한다. 주제 선정 → 기획 → 카피 → 이미지 → 합성 → 렌더 → 검수까지 한 번에 수행한다.
---

> 원저작: VIBE MAFIA CLUB (https://github.com/vibemafiaclub/harness-seminar-sample). 라이선스는 원본 README의 License 절(MIT) 그대로입니다. 아래 원문과 저작권 표기는 손대지 않았습니다. 컨벤져스 키트용으로 스킬 이름만 바꿔 옮겼습니다.

# 마케팅 컨텐츠 파이프라인 (Auto)

## 사용

```
/auto                    # 주제부터 자동 선정
/auto <topic-slug>       # 기존 진행 중인 slug로 이어서 실행
```

## 사전 조건

- `docs/brand-voice.yaml`, `docs/channel-formats.yaml`, `docs/content-adr.yaml`, `docs/reels-templates.yaml`이 작성되어 있다.
- `docs/domain-knowledge/topic-pool.yaml`, `docs/topic-history.yaml`이 존재한다.
- 이미지 단계: `nanobanana` MCP 활성화.
- 합성 단계: ImageMagick(`magick`) 또는 Pillow 등 합성 도구 가용.
- 렌더 단계: 로컬 `ffmpeg` 설치.

## 파이프라인

### Step 1: 상태 점검

1. 사용자에게 다음을 요약해 보여준다:
   - 적용될 브랜드(브랜드명 / 톤 핵심 규칙 / 발행 채널 = reels + instagram caption)
   - 외부 의존(`nanobanana` MCP, ImageMagick/Pillow, ffmpeg)의 가용 여부
2. 인자가 비어 있으면 Step 2부터, slug가 주어지면 해당 slug 산출물의 진행도를 확인하고 결손 단계부터 이어서 시작.

### Step 2: 주제 선정

1. **`pick-topic` skill을 실행**한다 (내부적으로 `topic-curator` sub-agent 호출).
2. topic-pool과 topic-history를 비교해 30일 쿨다운 적용된 후보 3~5개를 점수와 함께 제시.
3. 사용자가 1개를 고르면 topic-slug을 함께 결정.
4. `topic.md` 저장 + `docs/topic-history.yaml` append.

### Step 3: Brief

1. **`brief` skill을 실행**한다 (메인 컨텍스트에서 사용자와 직접 대화).
2. 선정된 주제 기반으로 frame_template, card_concept, selected_card_index, CTA, BGM 사용 여부를 사용자와 함께 확정.
3. 모호한 부분(카드 컨셉의 시각적 분류, 카드 선택의 의도 등)을 명확히 한다.
4. `brief.md` 저장.

### Step 4: Draft

1. **`draft` skill을 실행**한다 (`content-drafter` sub-agent 호출).
2. brief + reels-templates + brand-voice + reading-style + tarot-cards 기반으로 프레임별 카피 작성.
3. 사용자에게 제시. 톤 강도·시그니처 표현 사용 여부 피드백 반영.
4. `draft.md` 확정.

### Step 5: Image

1. **`image` skill을 실행**한다 (`tarot-image-generator` + `frame-composer` sub-agent 순차 호출).
2. tarot-image-generator: nanobanana로 카드 뒷면·미리보기 5장·확대 카드 raw 생성.
3. 사용자에게 raw 이미지를 보여주고 재생성/수락 받음.
4. frame-composer: raw 이미지에 텍스트·로고를 합성해 4개의 9:16 프레임 PNG 생성.
5. 사용자에게 합성된 프레임 보여주고 재합성/수락.

### Step 6: Format

1. **`format` skill을 실행** (sub-agent에 위임 가능, 단순 변환이라 메인에서 처리해도 됨).
2. 각 채널별 메타와 캡션을 생성:
   - `formatted/reels.md` — 프레임 시퀀스, 노출 시간, BGM 사용 여부
   - `formatted/instagram.md` — 인스타 피드 캡션 본문 + 해시태그

### Step 7: Render

1. **`render` skill을 실행**한다 (`reels-renderer` sub-agent 호출).
2. ffmpeg로 4 PNG → mp4 합성.
3. BGM 파일이 brief에 지정되어 있으면 합성 단계에 포함.
4. `output.mp4` 저장.

### Step 8: Review (자동)

1. **`review` skill을 실행**한다 (`content-reviewer` sub-agent 호출). 사용자 확인 없이 자동.
2. 텍스트·비주얼·비디오 규칙을 자동 검사.
3. `review.md` 저장.
4. FAIL 있으면 사용자에게 강조해 보고. 사용자가 수정/수용 결정.

### Step 9: 사람 최종 승인

1. `output.mp4`, `formatted/instagram.md`, `images/composed/`, `review.md`를 묶어 사용자에게 제시.
2. **자동 발행하지 않는다.** 사용자가 직접 인스타에 업로드한다.

## 완료

산출물 경로의 전체 파일 목록과 review 최종 상태를 사용자에게 보고한다.
