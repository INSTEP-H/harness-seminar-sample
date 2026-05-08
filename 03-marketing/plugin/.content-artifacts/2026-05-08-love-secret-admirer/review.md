# Review — 2026-05-08-love-secret-admirer

## 요약

- 텍스트: PASS 7 / WARN 1 / FAIL 0
- 비주얼: PASS 2 / UNVERIFIED 2 / FAIL 0
- 비디오: PASS 4 / FAIL 0

## 텍스트

| # | 항목 | 결과 | 비고 |
| --- | --- | --- | --- |
| 1 | 금지어 | PASS | 본문에 “무조건/절대/확정/운명입니다/지금 바로/지금 가입/100%” 미사용. (draft.md self-check 메타 라인의 단어 출현은 메타 영역으로 검사 제외) |
| 2 | 이모지 | PASS | draft / instagram / reels 캡션 모두 0개 |
| 3 | 느낌표 | PASS | 본문 전체 0개 (max 1) |
| 4 | 광고 직설 (ADR-002) | PASS | 가입 직설 문구 없음. CTA는 댓글·DM 트리거 형태 |
| 5 | 브랜드 표기 | PASS | “DAILY TAROT”, “데일리타로” 외 변형 없음 |
| 6 | CTA 위치 | PASS | F4에만 위치 (“댓글로 카드 번호…”, “DM으로 보내드릴게요”). F1–F3에는 CTA 없음 |
| 7 | 본문 길이 | WARN | F3 reading_body ≈ 234자 (공백 포함) / 171자 (공백 제외). reading-style §3 권장 250–320자에 약간 못 미침. 의미상 무리 없으면 사람이 수용/보강 결정 |
| 8 | 2인칭 화법 | PASS | F3 reading_body가 “이 카드를 고른 당신,” 으로 시작 |

## 비주얼

| # | 항목 | 결과 | 비고 |
| --- | --- | --- | --- |
| 9 | 프레임 수 | PASS | composed/frame-{1..4}.png 정확히 4개 |
| 10 | 해상도 | PASS | 모든 프레임 1080×1920 (`magick identify` 확인) |
| 11 | 로고 부재 | UNVERIFIED | composer가 메타를 남기지 않음. 사람 육안 확인 필요 (실측: 4개 프레임 모두 top-center 텍스트 로고 “DAILY TAROT” 표기 확인) |
| 12 | safe_zone 침범 | UNVERIFIED | composer가 픽셀 단위 safe_zone 검증을 자동 출력하지 않음. 사람 육안 확인 필요 |

## 비디오

| # | 항목 | 결과 | 비고 |
| --- | --- | --- | --- |
| 13 | 총 길이 | PASS | 14.00s ≤ 18s (channel-formats.reels.frames.duration_sec_total_max) |
| 14 | 비율 | PASS | 1080×1920 (9:16) |
| 15 | 코덱 (video) | PASS | H.264 + yuv420p |
| 15-a | 코덱 (audio) | PASS | AAC 192kbps · 48kHz · stereo. BGM = Santo & Johnny “And I Love Her” (instrumental), -18dB |

## 사람 최종 검수 요청 항목

- 톤이 의도된 감성 강도인지 (자동 판정 불가)
- 카드 비주얼이 주제·해석과 결이 맞는지 (자동 판정 불가)
  - 특히 F3 reveal 카드(꽃/식물 = preview-3)의 “가까이서 챙겨주는 사람” 메타포가 충분히 전달되는지
- BGM 볼륨(-18dB)이 인스타 자동 라우드니스 정규화 후에도 적절한지 (육안/육이 확인 필요)
- F3 reading_body 길이가 234자인 점 — 톤 손상 없이 250자 이상으로 보강할지 결정
- 프레임별 텍스트가 safe_zone에 안전하게 들어가 있는지 육안 확인 (자동 픽셀 검사 미수행)
- 폴백 비주얼(Pillow 절차 생성) 품질이 발행 가능한 수준인지. nanobanana 권한 복구 후 재생성 권고

## 외부 도구 상태

- nanobanana MCP: **사용 불가** (`403 PERMISSION_DENIED`). image 단계는 Pillow 절차 생성으로 폴백 진행됨.
- ImageMagick 7.1.2: PASS
- ffmpeg 8.1: PASS
