# 마케팅 컨텐츠 파이프라인

전체 마케팅 컨텐츠 파이프라인을 오케스트레이션한다.

## 사용법

```
/mafia-marketing:auto <topic-slug>
```

`<topic-slug>`을 생략하면 brief 단계에서 사용자와 함께 결정한다.

## 사전 조건

- `docs/brand-voice.yaml`, `docs/channel-formats.yaml`, `docs/content-adr.yaml`이 작성되어 있어야 한다.
- 이미지 단계 사용 시 `nanobanana` MCP가 활성화되어 있어야 한다.

## 파이프라인

### Step 1: 상태 점검

1. 사용자에게 다음을 요약해 보여준다:
   - 적용될 브랜드 톤 핵심 규칙 (CLAUDE.md의 always-apply 섹션)
   - 발행 후보 채널 (channel-formats.yaml의 channels 목록)
2. `nanobanana` MCP가 사용 가능한지 가볍게 확인한다. 사용 불가 시 image 단계가 SKIP될 것임을 미리 고지.
3. `<topic-slug>`이 주어지지 않았다면 brief 단계에서 함께 결정.

### Step 2: Brief (작업 명세서)

1. 메인 컨텍스트에서 `/brief` skill을 실행한다 (sub-agent 위임 없이 사용자와 직접 대화).
2. 주제·타겟·핵심 메시지·CTA·발행 채널을 사용자와 함께 확정한다.
3. 모호한 부분(예: 타겟 페르소나의 구체성, 메시지의 단일성)을 정리해 사용자에게 질문한다.
4. `brief.md`를 산출물 경로에 저장한다.
5. brief가 확정되기 전에는 다음 단계로 진행하지 않는다.

### Step 3: Draft (본문 초안)

1. **sub-agent를 호출**하여 `/draft` skill을 실행한다.
2. sub-agent는 brief + brand-voice + content-adr을 참조하여 단일 본문(채널 무관)을 작성한다.
3. 초안을 사용자에게 제시한다. 메시지 강도·후크·시그니처 표현 사용 여부에 대한 피드백을 받는다.
4. 사용자 피드백을 반영하여 `draft.md`를 확정한다.

### Step 4: Image (이미지 생성)

1. **sub-agent를 호출**하여 `/image` skill을 실행한다.
2. sub-agent는 brief + draft를 입력으로 이미지 프롬프트를 생성하고, `nanobanana` MCP로 이미지를 생성한다.
3. 생성된 이미지와 프롬프트를 사용자에게 보여준다.
4. 사용자 피드백(재생성/수락)에 따라 반복하고 `images/`에 저장.

### Step 5: Format (채널별 포맷 변환)

1. brief에서 확정된 발행 채널 각각에 대해 **sub-agent를 호출**하여 `/format` skill을 실행한다.
2. sub-agent는 draft + channel-formats의 해당 채널 규칙을 참조하여 포맷을 변환한다.
3. 채널별 산출물을 `formatted/{channel}.md`에 저장한다.

### Step 6: Review (규칙 기반 검수)

1. **sub-agent를 호출**하여 `/review` skill을 실행한다. **사용자 확인 없이 자동으로 진행한다.**
2. 규칙 기반 단순 비교만 수행한다 (길이·해시태그 수·금지어·이미지 비율 등).
3. `review.md`를 산출물 경로에 저장한다.
4. FAIL이 있는 경우 사용자에게 강조해서 보고하고, 사용자가 수정/수용을 결정한다.

### Step 7: 사람 최종 승인

1. `formatted/`의 모든 채널 발행본 + `images/` + `review.md`를 사용자에게 묶어서 제시한다.
2. **자동 발행하지 않는다.** 사용자가 직접 발행하도록 안내한다.

### 완료

산출물 경로의 전체 파일 목록과 review 최종 상태를 사용자에게 보고한다.
