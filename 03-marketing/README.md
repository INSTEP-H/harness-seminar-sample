# MAFIA Marketing harness — Pick-a-Card Reels

Claude Code 기반 운세(타로/사주) 컨텐츠 자동화 파이프라인.
샘플 브랜드는 가상의 **DAILY TAROT (데일리타로)** 입니다.

> 단일 주제를 자동 선정 → 기획 → 카피 → 이미지 → 9:16 프레임 합성 → mp4 렌더 → 검수까지 자동화합니다.
> 사람이 개입하는 지점은 **주제 확정 / brief 확정 / 최종 발행 승인** 세 번입니다.

> 하네스와 파이프라인에 대한 자세한 설명은 [영상](https://www.youtube.com/watch?v=CfLhrS0ww5w)을 참고해주세요.

## Quick Start

1. 플러그인을 설치합니다.

   ```sh
   # claude code 실행
   claude

   # 플러그인 설치
   /plugin marketplace add vibemafiaclub/mafia-marketing-harness
   /plugin install mafia-marketing
   ```

2. `docs/` 하위 파일들을 본인 브랜드에 맞게 수정합니다.
3. 외부 의존:
   - **이미지 생성**: `nanobanana` MCP
   - **프레임 합성**: ImageMagick(`magick`) 또는 Pillow / sharp 중 하나
   - **비디오 렌더**: 로컬 `ffmpeg` 바이너리
4. Claude Code에서 `/auto`를 실행하세요.

## 파이프라인 흐름

```
/auto
  → [1] 상태 점검 (외부 의존 가용 확인)
  → [2] Pick Topic        — 30일 쿨다운 + 바이럴 점수로 후보 추천
  → [3] Brief             — frame_template, card_concept, CTA, BGM 확정
  → [4] Draft             — 프레임별 카피 (F1/F2/F3/F4)
  → [5] Image (raw)       — 나노바나나로 카드 뒷면·미리보기 5장·확대 카드 생성
       Image (compose)    — 텍스트·로고 합성 → 9:16 4프레임 PNG
  → [6] Format            — reels.md 시퀀스 메타 + instagram.md 캡션
  → [7] Render            — ffmpeg로 mp4 (BGM 합성 옵션)
  → [8] Review (자동)     — 텍스트·비주얼·비디오 규칙 검수
  → [9] 사람 최종 승인    — 발행 직전 사람이 확인
```

## 자동 주제 선정

`docs/topic-history.yaml`로 직전 30일 발행 이력을 관리합니다 (ADR-004).
`pick-topic` skill이 호출되면:
- topic-pool에서 30일 쿨다운에 걸리지 않는 주제만 후보로 남기고
- 무작위 셔플 후 viral_signals 점수로 정렬해 상위 3~5개를 제시합니다.
- 사용자가 고른 주제는 history에 자동 append되어 다음 회차 중복을 방지합니다.

## 브랜드 톤 일관성

브랜드 톤은 `plugin/CLAUDE.md`에 요약되어 모든 sub-agent에 항상 적용됩니다.
상세 항목·금지어·시그니처 표현은 `docs/brand-voice.yaml`에 있고, 본문 작성 가이드는 `docs/domain-knowledge/reading-style.md`에 있습니다.

## Skill 목록

| 커맨드           | 설명                                                  |
| ---------------- | ----------------------------------------------------- |
| `/auto`          | 전체 파이프라인 오케스트레이션                        |
| `/pick-topic`    | 주제 풀에서 30일 미사용 + 바이럴 시그널 후보 추천     |
| `/brief`         | frame_template, card_concept, CTA, BGM 확정           |
| `/draft`         | 프레임별 카피 작성                                    |
| `/image`         | raw 이미지 생성(나노바나나) + 합성 (4프레임 PNG)      |
| `/format`        | reels 시퀀스 메타 + instagram 캡션                    |
| `/render`        | ffmpeg로 mp4 렌더 (BGM 합성 옵션)                     |
| `/review`        | 규칙 기반 자동 검수 (텍스트/비주얼/비디오)            |
| `/update-docs`   | docs/ 항목 추가/수정/삭제 + 충돌 검토                 |

## Sub-agent 목록

| Agent                   | 모델   | 역할                                                  |
| ----------------------- | ------ | ----------------------------------------------------- |
| `topic-curator`         | sonnet | 주제 후보 큐레이션 (쿨다운 + 점수)                    |
| `content-drafter`       | sonnet | 프레임별 카피 작성                                    |
| `tarot-image-generator` | sonnet | 나노바나나 raw 이미지 생성                            |
| `frame-composer`        | sonnet | 텍스트·로고 합성으로 9:16 PNG 4장 생성                |
| `reels-renderer`        | sonnet | ffmpeg로 mp4 렌더                                     |
| `content-reviewer`      | sonnet | 규칙 기반 검수                                        |

## 산출물

작업별 산출물은 `.content-artifacts/{topic-slug}/`에 저장됩니다.

```
.content-artifacts/{topic-slug}/
├── topic.md
├── brief.md
├── draft.md
├── images/
│   ├── raw/
│   │   ├── card-back.png
│   │   ├── card-preview-{1..5}.png
│   │   └── card-revealed.png
│   ├── composed/frame-{1..4}.png
│   └── image-prompts.md
├── formatted/
│   ├── reels.md
│   └── instagram.md
├── output.mp4
└── review.md
```

## License

MIT
