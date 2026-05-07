# Review (규칙 기반 검수)

채널별 발행본을 brand-voice·channel-formats·content-adr의 **규칙**에 비추어 자동 검수한다.
톤·창의성에 대한 평가는 수행하지 않는다. 그 판단은 사람의 책임이다.

## 사용법

```
/mafia-marketing:review <topic-slug>
```

## 실행 방식

이 skill은 sub-agent에 위임되며 **사용자 확인 없이 자동으로 실행된다.**

## 검수 항목 (모두 규칙 기반)

### 1. 길이
- 각 `formatted/{channel}.md` 본문이 channel-formats의 `body.max_chars` 이하인가?

### 2. 후크 위치
- channel-formats의 `body.hook_first_line`이 true인 채널에서 첫 줄이 후크 형식인가?
  - 검사: 첫 줄이 평이한 인사("안녕하세요" 등)나 자기소개로 시작하지 않는가?

### 3. 금지 항목
- brand-voice.forbidden.emojis가 true이면 이모지 검출 시 FAIL.
- brand-voice.forbidden.phrases의 표현 출현 검출 시 FAIL.
- brand-voice.forbidden.passive_phrasings의 표현 출현 검출 시 FAIL (경고로 분류, FAIL 아님).

### 4. 브랜드명 표기 (content-adr ADR-004)
- '바이브마피아클럽', 'VIBE MAFIA CLUB', 'VMC' 외의 변형 검출 시 FAIL.

### 5. CTA 위치 (content-adr ADR-003)
- CTA로 보이는 표현(brand-voice.cta.default 또는 URL 'vibemafiaclub.com')이 본문 중간에 있으면 FAIL.

### 6. 해시태그
- channel-formats의 `hashtags.max_count` 초과 시 FAIL.
- `hashtags.placement`가 end_of_post인데 본문 중간에 해시태그가 있으면 FAIL.

### 7. 이미지
- channel-formats의 `image.required`가 true인데 첨부 이미지가 없으면 FAIL.
- `image.ratio`에 없는 비율의 이미지가 첨부되어 있으면 FAIL.
- `image.max_count` 초과 시 FAIL.

### 8. 채널 간 동일성
- 모든 채널의 본문이 100% 동일하면 경고 (channel별 표현 차별화 권장).

## 절차

1. **sub-agent를 호출**하여 다음을 수행한다:
   - `formatted/` 하위 모든 파일 목록을 수집한다.
   - 각 파일에 대해 위 8개 항목을 차례로 검사한다.
   - 항목별 결과를 PASS / FAIL / WARN으로 분류한다.
2. `review.md`를 작성한다.
3. FAIL이 하나라도 있으면 호출자에게 강조해서 보고한다.

## 산출물 경로

```
.content-artifacts/{topic-slug}/review.md
```

## 문서 구조

```markdown
# Review — {topic-slug}

## 요약
- 채널별 결과:
  - threads.md: PASS
  - linkedin.md: FAIL (1)
  - x.md: WARN (1)

## 채널별 상세

### threads.md
| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| 1 | 길이 | PASS | 287/500 |
| 2 | 후크 위치 | PASS | |
| 3 | 금지 항목 | PASS | |
| 4 | 브랜드명 표기 | PASS | |
| 5 | CTA 위치 | PASS | |
| 6 | 해시태그 | PASS | 4/5 |
| 7 | 이미지 | PASS | 1:1 첨부 |

### linkedin.md
| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| 1 | 길이 | PASS | 2384/3000 |
| 3 | 금지 항목 | **FAIL** | "안녕하세요" 출현 (line 3) |
| ... | | | |

## 사람 최종 검수 요청 항목
- 톤이 도발 강도가 의도대로인지 (자동 판정 불가)
- 이미지가 메시지와 결이 맞는지 (자동 판정 불가)
- 해시태그 선택이 적절한지 (의미적 판정 불가)
```

## 제약

- 톤·강도·창의성에 대한 평가를 하지 않는다. 그 판단은 발행 직전 사람이 한다.
- 임의로 본문을 수정하지 않는다. FAIL을 보고만 하고 수정은 사용자 결정에 따라 format/draft 단계로 회귀한다.
- 단순 비교만 수행한다. 정규식·문자열 매칭 수준에서 끝낸다.
