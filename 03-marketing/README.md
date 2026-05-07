# MAFIA Marketing harness

Claude Code 기반 마케팅 컨텐츠 자동화 파이프라인.

> 단일 토픽을 기획 → 초안 → 이미지 → 채널별 포맷 변환 → 검수까지 자동화합니다.
> 사람이 개입하는 지점은 brief 확정과 최종 발행 승인 두 번입니다.

> 하네스와 파이프라인에 대한 자세한 설명은 [영상](https://www.youtube.com/watch?v=CfLhrS0ww5w)을 참고해주세요.

## Quick Start

1. 플러그인을 설치합니다.

   ```sh
   # claude code 실행
   claude

   # 플러그인 설치
   /plugin marketplace add vibemafiaclub/mafia-marketing-harness
   /plugin install mafia-marketing
   ```

2. `docs/brand-voice.yaml`, `docs/channel-formats.yaml`, `docs/content-adr.yaml`를 복사한 뒤 브랜드 상황에 맞게 수정합니다.
3. 이미지 생성에는 `nanobanana` MCP가 필요합니다. 설치되어 있어야 `image` 단계가 동작합니다.
4. Claude Code에서 `/mafia-marketing:auto <topic-slug>`를 실행하세요.

## 파이프라인 흐름

```
/mafia-marketing:auto <topic-slug>
  → [1] 상태 점검 (brand-voice 확인)
  → [2] Brief (메인)              — 주제·타겟·메시지 확정
  → [3] Draft (Sub-agent)         — 브랜드 톤 기반 본문 초안
  → [4] Image (Sub-agent)         — nanobanana로 이미지 생성
  → [5] Format (Sub-agent)        — 채널별 포맷 변환
  → [6] Review (Sub-agent, 자동)  — 규칙 기반 검수
  → [7] 사람 최종 승인            — 발행 직전 사람이 확인
```

## 브랜드 톤 일관성

브랜드 톤은 `plugin/CLAUDE.md`에 요약되어 모든 sub-agent에 항상 적용됩니다(AGENTS.md 패턴).
상세 항목·금지어·시그니처 표현 등은 `docs/brand-voice.yaml`에 정의되어 있고, 각 단계가 필요할 때 참조합니다.

## Skill 목록

| 커맨드                          | 설명                            |
| ------------------------------- | ------------------------------- |
| `/mafia-marketing:auto`         | 전체 파이프라인 오케스트레이션  |
| `/mafia-marketing:brief`        | 주제·타겟·메시지 확정 (작업 명세서) |
| `/mafia-marketing:draft`        | 본문 초안 작성                  |
| `/mafia-marketing:image`        | 이미지 프롬프트 + 생성          |
| `/mafia-marketing:format`       | 채널별 포맷 변환                |
| `/mafia-marketing:review`       | 규칙 기반 검수                  |
| `/mafia-marketing:update-docs`  | brand-voice / channel / ADR 관리 |

## 산출물

작업별 산출물은 `.content-artifacts/{topic-slug}/`에 저장됩니다.

- `brief.md` — 작업 명세서 (주제·타겟·핵심 메시지·CTA)
- `draft.md` — 본문 초안
- `images/` — 생성된 이미지 + `image-prompts.md`
- `formatted/{channel}.md` — 채널별 발행본
- `review.md` — 규칙 기반 검수 결과

## License

MIT
