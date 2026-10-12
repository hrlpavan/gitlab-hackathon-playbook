# Chapter 5: Hackathon Strategy & Leaderboard Optimization

Winning or placing in the top tiers of the GitLab Hackathon requires balancing deep engineering work with smart tactical prioritization over 48 hours.

---

## 1. Score Composition Breakdown

Understanding where points come from:

### 1. Merged Code MRs (+130 Points each)
- **The Core Engine**: This is where real reputation and major point chunks are won.
- **Cycle Time**: Takes between 4 to 24 hours from opening to final merge (due to CI runtime + reviewer turnarounds).
- **Strategy**: Open your complex code MRs in the first 24 hours of the hackathon so reviewers have ample time to process them.

### 2. Merged Documentation MRs (+25 Points each)
- **Fast Turnaround**: Documentation updates in `gitlab-docs`, markdown guides, or typo/link fixes require very fast pipelines and technical writer reviews.
- **Strategy**: Great for filling gaps between coding sessions or during the final sprint hours.

### 3. Translation / Localization (CrowdIn / Weblate)
- **Volume Bursts**: Translating strings on CrowdIn generates activity points without requiring individual MR review cycles.
- **Post-Hackathon Audits**: GitLab community coordinators audit bulk translation contributions after cutoff to prevent machine-generated spam. Genuine localization, however, is heavily rewarded.

---

## 2. The 48-Hour Tactical Timeline

| Phase | Window | Focus Area |
| :--- | :--- | :--- |
| **Phase 1: Discovery & Lock-in** | Hours 0 – 12 | Find 5–8 high-probability issues on `contributors.gitlab.com`. Self-assign immediately. Start local branches. |
| **Phase 2: Code & Open MRs** | Hours 12 – 24 | Complete implementations, write unit tests, verify Danger commit conventions, push, and open MRs with `Closes #issue`. |
| **Phase 3: CI Hardening & Reviews** | Hours 24 – 36 | Monitor pipelines closely. Fix any flaky or failing specs. Reply to reviewer comments within 30 minutes. |
| **Phase 4: Maintainer Handoffs & Merge Trains** | Hours 36 – 44 | Ensure all bot threads are resolved. Nudge maintainers politely. Get MRs onto the merge train. |
| **Phase 5: The Final Sprint** | Hours 44 – 48 | While waiting for merge train queues to complete, submit quick documentation fixes or CrowdIn translations. |

---

## 3. Tier Rewards & The Long-Term Game

GitLab Hackathons are **tiered**, not winner-take-all:
- Reaching qualifying merged MR milestones unlocks **Contributor Store credits** (redeemable for mechanical keyboards, laptops, gear, and official merchandise).
- High placement earns you badges, Hall of Fame recognition, and direct relationships with GitLab engineers.
- Every merged MR in GitLab core becomes permanent public proof of enterprise software engineering mastery on your profile.
