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

`tools/generate_cards.py` (이번 데모용 1회성)에서 Pillow로 다음 요소를 합성:

- 다크 버건디 배경 + 모서리 비네팅
- 골드 1.5px 테두리, 8% 모서리 라운드
- 카드별 시그니처 모티프 (sun-moon / 길 / 물가 / 화분 / 의자 / 도시)
- 결과물은 nanobanana 복귀 시 동일 파일 경로로 덮어쓸 수 있음
