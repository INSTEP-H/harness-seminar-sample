# Marketing Harness — DAILY TAROT (sample brand)

이 프로젝트는 Claude Code 기반 운세 컨텐츠(타로/사주) 자동화 파이프라인이다.
주제 선정 → 기획 → 카피 → 이미지 → 프레임 합성 → 비디오 렌더 → 검수까지 수행한다.
샘플 브랜드는 가상의 **데일리타로 (DAILY TAROT)** 이며, 동일 구조로 다른 운세 브랜드에도 이식 가능하다.

## 산출물 경로

모든 산출물은 `.content-artifacts/{topic-slug}/` 하위에 저장한다.
`{topic-slug}`은 pick-topic 단계에서 결정된다 (예: `2026-05-08-secret-admirer`).

산출물 목록:
- `topic.md` — 선정된 주제 + 후보군 + 선정 사유
- `brief.md` — 작업 명세서 (프레임 템플릿·질문·카드 컨셉·CTA)
- `draft.md` — 프레임별 카피 통합본
- `images/raw/` — 나노바나나 원본 이미지
- `images/composed/frame-{1..4}.png` — 로고·텍스트 합성 완료된 9:16 프레임
- `images/image-prompts.md` — 사용된 프롬프트 기록
- `formatted/reels.md` — reels 시퀀스 메타 (프레임별 노출 시간 등)
- `output.mp4` — 최종 렌더링된 릴스 비디오
- `review.md` — 규칙 기반 검수 결과

## 참조 문서

- `docs/brand-voice.yaml` — 브랜드 톤 (감성·신비형, 단정·도발형 아님)
- `docs/channel-formats.yaml` — instagram(카드뉴스) + reels(9:16 4프레임)
- `docs/content-adr.yaml` — 컨텐츠 의사결정
- `docs/reels-templates.yaml` — 릴스 프레임 시퀀스 템플릿 (예: pick-a-card)
- `docs/topic-history.yaml` — 발행 이력. pick-topic이 중복 회피에 사용
- `docs/bgm-pool.yaml` — 인스트루멘털 트렌딩 BGM 풀. brief가 무작위 1곡 자동 선택
- `docs/domain-knowledge/topic-pool.yaml` — 주제 풀 + 바이럴 시그널
- `docs/domain-knowledge/tarot-cards.md` — 카드 의미 사전
- `docs/domain-knowledge/reading-style.md` — 해석 톤·구조 가이드
- `docs/domain-knowledge/visual-style.md` — 이미지 스타일·브랜드 비주얼 규칙

## 브랜드 톤 (always-apply)

이 톤은 모든 단계, 모든 sub-agent의 기본 시스템 프롬프트로 작용한다.
상세 항목·예시는 `docs/brand-voice.yaml`을 참조한다.

1. **감성 서사형으로 쓴다.** "~네요", "~ 같아요", "~인 것 같습니다" 등 부드러운 어미를 활용한다. 단정·도발형 어미를 강하게 쓰지 않는다.
2. **2인칭으로 독자를 호명한다.** "당신의 마음에는…", "지금 당신을 둘러싼…" 같이 청자에게 직접 말한다.
3. **카드/별자리/사주 용어를 본문에 자연스럽게 녹인다.** 해석체이지 점쟁이 클리셰는 자제한다 ("운명입니다!" 같은 강조 표현 회피).
4. **광고 직설 금지.** "지금 가입하세요" 같은 표현 대신, 댓글·DM 트리거 형태로 자연스럽게 다음 행동을 유도한다.
5. **브랜드 표기**: '데일리타로', 'DAILY TAROT' 두 가지만 사용한다. 변형·줄임말·이모지 미사용은 content-adr 참조.
6. **금지어**는 brand-voice.yaml의 `forbidden` 항목을 항상 검사한다.

## 파이프라인 규칙

1. 모든 sub-agent는 산출물 디렉토리(`.content-artifacts/{topic-slug}/`)에만 쓰기 권한을 가진다. 본 프로젝트의 다른 파일을 수정하지 않는다. 단 `docs/topic-history.yaml`은 pick-topic 종료 시 추가만 가능하다.
2. 이미지 생성은 `nanobanana` MCP를 사용한다. MCP가 사용 불가하면 image 단계를 중단하고 사용자에게 보고한다.
3. 비디오 렌더는 로컬 `ffmpeg` 바이너리에 의존한다. 미설치 시 render 단계를 중단하고 보고한다.
4. review는 규칙 기반 단순 비교만 수행한다. 톤·창의성 평가는 사람에게 위임한다.
5. 최종 발행은 사람이 한다. review가 PASS여도 자동 발행하지 않는다.
6. pick-topic은 `topic-history.yaml`의 직전 N일 내 발행 주제를 자동 제외하여 중복 발행을 방지한다.
7. BGM은 항상 `docs/bgm-pool.yaml`의 인스트루멘털 풀에서 무작위 1곡 자동 선택한다. 가사 있는 곡 / 사용자 임의 외부 파일은 사용자가 명시적으로 지정한 경우에만 허용한다 (한국어 텍스트와 가사 충돌 방지).
