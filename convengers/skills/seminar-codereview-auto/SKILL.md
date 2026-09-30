---
name: seminar-codereview-auto
description: 코드리뷰 파이프라인 전체를 오케스트레이션한다. 설계의도 작성 → 평가기준 수립 → PR 본문 + GitHub PR 생성 → 코드리뷰 + GitHub 코멘트 게시 → 리뷰 반영 + 답글 순으로 진행한다.
---

> 원저작: VIBE MAFIA CLUB (https://github.com/vibemafiaclub/harness-seminar-sample). 라이선스는 원본 README의 License 절(MIT) 그대로입니다. 아래 원문과 저작권 표기는 손대지 않았습니다. 컨벤져스 키트용으로 스킬 이름만 바꿔 옮겼습니다.

# 코드리뷰 파이프라인

전체 코드리뷰 파이프라인을 오케스트레이션한다. 산출물은 로컬 파일 + GitHub PR에 동시에 반영된다.

## 사전 조건

- `docs/code-convention.yaml`과 `docs/adr.yaml`이 팀 상황에 맞게 작성되어 있어야 한다.
- 구현이 완료된 feature branch에서 실행한다.
- `gh` CLI 인증 완료.

## 파이프라인

### Step 1: 상태 점검

1. `git branch --show-current`로 현재 branch를 확인한다.
2. `gh auth status`로 GitHub 인증을 확인한다.
3. 사용자에게 다음을 확인한다:
   - branch명 (head)
   - base branch (기본: `main`)
4. base branch 대비 git diff를 확인한다.
   ```
   git diff {base}...HEAD --stat
   ```
   변경 파일 수와 라인 수를 사용자에게 보고한다.
5. `.review-artifacts/{branch-name}/` 디렉토리를 생성한다.

### Step 2: 설계의도 작성

1. **worktree(fork)를 생성**하여 `write-intent` skill을 실행한다.
2. 초안과 함께 **모호한 논의점**을 사용자에게 제시한다.
3. 사용자 피드백을 반영하여 `design-intent.md`를 확정한다.
4. 산출물을 `.review-artifacts/{branch-name}/`에 저장한다.
5. worktree를 정리한다.

### Step 3: 평가기준 수립

1. **worktree(fork)를 생성**하여 `gen-criteria` skill을 실행한다.
2. sub-agent가 `docs/adr.yaml`을 분석하여 관련 항목을 추출한다.
3. 초안과 함께 **기준 적용 범위가 모호한 논의점**을 사용자에게 제시한다.
4. 사용자 피드백을 반영하여 `code-quality-guide.md`를 확정한다.
5. 산출물을 `.review-artifacts/{branch-name}/`에 저장한다.
6. worktree를 정리한다.

### Step 4: PR 본문 생성 + GitHub PR 생성

1. **worktree(fork)를 생성**하여 `create-pr-body` skill을 실행한다.
2. git diff 기반으로 PR 본문 초안을 생성한다.
3. 초안과 함께 **명확히 해야 할 논의점**을 사용자에게 제시한다.
4. 사용자 피드백을 반영하여 `pr-body.md`를 확정한다.
5. 현재 branch를 origin에 push (필요 시).
6. `gh pr create`로 실제 PR을 생성한다 (draft 모드 권장).
7. PR 메타정보를 `pr.json`에 저장한다.
8. PR URL을 사용자에게 보고한다.
9. worktree를 정리한다.

### Step 5: 코드리뷰 실행 + GitHub 코멘트 게시

1. **sub-agent를 호출**하여 `review` skill을 실행한다.
2. sub-agent는 다음을 입력받아 자동으로 리뷰한다:
   - `code-quality-guide.md`, `design-intent.md`, `pr-body.md`, `pr.json`
   - `git diff {base}...HEAD`
3. 리뷰 결과를 `review-comments.md`에 저장한다.
4. 각 코멘트를 GitHub PR에 inline review comment로 게시한다.
   - 본문은 `[reviewer] pN) `으로 시작.
   - 라인별로 `path` + `line` + `side="RIGHT"` 지정.
5. 게시 결과(comment id 등)를 `review-posted.json`에 저장한다.
6. **사용자 확인 없이 자동으로 진행한다.**

### Step 6: 리뷰 반영 + GitHub 답글 게시

1. **worktree(fork)를 생성**하여 `reflect-review` skill을 실행한다.
2. PR의 `[reviewer]` 코멘트를 모두 가져온다 (이미 답글이 달린 것은 제외).
3. 각 코멘트의 수용/거부 판단을 사용자에게 일괄 제시한다.
4. 사용자 확인 후:
   - **수용**: 코드 수정 → 관련 묶음 단위로 commit → push → 답글에 commit 해시 게시.
   - **거부**: 답글에 거부 사유 게시.
5. QA를 수행한다 (빌드, 테스트). 버그 발견 시 수정 루프 반복.
6. 핵심 변경사항(반영/거부 수, 추가 commit, QA 결과)을 사용자에게 보고한다.

### 완료

파이프라인이 완료되면 다음을 사용자에게 보고한다:
- PR URL
- 산출물 경로 (`.review-artifacts/{branch-name}/`)의 전체 파일 목록
- 게시된 review comment 수와 그중 반영/거부 수
- 추가 commit 목록과 QA 최종 상태
