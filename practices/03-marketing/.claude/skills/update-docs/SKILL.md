---
name: update-docs
description: brand-voice / channel-formats / content-adr / reels-templates / domain-knowledge(topic-pool, tarot-cards, reading-style, visual-style) 문서에 항목을 추가/수정/삭제한다. 변경 시 다른 문서와의 충돌·연쇄 영향을 함께 검토한다.
---

# 문서 업데이트

## 사용

```
/update-docs voice         — brand-voice.yaml
/update-docs channel       — channel-formats.yaml
/update-docs adr           — content-adr.yaml
/update-docs reels         — reels-templates.yaml
/update-docs pool          — domain-knowledge/topic-pool.yaml
/update-docs cards         — domain-knowledge/tarot-cards.md
/update-docs reading       — domain-knowledge/reading-style.md
/update-docs visual        — domain-knowledge/visual-style.md
/update-docs history       — topic-history.yaml (수동 보정)
```

인자 없이 호출하면 모든 문서를 함께 검토한다.

## 공통: 컨텍스트 분석 우선 원칙

어떤 문서를 업데이트하든, 지금까지의 작업 내용(특히 최근 review 결과 / 발행 후 피드백)을 먼저 읽고 분석한다. **참고 문서 전체도 모두 먼저 읽고 분석해야 한다.**

1. 위에서 나열된 모든 docs 파일을 읽는다.
2. 새 결정과 기존 항목을 대조하여 다음을 판단한다:
   - **충돌 항목**: 새 결정이 기존 항목과 모순되는가?
   - **연쇄 수정**: 한 문서의 변경이 다른 문서에도 영향을 미치는가?
     - 예: brand-voice.forbidden.phrases에 새 단어 추가 시, 기존 draft·formatted 산출물에 그 단어가 있는지 검토 필요.
     - 예: channel-formats.reels.canvas 변경 시, frame-composer가 만든 기존 PNG가 무효화됨.
     - 예: reels-templates에 frame을 추가하면, content-drafter / frame-composer / reels-renderer 모두 영향을 받음.
   - **폐기 대상**: 이번 변경으로 더 이상 유효하지 않은 항목?
3. 변경 제안을 사용자에게 MUST / RECOMMENDED 등급으로 정리하여 제시.
4. 사용자가 최종 결정한 내용을 반영.

## brand-voice 업데이트

1. brand-voice.yaml + content-adr.yaml을 함께 읽고 ADR과 충돌 여부 확인.
2. forbidden 또는 signature_phrasings 추가 시, 기존 draft.md들을 살펴 영향 범위를 추정해 보고.
3. 변경 반영.

## channel-formats 업데이트

1. channel-formats.yaml + reels-templates.yaml을 함께 읽고, 캔버스/프레임 수 변경 시 reels-templates와 정합 확인.
2. 캔버스/safe_zone/branding 변경 시 기존 composed PNG / output.mp4가 무효화될 수 있음을 고지.
3. 변경 반영.

## content-adr 업데이트

1. content-adr.yaml + brand-voice.yaml + reels-templates.yaml을 함께 읽고 모순 여부 확인.
2. 변경 제안 목록 제시.
3. 항목 작성 스키마:
   ```yaml
   - id: ADR-{번호}
     title: ...
     status: adopted | deprecated | superseded
     date: YYYY-MM-DD
     channels: [...]
     context: |
       (구체적 상황 서술 — 가이드라인 참조)
     decision: ...
     consequence: ...
   ```
4. context 작성 가이드라인:
   - context만 읽고도 "왜 이 결정이 필요했는가"를 구체적으로 연상할 수 있어야 한다.
   - 나쁜 예: "광고 표현이 안 어울림"
   - 좋은 예: "초기에는 마지막 프레임에 '지금 가입하세요' 같은 직접 가입 유도 카피를 넣었으나, 알고리즘이 광고성 컨텐츠로 분류해 도달이 떨어졌다. A/B 결과 댓글/DM 트리거가 우위였다."
5. 변경 확인.

## reels-templates 업데이트

1. reels-templates.yaml + channel-formats.yaml + reels-templates에 의존하는 sub-agent(content-drafter, frame-composer, reels-renderer) 영향 범위 검토.
2. 새 템플릿 추가 시 4프레임 구조에 얽매이지 않아도 되지만, 각 frame.role과 text/image_slots 정의가 필수.
3. 변경 반영.

## topic-pool 업데이트

1. domain-knowledge/topic-pool.yaml에 새 주제 추가.
2. 기존 topic_id와 중복되지 않게 한다.
3. viral_signals 태그는 정해진 카테고리(personal_curiosity_high / low_threshold_for_engagement / near_term_anxiety / hope_seeking / identity_curiosity) 중에서만 사용.
4. 새 카테고리가 필요하면 사용자 합의 후 update-docs voice 등에서도 일관성 확인.

## topic-history 수동 보정

1. 잘못 기록된 항목 정정 또는 외부 발행분(이 하네스 외부에서 발행한 컨텐츠)을 history에 추가.
2. append-only가 깨지는 변경(삭제·수정)은 사용자 명시 확인 후 실행.

## tarot-cards / reading-style / visual-style 업데이트

1. 마크다운 문서이므로 기존 구조를 보존하며 섹션 단위로 수정.
2. 카드 의미·해석 톤·비주얼 규칙을 바꾸면 향후 모든 draft·image 산출물이 달라짐을 고지.
3. 사용자가 최종 확인한 내용을 반영.
