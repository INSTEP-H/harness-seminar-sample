# Marketing Harness

이 프로젝트는 Claude Code 기반 마케팅 컨텐츠 자동화 파이프라인이다.
단일 토픽을 기획 → 초안 → 이미지 → 채널별 포맷 → 검수까지 자동화한다.

## 산출물 경로

모든 산출물은 `.content-artifacts/{topic-slug}/` 하위에 저장한다.
`{topic-slug}`은 사용자가 brief 단계에서 확정한 슬러그(예: `harness-onboarding`, `2026-04-launch`)이다.

산출물 목록:
- `brief.md` — 작업 명세서 (주제·타겟·핵심 메시지·CTA·발행 채널 목록)
- `draft.md` — 본문 초안
- `images/` — 생성된 이미지 파일 + `image-prompts.md`
- `formatted/{channel}.md` — 채널별 발행본
- `review.md` — 규칙 기반 검수 결과

## 참조 문서

- `docs/brand-voice.yaml` — 브랜드 톤·페르소나·금지어·시그니처 표현
- `docs/channel-formats.yaml` — 채널별(Threads/X/LinkedIn/IG) 길이·해시태그·이미지 비율 규칙
- `docs/content-adr.yaml` — 컨텐츠 의사결정 (예: "이모지 미사용", "후크 우선" 등)

## 브랜드 톤 (always-apply)

이 톤은 모든 단계, 모든 sub-agent의 기본 시스템 프롬프트로 작용한다.
상세 항목·예시는 `docs/brand-voice.yaml`을 참조하되, 아래 핵심 규칙은 어떤 단계에서도 위반하지 않는다.

1. **단정형으로 쓴다.** "~할 수 있을지도 몰라요" 같은 회피 표현 금지. "~한다", "~다."
2. **도발형 후크를 첫 줄에 둔다.** 평이한 인사말로 시작하지 않는다.
3. **이모지를 사용하지 않는다.** (브랜드 결정. content-adr 참조)
4. **약속이 아니라 도발.** "~를 도와드립니다"가 아니라 "~에 멈춰 있다면, 그건 당신의 한계가 아니라 도구의 한계다."
5. **고유 명사 표기**: '바이브마피아클럽', 'VIBE MAFIA CLUB', 'VMC' 중 하나만 사용. 줄임말·변형 금지.
6. **금지어**는 brand-voice.yaml의 `forbidden` 항목을 항상 검사한다. 검수 단계에서 위반 시 자동 FAIL.

## 파이프라인 규칙

1. Sub-agent로 실행하는 단계(draft, image, format, review)는 산출물 디렉토리(`.content-artifacts/{topic-slug}/`)에만 쓰기를 수행한다. 본 프로젝트의 다른 파일을 수정하지 않는다.
2. 이미지 생성은 `nanobanana` MCP를 사용한다. MCP가 사용 불가능하면 image 단계를 중단하고 사용자에게 보고한다.
3. review는 규칙 기반 단순 비교만 수행한다 (길이·해시태그 수·금지어·이미지 비율 등). 톤·창의성에 대한 평가는 하지 않는다.
4. 최종 발행 승인은 반드시 사람이 한다. review가 PASS여도 자동 발행하지 않는다.
5. 사용자에게 확인을 요청할 때, 모호하여 구체화가 필요한 논의점을 반드시 함께 정리하여 전달한다.
