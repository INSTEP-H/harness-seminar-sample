---
name: create-pr-body
description: 구현 완료된 코드의 git diff와 spec 변경사항을 기반으로 PR 본문 초안을 생성하고, 실제 GitHub PR을 생성한다. worktree(fork)에서 실행된다.
---

# PR 본문 생성 + GitHub PR 생성

구현 완료된 코드의 git diff와 spec 변경사항을 기반으로 PR 본문을 생성하고, 확정 후 실제 GitHub PR을 생성한다.

## 실행 방식

이 skill은 worktree(fork)에서 실행된다.

## 사전 조건

- `gh` CLI 인증 완료 (`gh auth status`로 확인 가능).
- 현재 branch는 base branch와 다른 변경사항이 있어야 한다.

## 절차

### A. PR 본문 작성

1. base branch(기본: `main`) 대비 현재 branch의 git diff를 수집한다.
   ```
   git diff {base}...HEAD
   ```
2. 변경된 파일 목록과 각 파일의 변경 내용을 분석한다.
3. 아래 구조에 맞춰 PR 본문 초안을 작성한다.
4. 초안을 사용자에게 제시하되, **PR 설명에서 명확히 해야 할 논의점**을 반드시 함께 정리한다.
   - 예: "breaking change 여부", "마이그레이션 필요 여부", "관련 이슈 번호"
5. 사용자 피드백을 반영하여 확정한다.
6. 확정된 문서를 `.review-artifacts/{branch-name}/pr-body.md`에 저장한다.

### B. GitHub PR 생성

1. 현재 branch가 origin에 push되어 있는지 확인한다. 없으면 push한다.
   ```
   git rev-parse @{upstream} 2>/dev/null || git push -u origin HEAD
   ```
2. 같은 head/base 조합으로 이미 열린 PR이 있는지 확인한다.
   ```
   gh pr list --head {head-branch} --base {base} --state open --json number,url
   ```
3. 없으면 새 PR 생성, 있으면 body만 업데이트한다.
   - 새 PR:
     ```
     gh pr create --base {base} --head {head-branch} \
       --title "{PR 제목}" \
       --body-file .review-artifacts/{branch-name}/pr-body.md \
       --draft
     ```
   - 기존 PR 업데이트:
     ```
     gh pr edit {number} --body-file .review-artifacts/{branch-name}/pr-body.md
     ```
4. PR 메타정보를 `.review-artifacts/{branch-name}/pr.json`에 저장한다.
   ```json
   {
     "number": 1234,
     "url": "https://github.com/owner/repo/pull/1234",
     "base": "main",
     "head": "feature-x",
     "head_sha": "abc1234...",
     "repo": "owner/repo"
   }
   ```
   `head_sha`는 `gh pr view {number} --json headRefOid -q .headRefOid`로 얻는다.
5. PR URL을 사용자에게 보고한다.

## 산출물 경로

```
.review-artifacts/{branch-name}/pr-body.md
.review-artifacts/{branch-name}/pr.json
```

## 문서 구조 (pr-body.md)

```markdown
# PR: {제목}

## Summary
(이 PR이 해결하는 문제와 접근 방식 요약, 1-3문장)

## Changes
(변경된 파일/모듈 단위로 무엇이 어떻게 바뀌었는지)

### {모듈/영역}
- ...

## Breaking Changes
(없으면 "없음")

## Test Plan
- [ ] ...

## Related
(관련 이슈, ADR, 설계 문서 등)
```
