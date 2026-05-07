# 문서 업데이트 (brand-voice / channel-formats / content-adr)

`docs/`의 3개 yaml 파일에 항목을 추가/수정/삭제한다.

## 사용법

```
/mafia-marketing:update-docs voice       — brand-voice.yaml
/mafia-marketing:update-docs channel     — channel-formats.yaml
/mafia-marketing:update-docs adr         — content-adr.yaml
```

인자 없이 호출하면 모든 문서를 함께 검토한다.

## 공통: 컨텍스트 분석 우선 원칙

어떤 문서를 업데이트하든, 지금까지의 작업 내용(특히 최근 review 결과 / 발행 후 피드백)을 먼저 읽고 분석한다. **기존 문서 3개도 모두 먼저 읽고 분석해야 한다.**

1. `docs/brand-voice.yaml`, `docs/channel-formats.yaml`, `docs/content-adr.yaml`을 모두 읽는다.
2. 새 결정과 기존 항목을 대조하여:
   - **충돌 항목**: 새 결정이 기존 항목과 모순되는가?
   - **연쇄 수정**: 한 문서의 변경이 다른 문서에도 영향을 미치는가?
     - 예: brand-voice의 forbidden.phrases에 새 단어 추가 시, 기존 콘텐츠 산출물에 해당 단어가 있는지 검토 필요
     - 예: content-adr 신규 항목이 brand-voice의 default cta 위치와 모순되는가?
   - **폐기 대상**: 이번 변경으로 더 이상 유효하지 않은 항목?
3. 변경 제안 목록을 사용자에게 MUST / RECOMMENDED 등급으로 제시한다.
4. 사용자가 최종 결정한 내용을 반영한다.

## brand-voice 업데이트 절차

1. `docs/brand-voice.yaml`을 읽는다.
2. `docs/content-adr.yaml`도 함께 읽고 ADR과 충돌하는 변경이 아닌지 확인한다.
3. forbidden 또는 signature_phrasings에 항목 추가 시, 기존 review.md들을 살펴 영향 범위를 추정해 사용자에게 보고한다.
4. 변경을 반영한다.

## channel-formats 업데이트 절차

1. `docs/channel-formats.yaml`을 읽는다.
2. 채널 추가 시 다음 스키마를 따른다:
   ```yaml
   - id: {channel-id}
     display_name: ...
     body:
       max_chars: ...
       hook_first_line: true | false
       paragraphs_max: ...
       headings_allowed: true | false   # optional
     hashtags:
       max_count: ...
       placement: end_of_post | inline | none
     image:
       required: true | false
       ratio: [...]
       max_count: ...
     notes: [...]
   ```
3. 기존 채널의 규칙(특히 max_chars, image.ratio)을 변경할 경우 기존 산출물의 review가 무효화될 수 있음을 고지한다.

## content-adr 업데이트 절차

1. `docs/content-adr.yaml`을 읽는다.
2. `docs/brand-voice.yaml`도 함께 읽고 모순되는 항목이 있는지 확인한다.
3. 변경 제안 목록을 사용자에게 제시한다.
4. 항목 작성 시 다음 스키마를 따른다:
   ```yaml
   - id: ADR-{번호}
     title: ...
     status: adopted | deprecated | superseded
     date: YYYY-MM-DD
     channels: [...]                   # all 또는 특정 채널 id 목록
     context: |
       (구체적인 상황 서술 — 아래 가이드라인 참조)
     decision: ...
     consequence: ...
   ```
5. **context 작성 가이드라인:**
   - context만 읽고도 "왜 이 결정이 필요했는가"를 구체적으로 연상할 수 있어야 한다.
   - 나쁜 예: "이모지가 톤과 안 맞음"
   - 좋은 예: "초기 SNS 운영 시 이모지를 적극 활용했으나, 도발형 톤과의 부조화가 잦아 메시지가 약화됐다. 또한 채널/플랫폼별 렌더링 차이로 의도와 다른 인상을 주는 사례가 분기마다 반복됐다."
   - 당시 어떤 문제가 있었는지, 어떤 데이터/관찰이 있었는지를 포함한다.
6. context가 불충분하다고 판단되면 사용자에게 구체화 방안을 요청한다.
7. 변경 내용을 사용자에게 확인받는다.
