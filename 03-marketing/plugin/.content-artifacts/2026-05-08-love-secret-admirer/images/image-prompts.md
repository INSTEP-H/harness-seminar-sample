# Image Prompts — 2026-05-08-love-secret-admirer

## 외부 도구 상태

- nanobanana MCP: **사용 불가** (`403 PERMISSION_DENIED` — 두 모델 동일).
  - 하네스 규칙(plugin/CLAUDE.md §파이프라인 규칙 2)은 “MCP 사용 불가 시 image 단계 중단 후 보고”다.
  - 이번 시연에서는 사용자 지시(“오류 시 개선/수정하면서 진행”)에 따라 Pillow 기반 절차 생성으로 폴백.
- Pillow 12.2.0: 사용 가능 (절차 생성 fallback).

## 공통 프리픽스 (visual-style §4)

```
soft cinematic painterly tarot card style,
muted dark burgundy background (#3B1B1B), warm cream highlights,
subtle gold accents (#D4A24C), dreamy mystical mood,
9:16 aspect ratio
```

## 카드별 프롬프트 (nanobanana 복귀 시 재사용)

### card-back

```
{공통 프리픽스},
centered minimalist gold sun-and-crescent-moon symbol,
thin elegant 1.5px gold border frame around the card,
art deco geometric pattern, slightly rounded corners,
no text, no logos, no human face,
painterly soft depth of field, deep shadow vignette
```

### card-preview-1 (길/도로)

```
{공통 프리픽스},
narrow rainy alley after rain, distant warm lantern glow,
wet cobblestone reflections, soft mist,
no text, no logos, no human face close-up,
painterly soft depth of field
```

### card-preview-2 (물가)

```
{공통 프리픽스},
calm lake at dusk with a small folded paper boat floating,
soft ripples, gentle reflective light,
no text, no logos, no human face,
painterly soft depth of field
```

### card-preview-3 (꽃/식물) — 선택될 카드

```
{공통 프리픽스},
small potted plant on a wooden desk, slanted afternoon sunlight,
warm cream highlights on leaves, dust particles in air,
no text, no logos, no human face,
painterly soft depth of field
```

### card-preview-4 (실내 공간)

```
{공통 프리픽스},
quiet interior with sheer curtain letting light pass through,
empty wooden chair half in shadow, dust motes drifting,
no text, no logos, no human face,
painterly soft depth of field
```

### card-preview-5 (도시 야경)

```
{공통 프리픽스},
view from a window onto a distant city at night,
scattered warm window lights, faint condensation,
no text, no logos, no human face close-up,
painterly soft depth of field
```

### card-revealed (= card-preview-3 확대)

```
{card-preview-3 프롬프트와 동일 + ultra-detailed close-up framing}
```

## Fallback 절차 생성 노트

`_tools/generate_cards.py` 에서 다음 두 경로를 사용:

### 카드 5장 (preview-1..5)

**Wikimedia Commons의 Rider-Waite-Smith 원본 (public domain)** 을 사용한다.

| 카드 슬롯 | RWS 원본 | 의미 매핑 |
| --- | --- | --- |
| preview-1 (길/도로) | The Fool (0) | 새로운 시작·이동 |
| preview-2 (물가) | The Star (XVII) | 회복·희망의 물가 |
| preview-3 (꽃/식물, 선택) | The Lovers (VI) | 끌림·가까이 머무는 마음 |
| preview-4 (실내 공간) | The Hermit (IX) | 내면 탐색·고요한 실내 |
| preview-5 (도시 야경) | The Moon (XVIII) | 밤의 환상·잠재의식 |

원본 위에 다음 가벼운 후처리:
- 채도 0.92, sepia(212,162,76) 6% blend, 비네팅 10% — 빈티지 톤 통일
- 골드 이중 외곽 + 매팅(burgundy) + 안쪽 골드 라인 + 4코너 아르누보 곡선

원본 출처:
- The Fool: https://commons.wikimedia.org/wiki/File:RWS_Tarot_00_Fool.jpg
- The Lovers: https://commons.wikimedia.org/wiki/File:RWS_Tarot_06_Lovers.jpg
- The Hermit: https://commons.wikimedia.org/wiki/File:RWS_Tarot_09_Hermit.jpg
- The Star: https://commons.wikimedia.org/wiki/File:RWS_Tarot_17_Star.jpg
- The Moon: https://commons.wikimedia.org/wiki/File:RWS_Tarot_18_Moon.jpg

저작권: Pamela Colman Smith (1878–1951), life+70 만료. 글로벌 public domain.

### 카드 뒷면 + reveal + 카운트다운

Pillow 자체 생성:
- card-back: 다크 버건디 + 아르누보 다이아몬드 액자 + 32방향 sun-rays + 중앙 sun-moon
- card-revealed: preview-3(The Lovers) + 골드 외곽 글로우
- 카운트다운 25 sub-frame: F2 베이스 위에 골드 외곽 링 + 진행 호 + 펄스 숫자 (등장→안정→박동→페이드)
