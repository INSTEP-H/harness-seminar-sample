---
name: reflect-review
description: GitHub PR에 게시된 [reviewer] 리뷰 코멘트를 검토하여 수용/거부를 판단하고, 수용한 코멘트는 코드를 수정하여 commit 해시를 답글로, 거부한 코멘트는 거부 사유를 답글로 남긴다.
---

# 리뷰 반영

GitHub PR에 게시된 `[reviewer]` 리뷰 코멘트를 검토하고, 각 코멘트에 대해 코드 수정 여부를 결정한다. 수정한 항목은 commit 해시를, 거부한 항목은 사유를 답글(reply)로 남긴다.

## 실행 방식

이 skill은 worktree(fork)에서 실행된다.
구현 컨텍스트가 보존된 상태에서 실행되어야 한다.

## 사전 조건

- `.review-artifacts/{branch-name}/pr.json`, `review-posted.json` 존재.
- `gh` CLI 인증 완료.
- 현재 branch가 origin에 push되어 있어야 한다 (반영 후 추가 commit을 push해야 PR에 반영됨).

## 절차

### A. 리뷰 코멘트 수집

1. `pr.json`에서 PR number와 repo를 읽는다.
2. PR의 모든 review comment를 가져온다.
   ```
   gh api /repos/{owner}/{repo}/pulls/{number}/comments
   ```
3. body가 `[reviewer]`로 시작하는 코멘트만 대상으로 한다 (사람·다른 봇 코멘트 제외).
4. 이미 답글이 달린 코멘트는 제외한다 (in_reply_to_id가 해당 코멘트를 가리키는 다른 코멘트가 있으면 처리 완료로 간주).
   ```
   # 처리 안 된 reviewer 코멘트만 추리는 로직:
   # comments 중 body가 "[reviewer]"로 시작하면서,
   # 다른 comment의 in_reply_to_id가 자기 id를 가리키지 않는 항목.
   ```

### B. 코멘트별 판단

각 코멘트에 대해:

1. body에서 priority(p1~p4)를 추출한다.
2. code-quality-guide.md, design-intent.md를 참고하여 수용/거부를 판단한다.
   - `p1` 항목은 기본 수용. 거부 시 명확한 근거 필요.
   - `p2` 항목은 판단과 근거를 제시하고 사용자 확인.
   - `p3` 항목은 판단을 제시하되 사용자 재량.
   - `p4` 항목은 일괄 수용 또는 무시.
3. 사용자에게 판단 결과를 일괄 제시하고 확인을 받는다.
   - p1은 자동 수용 의도, p2~p4는 명시적 확인 권장.

### C. 수용한 코멘트 처리

1. 코드를 수정한다.
2. 코멘트 단위 또는 묶음 단위로 commit한다 (관련 있는 수정은 묶어서 1 commit).
   commit message 예: `fix(review): apply p2 comment - {요약}`
3. commit 후 push한다.
   ```
   git push
   ```
4. push 완료 후 commit 해시(short)를 얻는다.
   ```
   COMMIT_SHA=$(git rev-parse --short HEAD)
   ```
5. 해당 review comment에 답글을 게시한다.
   ```
   gh api -X POST /repos/{owner}/{repo}/pulls/{number}/comments \
     -f body="반영 완료: {COMMIT_SHA} - {적용 요약}" \
     -F in_reply_to={comment_id}
   ```
   - body 예: `반영 완료: a1b2c3d - extractPaymentData() 함수로 분리`

### D. 거부한 코멘트 처리

1. 거부 사유를 명확히 작성한다 (단순 "동의 안 함" 금지, 설계의도·트레이드오프 근거).
2. 답글로 게시한다.
   ```
   gh api -X POST /repos/{owner}/{repo}/pulls/{number}/comments \
     -f body="반영하지 않음. 이유: {사유}" \
     -F in_reply_to={comment_id}
   ```
   - body 예: `반영하지 않음. 이유: 현재 구조에서 분리하면 호출 경로가 3단계로 늘어나 가독성이 떨어짐. design-intent.md의 "최소 추상화" 원칙 참조.`

### E. QA + 보고

1. 코드 수정이 끝나면 QA를 수행한다.
   - 빌드 확인 (`pnpm build` 또는 프로젝트 표준 명령)
   - 테스트 실행 (`pnpm test`)
   - 버그 발견 시 수정 루프 (수정 → QA → 재확인)
2. `.review-artifacts/{branch-name}/review-comments.md`에 각 코멘트의 판정과 commit 해시를 추가한다.
3. 핵심 변경사항(반영 코멘트 수, 거부 코멘트 수, 추가된 commit 목록, QA 결과)을 사용자에게 보고한다.

## 산출물 경로

```
.review-artifacts/{branch-name}/review-comments.md  (판정 추가하여 갱신)
```

## 판정 형식 (review-comments.md 갱신)

각 코멘트 하단에 판정과 답글 commit 해시를 추가한다:

```markdown
### [p1] src/payment/service.ts:42
- 근거: ...
- 내용: ...
- 제안: ...
- github_comment_id: 456
- **판정: ACCEPT**
- 반영 commit: a1b2c3d
- 답글: "반영 완료: a1b2c3d - extractPaymentData() 함수로 분리"
```

```markdown
### [p2] src/payment/controller.ts:15
- 근거: ...
- 내용: ...
- 제안: ...
- github_comment_id: 789
- **판정: REJECT**
- 거부 사유: 현재 구조에서 분리하면 오히려 복잡도가 증가함. design-intent.md 참조.
- 답글: "반영하지 않음. 이유: ..."
```
