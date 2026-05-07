# 비주얼 스타일 가이드

image / frame-composer 단계가 참조한다.
나노바나나 프롬프트와 합성 합치 위치 등 모든 비주얼 결정의 근거.

## 1. 컬러 팔레트

- 배경 (Primary): `#3B1B1B` 다크 버건디
- 텍스트 (Body): `#F4E9D8` 크림
- 강조 (Accent): `#D4A24C` 골드
- 보조 (Subtle): `#8B5A3C` 머스크

명도 차이는 본문 가독성을 위해 충분히 확보 (배경-텍스트 명도차 7:1 이상 유지).

## 2. 타이포그래피

- Title (질문 슬롯): 한글 명조 계열 / Latin은 Playfair Display 등 클래식 세리프
- Body (해석 본문): 한글 본명조 또는 노토 산스 / Latin은 Inter
- Title size: 캔버스 너비 × 4.2% (1080 기준 약 45px)
- Body size: 캔버스 너비 × 2.8% (1080 기준 약 30px). safe_zone 내부에 들어가지 않으면 자동 축소.

## 3. 카드 비주얼

### 카드 뒷면 (frame 1, frame 2 일부)

모든 카드의 뒷면은 동일한 디자인. 시즌별로 디자인을 바꾸지 않는다 (브랜드 인지 용도).

- 배경: 다크 버건디
- 중앙 모티프: 골드 컬러의 단순화된 태양 또는 달 심볼
- 테두리: 1.5px 골드 라인
- 모서리 라운드: 8% 정도

### 카드 미리보기 (frame 2)

각 카드는 서로 분명히 구별되는 분위기/풍경 이미지. 다음 다섯 분류를 default로 사용한다:

1. 길/도로 — 외부, 이동의 메타포
2. 물가 — 흐름, 정서의 메타포
3. 꽃/식물 — 성장, 관계의 메타포
4. 실내 공간 — 마음의 메타포
5. 도시 야경 또는 자연 — 환경의 메타포

브리프의 `card_concept`이 다르게 지정되면 그에 맞춰 다른 5분류를 사용한다.

### 카드 reveal (frame 3)

선택된 1장을 확대 노출한다. 이미지 전체가 카드 그래픽 내부에 들어가도록 자르고, 카드 테두리(골드)는 유지.
상단에 선택 인덱스 ("3번")를 골드 컬러로 작게 표기.

## 4. 나노바나나 프롬프트 가이드

### 공통 프리픽스 (모든 프롬프트 앞에 자동 결합)

```
soft cinematic painterly tarot card style,
muted dark burgundy background, warm cream highlights,
subtle gold accents, dreamy mystical mood,
9:16 aspect ratio
```

### 카드별 차별화

각 카드 프롬프트는 다음 구조로:

```
{공통 프리픽스},
{장소/오브젝트 설명, 영문 1-2문},
no text, no logos, no human face close-up,
soft depth of field
```

### 금지 키워드 (이미지 일관성)

- 사진 사실주의 (photorealistic, realistic)
- 강한 색조 대비 (high contrast, vibrant)
- 직접 묘사 인물 (no human portraits — 풍경/오브젝트로만 표현)
- 텍스트 (no text, no letters)

## 5. 합성 합치

frame-composer는 다음 순서로 레이어를 쌓는다:

1. 배경 (다크 버건디 단색 또는 그라디언트)
2. 카드(들) — reels-templates의 `image_slots.arrangement`에 따라 배치
3. 카드 인덱스 번호 (frame 1, 2)
4. 텍스트 슬롯 (Title 또는 Body)
5. 로고 (상단 중앙, safe_zone 내부)
6. 선택적 골드 액센트 (카드 테두리, 인덱스 박스)

모든 텍스트·로고는 `safe_zones` 안에 들어가야 한다 (channel-formats.yaml 참조).

## 6. 일관성 점검

review 단계가 다음을 자동 점검:

- 배경 컬러가 brand 컬러 셋 안에 있는지 (히스토그램 기반)
- 로고 위치가 top-center safe_zone 안인지
- 텍스트 슬롯이 safe_zone을 벗어나지 않았는지
- 모든 프레임에서 카드 디자인의 톤이 일관되는지
