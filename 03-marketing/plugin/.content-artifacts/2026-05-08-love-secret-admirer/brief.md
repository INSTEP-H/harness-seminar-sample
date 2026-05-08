# Brief — 2026-05-08-love-secret-admirer

## 메타

- **topic_slug**: 2026-05-08-love-secret-admirer
- **frame_template**: pick-a-card
- **publish_channels**: [reels, instagram]
- **bgm**: Santo & Johnny — “And I Love Her” (instrumental, 1964). t=60s부터 14s, fade in 0.8s / fade out 1.5s, mix -18dB (channel-formats.audio.bgm.volume_db). source: https://www.youtube.com/watch?v=EHQYAylvqIo. 인스트루멘털 트렌딩 풀(`docs/bgm-pool.yaml`)에서 선택

## 후크

- **F1 question**: 요즘 티 안내고 나를 좋아하는 사람
- **F2 question_full**: 직관적으로 끌리는 한 장을 골라보세요

## 카드 컨셉 (5장 미리보기)

“주변에서 호감을 보일 만한 5가지 사람 유형”을 풍경/오브젝트 메타포로 매핑한다.
모든 카드는 인물 클로즈업 없이 풍경·오브젝트로만 표현 (visual-style §4 금지 키워드).

| n | 메타포 | 시각 | 의미 |
| --- | --- | --- | --- |
| 1 | 길/도로 | 비 온 뒤 골목길, 멀리 보이는 가로등 | 같이 다니는 길에서 자주 마주치는 사람 |
| 2 | 물가 | 잔잔한 호숫가에 떠 있는 작은 종이배 | 멀리서 마음을 흘려보내는 사람 |
| 3 | 꽃/식물 | 책상 위 작은 화분, 햇빛이 비스듬히 | 가까이서 자주 챙겨주는 사람 |
| 4 | 실내 공간 | 커튼 사이로 새어드는 빛, 빈 의자 | 마음 안쪽에 자리 잡고 있던 옛 사람 |
| 5 | 도시 야경 | 밤 도시 창가에서 본 도시 불빛 | SNS·연락 너머에서 지켜보는 사람 |

## 선택될 카드 (selected_card_index)

- **n=3 (꽃/식물)** — 가까이서 자주 챙겨주는 사람.
  - 5장 중 가장 “현실 가능성”이 높아 댓글 유입 트리거가 강함.
  - The Lovers (정방향) 키워드를 풀어 쓰는 데 적합.

## 인용 카드

- **The Lovers (정방향)** — 끌림, 가까이 머무르는 마음, 선택의 신호 (tarot-cards.md)

## CTA

- 마지막 프레임에만 둠 (channel-formats.review_rules.cta_in_last_frame_only).
- 카피: “나머지 카드 해석은 댓글로 카드 번호를 남겨주시면 보내드릴게요”
- 직설 가입 유도 금지 (content-adr ADR-002).

## 비주얼

- 컬러: 다크 버건디 / 크림 / 골드 (visual-style §1).
- 카드 뒷면: 골드 태양 모티프, 골드 1.5px 테두리, 모서리 8% 라운드.
- safe_zone: top 8% / bottom 22% / side 6% (channel-formats.reels.safe_zones).
- 로고: top-center, 너비 14% (assets/brand-logo.svg).

## 프레임 노출 시간

| n | role | duration_sec |
| --- | --- | --- |
| 1 | hook | 2.5 |
| 2 | selection | 3.0 |
| 3 | reveal | 6.0 |
| 4 | cta | 2.5 |
| **total** | | **14.0** |

권장 14–18초 범위 내 (channel-formats.reels.frames.duration_sec_total_max).
