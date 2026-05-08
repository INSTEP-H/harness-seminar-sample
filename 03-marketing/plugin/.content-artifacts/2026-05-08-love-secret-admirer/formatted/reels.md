# Reels Sequence Meta — 2026-05-08-love-secret-admirer

## 캔버스

- aspect_ratio: 9:16
- resolution: 1080x1920
- background_color: "#3B1B1B"

## 시퀀스

| frame | role | duration_sec | image | 텍스트 슬롯 |
| --- | --- | --- | --- | --- |
| 1 | hook | 2.5 | images/composed/frame-1.png | 요즘 티 안내고 / 나를 좋아하는 사람 |
| 2 | selection | 3.0 | images/composed/frame-2.png | 직관적으로 끌리는 / 한 장을 골라보세요 |
| 3 | reveal | 6.0 | images/composed/frame-3.png | 3번 카드 + 본문 (294자) |
| 4 | cta | 2.5 | images/composed/frame-4.png | 댓글로 카드 번호를 남겨주세요 |

- **total_duration_sec**: 14.0
- **권장 범위**: 14–18초 (channel-formats.reels.frames.duration_sec_total_max)

## 오디오

- bgm: **Santo & Johnny — “And I Love Her”** (instrumental, 1964). t=60s부터 14s 후크, fade in 0.8s / fade out 1.5s, -18dB
- bgm 선정: `docs/bgm-pool.yaml`의 인스트루멘털 트렌딩 풀에서 선택
- tts: 미사용

## 렌더 옵션 (ffmpeg)

- input: 4 PNG, 각 duration에 따라 단순 stills concat
- vcodec: libx264, preset: medium, crf: 18
- pix_fmt: yuv420p (인스타 호환)
- output: output.mp4

## 채널 라벨

- target_channels: [reels, instagram]
- caption: formatted/instagram.md 참조
