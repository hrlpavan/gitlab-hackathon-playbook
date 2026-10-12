# Chapter 2: Issue Discovery, Rule 2 & Self-Assignment

In the GitLab Hackathon, **Rule 2** states that contributors must be assigned to an issue before opening or merging merge requests for it. Failing to assign yourself can lead to warnings or disqualification.

---

## 1. The "@gitlab-bot assign" Trap

When newcomers want to claim an issue, they often post:
`@gitlab-bot assign` or `@gitlab-bot assign me`

### Why This Fails
`gitlab-bot` (Triage Bot) **does not have an assign command** for public community members on `gitlab-org` issues. The comment is treated as plain text, no action is taken, and the issue remains completely unassigned.

---

## 2. The Official Self-Assignment Engine: `contributors.gitlab.com`

GitLab built a dedicated portal for community contributors: **[contributors.gitlab.com](https://contributors.gitlab.com)**.

When you sign in with your GitLab.com account on the portal, an authorized backend service can assign you to issues with **one click**.

### Direct Link Format
You do not need to hunt through paginated lists. You can construct direct URLs for any issue:

```text
https://contributors.gitlab.com/manage-issue?projectPath=<PROJECT_PATH>&issueIid=<ISSUE_IID>&action=work
```

### Examples:
- **GitLab Core Issue #601059**:
  `https://contributors.gitlab.com/manage-issue?projectPath=gitlab-org/gitlab&issueIid=601059&action=work`
- **GitLab LSP Issue #2596**:
  `https://contributors.gitlab.com/manage-issue?projectPath=gitlab-org/editor-extensions/gitlab-lsp&issueIid=2596&action=work`
- **Omnibus GitLab Issue #841**:
  `https://contributors.gitlab.com/manage-issue?projectPath=gitlab-org/omnibus-gitlab&issueIid=841&action=work`

Clicking this link while logged in presents an **"Assign me"** button. Clicking it executes the assignment instantly.

---

## 3. The Platform Cap (Concurrent Limit)

To prevent users from hoarding issues or claiming dozens of tasks they never finish, the Contributor Platform enforces an assignment cap (typically **8 to 10 active issues** across all projects).

If you click "Assign me" after reaching the limit, the platform will notify you that you have reached the maximum allowed concurrently assigned issues.

### What To Do When You Reach The Cap
The official Hackathon rule includes a sanctioned fallback:
> *"The way to do it is the issue finder on contributors.gitlab.com, it assigns you to quick win issues with one click, **or you ask in the issue and wait until a human assigns you**."*

In the issue thread, post a polite, transparent comment:
```markdown
Hi team! I am working on the fix for this issue in MR !<MR_NUMBER>.
Could a team member or maintainer please assign this issue to me for the GitLab Hackathon? Thank you!
```

This ensures complete compliance with hackathon rules even if your platform slots are full.

---

## 4. Avoiding Duplicate Work

Before beginning any code work on an issue:
1. Search the issue's comments for other contributors saying they are working on it.
2. Check the **Linked items / Related merge requests** section on the right sidebar of the GitLab issue.
3. If an MR is already open and actively being reviewed, **do not open a duplicate MR**. Pick another issue.
