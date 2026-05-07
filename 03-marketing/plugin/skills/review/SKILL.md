---
name: review
description: 텍스트(draft+formatted) · 비주얼(composed PNG) · 비디오(output.mp4)를 brand-voice / channel-formats / content-adr / reels-templates의 규칙에 비추어 자동 검수한다. 톤 평가는 하지 않는다.
---

# Review (규칙 기반 검수)

## 사용

```
/review <topic-slug>
```

## 실행 방식

이 skill은 `content-reviewer` sub-agent에 위임되며, **사용자 확인 없이 자동으로 실행된다.**

## 검수 영역

- **텍스트**: 금지어 / 이모지 / 느낌표 / 광고 직설 / 브랜드 표기 / CTA 위치 / 본문 길이 / 2인칭 화법
- **비주얼**: 프레임 수 / 해상도 / 로고 부재 / safe_zone 침범
- **비디오**: 총 길이 / 비율 / 코덱

상세 항목·판정 기준은 `agents/content-reviewer.md` 참조.

## 절차

1. **`content-reviewer` sub-agent 호출** → 모든 항목 점검.
2. 각 항목을 PASS / FAIL / WARN / UNVERIFIED로 분류.
3. `review.md` 저장.
4. FAIL이 있으면 호출자에게 강조해서 보고.

## 산출물 경로

```
.content-artifacts/{topic-slug}/review.md
```

## 제약

- 톤·창의성·이미지 미감 평가 금지. 그 판단은 사람이 한다.
- 임의로 본문/이미지/비디오를 수정하지 않는다. FAIL 보고만 한다.
- 점검 도구(ffprobe, identify 등) 미설치 시 UNVERIFIED 처리.
- 최종 발행 승인은 reviewer가 아니라 사람이 한다. PASS여도 자동 발행하지 않는다.
