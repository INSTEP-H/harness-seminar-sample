---
name: review
description: 평가기준·설계의도·PR 본문·git diff를 입력받아 근거 기반 코드리뷰를 수행하고, GitHub PR에 라인별 inline review comment를 게시한다. sub-agent가 사용자 확인 없이 자동으로 실행한다.
---

# 코드리뷰 실행 + GitHub 코멘트 게시

평가기준, 설계의도, PR 본문, git diff를 입력받아 근거 기반 코드리뷰를 수행하고, 결과를 실제 GitHub PR의 inline review comment로 게시한다.

## 실행 방식

이 skill은 sub-agent가 자동으로 실행한다. 사용자 확인 없이 진행된다.

## 사전 조건

- `.review-artifacts/{branch-name}/pr.json`이 있어야 한다 (create-pr-body 실행 후 생성됨).
- `gh` CLI 인증 완료.

## 절차

### A. 리뷰 작성

1. 산출물 경로에서 다음 문서를 읽는다:
   - `.review-artifacts/{branch-name}/code-quality-guide.md`
   - `.review-artifacts/{branch-name}/design-intent.md`
   - `.review-artifacts/{branch-name}/pr-body.md`
   - `.review-artifacts/{branch-name}/pr.json` (PR 번호, head_sha 등)
2. base branch 대비 git diff를 수집한다.
   ```
   git diff {base}...HEAD
   ```
3. 다음 원칙에 따라 리뷰 코멘트를 작성한다:
   - **의도를 최대한 잘 파악하고, 비판적으로 검토한다.** 설계의도 문서와 PR 본문을 통해 작성자의 의도를 깊이 이해한 뒤, 그 의도가 코드에 정확히 반영되었는지를 비판적 관점에서 검증한다.
   - **모든 코멘트는 code-quality-guide.md의 기준에 근거해야 한다.** 근거 없는 취향 리뷰를 남기지 않는다.
   - 설계의도 문서에 명시된 의도적 결정을 존중한다. 의도적 결정에 대해 "왜 이렇게 했나요?"라고 묻지 않는다. 단, 의도와 실제 구현이 불일치하는 경우는 지적한다.
   - 코멘트 우선순위를 분류한다:
     - `p1` — 반드시 수정. 버그, 기준 위반, 의도-구현 불일치 등
     - `p2` — 강력 권장. 유지보수성, 가독성에 유의미한 영향
     - `p3` — 권장. 개선하면 좋지만 현재도 동작에 문제 없음
     - `p4` — 사소한 개선. 네이밍, 포맷팅 등
   - **변경을 제안할 때, 해당 변경의 side effect가 있다면 반드시 함께 설명한다.** 그리고 side effect가 있음에도 해당 방향을 제안하는 이유를 명시한다. 리뷰는 무조건 반영해야 하는 것이 아니므로, 구현자가 트레이드오프를 판단할 수 있는 충분한 정보를 제공한다.
   - 파일 경로와 라인 번호를 명시한다 (GitHub inline 코멘트 위치 결정에 사용).
4. 리뷰 결과를 `.review-artifacts/{branch-name}/review-comments.md`에 저장한다.

### B. GitHub PR에 inline review comment 게시

1. `pr.json`에서 number, head_sha, repo를 읽는다.
2. 작성된 모든 코멘트를 하나의 review로 묶어 게시한다.
   각 코멘트의 body는 반드시 `[reviewer] pN) `으로 시작한다 (N은 1~4).

   API 호출:
   ```
   gh api -X POST /repos/{owner}/{repo}/pulls/{number}/reviews \
     --input - <<'JSON'
   {
     "commit_id": "{head_sha}",
     "event": "COMMENT",
     "body": "[reviewer] 자동 코드리뷰 결과 ({comment-count}개 코멘트)",
     "comments": [
       {
         "path": "src/foo.ts",
         "line": 42,
         "side": "RIGHT",
         "body": "[reviewer] p2) 본 코멘트 내용..."
       }
     ]
   }
   JSON
   ```
   - `line` + `side="RIGHT"`을 사용한다 (변경된 새 파일의 라인 번호).
   - 삭제된 라인을 가리키려면 `side="LEFT"`.
   - 다중 라인은 `start_line` + `line` (둘 다 필수).
3. 응답에서 review id와 각 코멘트의 id를 받아 `.review-artifacts/{branch-name}/review-posted.json`에 저장한다.
   ```json
   {
     "review_id": 123,
     "comments": [
       { "id": 456, "path": "src/foo.ts", "line": 42, "priority": "p2" }
     ]
   }
   ```

### 코멘트 본문 형식

```
[reviewer] p2) {본문}

근거: {code-quality-guide.md의 어떤 기준}
제안: {구체적 제안}
side effect: {예상되는 부작용 또는 "없음"}
제안 이유: {side effect에도 불구하고 이 방향을 제안하는 이유 — p3/p4는 생략 가능}
```

## 산출물 경로

```
.review-artifacts/{branch-name}/review-comments.md
.review-artifacts/{branch-name}/review-posted.json
```

## review-comments.md 구조

```markdown
# Code Review

## Summary
(전체 코드 품질에 대한 간략한 총평)

## Comments

### [p1] {파일경로}:{라인}
- 근거: ...
- 내용: ...
- 제안: ...
- side effect: ...
- 제안 이유: ...
- github_comment_id: 456

### [p2] {파일경로}:{라인}
...
```
