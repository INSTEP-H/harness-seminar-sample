# Code Review Harness

이 프로젝트는 Claude Code 기반 코드리뷰 자동화 파이프라인이다.
산출물은 로컬 파일 시스템과 실제 GitHub PR에 동시에 반영된다.

## 산출물 경로

모든 산출물은 `.review-artifacts/{branch-name}/` 하위에 저장한다.
branch명은 `git branch --show-current`로 resolve한다.

산출물 목록:
- `design-intent.md` — 설계의도 문서
- `code-quality-guide.md` — 평가기준 문서
- `pr-body.md` — PR 본문
- `pr.json` — 생성된 GitHub PR 메타정보 (number, url, base, head, head_sha, repo)
- `review-comments.md` — 리뷰 코멘트
- `review-posted.json` — GitHub에 게시된 review/comment id 목록

## 참조 문서

- `docs/code-convention.yaml` — 팀 코딩 컨벤션 (stacks 필드로 스택별 필터링 가능)
- `docs/adr.yaml` — Architecture Decision Records (stacks, date, status로 조회 가능)

## GitHub 통합 규칙

1. PR 생성·코멘트 게시·답글은 모두 `gh` CLI를 통해 실행한다 (`gh auth status`로 사전 확인).
2. 모든 리뷰 코멘트의 본문은 `[reviewer] pN) `으로 시작한다 (N=1~4). 사람·다른 봇 코멘트와 구분하기 위함.
3. 우선순위 의미:
   - `p1` 반드시 수정 (버그·기준 위반·의도-구현 불일치)
   - `p2` 강력 권장 (유지보수·가독성에 유의미한 영향)
   - `p3` 권장 (현재도 동작 가능, 개선 시 좋음)
   - `p4` 사소한 개선 (네이밍·포맷팅 등)
4. 리뷰 반영 시:
   - 수용: 코드 수정 → commit → push → 해당 review comment에 답글로 commit 해시 게시 (`반영 완료: {sha} - {요약}`).
   - 거부: 답글에 거부 사유 게시 (`반영하지 않음. 이유: {사유}`).
5. 답글은 GitHub PR review comment의 `in_reply_to`로 게시하여 thread를 형성한다.

## 파이프라인 규칙

1. Fork(worktree)로 실행하는 단계에서는 산출물 파일만 생성하고, 소스코드를 수정하지 않는다. (리뷰 반영 단계 제외)
2. 평가기준 생성 시 adr.yaml 전체를 포함하지 않는다. 이번 작업과 관련된 항목만 추출한다.
3. 코드리뷰는 반드시 평가기준에 근거해야 한다. 근거 없는 취향 리뷰를 남기지 않는다.
4. 사용자에게 확인을 요청할 때, 모호하여 구체화가 필요한 논의점을 반드시 함께 정리하여 전달한다.
5. base branch는 사용자가 명시하지 않으면 `main`을 기본으로 한다.
6. 동일 head/base 조합으로 이미 PR이 열려 있으면 새 PR을 만들지 않고 body만 업데이트한다.
