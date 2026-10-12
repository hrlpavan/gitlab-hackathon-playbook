# Chapter 4: Code Reviews, Hidden Threads & Merge Trains

Getting your code written and CI passing is only half the battle. Landing a production merge requires navigating GitLab's multi-stage review process and merge train queues.

---

## 1. The Multi-Tier Review Ladder

1. **GitLab Bot Triage**:
   - The bot assigns labels based on directory paths (`~frontend`, `~backend`, `~database`).
   - It assigns a Community Coach or initial Reviewer.
2. **Reviewer Review**:
   - The reviewer audits code conventions, edge cases, and test coverage.
   - Once satisfied, they click **Approve** and hand off the MR to a Maintainer:
     `@maintainer, could you please perform a maintainer review?`
3. **Maintainer Review & Merge**:
   - Maintainers are the only engineers with write permission to merge into `master`.
   - They will either hit merge directly or add the MR to the **Merge Train**.

---

## 2. Resolving "Hidden" Bot Threads ⚠️

A common roadblock in GitLab MRs:
> Your pipeline is green, your reviewer approved, but the merge button is greyed out with **"All discussions must be resolved"**.

### Why This Happens
When `gitlab-bot` or `GitLab Duo` posts an initial prompt (e.g. `@reviewer, this community contribution is ready for review`), GitLab marks the bot comment as a **resolvable discussion thread**.

If no human clicks **Resolve discussion** on the bot's thread, GitLab treats it as an open blocker!

### How To Fix
1. Scroll through your MR's **Overview** tab.
2. Look for any bot comments with a checkbox or **Resolve discussion** button.
3. Click **Resolve discussion** on every bot thread.
4. Once all threads are resolved, the MR state transitions to `mergeable` or `ready to merge`.

---

## 3. The Merge Train & MWPS (Merge When Pipeline Succeeds)

### What is the Merge Train?
GitLab merges code using a "train" architecture: it simulates the state of `master` with your MR applied on top of other pending MRs and runs a full test pipeline against that merged ref (`refs/merge-requests/<iid>/merge`).

### Merge When Pipeline Succeeds (MWPS)
When a maintainer sets MWPS:
- You will see `merge_when_pipeline_succeeds: true` in the API.
- You do not need to do anything!
- The moment the final job in the test pipeline turns green, GitLab's system automatically executes the merge commit.

---

## 4. Professional Nudging Across Timezones

Maintainers review dozens of community MRs per day. Courteous, well-timed nudges make a huge difference, especially near hackathon deadlines:

### Timing Matters
* **GitLab is 100% Remote & Global**:
  * US West Coast (PDT): Working hours ~9 AM to 5 PM PDT (~9:30 PM to 5:30 AM IST).
  * Europe (CEST): Working hours ~9 AM to 5 PM CEST (~12:30 PM to 8:30 PM IST).
  * APAC: Working hours ~9 AM to 5 PM AEST (~4:30 AM to 12:30 PM IST).
* Ping maintainers when it is morning or afternoon in their local timezone.

### Template: Friendly Handoff Ping
```markdown
Hi @maintainer, following up on @reviewer's review handoff—all feedback has been addressed, threads are resolved, and CI is 100% green. Whenever you have a moment, this is ready for maintainer review and merge. Thank you!
```
Keep it brief, cite the previous reviewer's signoff, and confirm that CI is green.
