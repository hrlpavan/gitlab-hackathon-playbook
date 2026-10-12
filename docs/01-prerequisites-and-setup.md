# Chapter 1: Prerequisites, Environment Setup & Git Pitfalls

Setting up a local environment for GitLab development requires special care due to repository size, commit hygiene requirements, and CI linting bots.

---

## 1. Forking & Remote Architecture

GitLab repositories belong to `gitlab-org`. When contributing:
1. Go to `https://gitlab.com/gitlab-org/gitlab` (or your target repo) and click **Fork**.
2. Select your personal namespace or a community fork group.
3. Configure your remotes locally:
   ```bash
   git remote add origin https://gitlab.com/your-username/gitlab.git
   git remote add upstream https://gitlab.com/gitlab-org/gitlab.git
   ```

### Working with Huge Monorepos (Disk Space Strategy)
`gitlab-org/gitlab` is >50 GB with full git history. If you are on limited disk space or need quick setup:
```bash
# Shallow clone for single-branch rapid work
git clone --depth 50 --branch master https://gitlab.com/your-fork/gitlab.git gitlab-source
```

---

## 2. Authentication: Personal Access Tokens (PAT)

When pushing from terminal or querying the GitLab API, use a Personal Access Token:
- Go to `gitlab.com/-/user_settings/personal_access_tokens`.
- Required scopes for hackathon work:
  - `api` (complete read/write API access)
  - `read_user`
  - `read_repository` & `write_repository`
- In terminal:
  ```bash
  git push https://oauth2:<YOUR_TOKEN>@gitlab.com/your-fork/gitlab.git branch-name
  ```

---

## 3. The Danger Bot Commit Convention Trap ⚠️

GitLab runs **`danger-review`** on every single commit.

### The Rule
> Every commit subject line **MUST start with a capital letter**.

❌ **Fails Danger**:
```text
test: simplify test name and drop unused option
fix: resolve non-ascii branch creation
chore: update changelog
```

✅ **Passes Danger**:
```text
Test: Simplify test name and drop unused option
Fix: Resolve non-ASCII branch creation
Chore: Update changelog
```

If you push a lowercase commit, Danger will fail your pipeline with:
`Commit subject must start with a capital letter.`
To fix it:
```bash
git commit --amend -m "Test: Capitalize subject line"
git push --force origin branch-name
```

---

## 4. GPG / SSH Signing Gotchas

If your local Git config has `commit.gpgsign = true` configured pointing to a non-existent or desktop-specific key, git commits will fail with:
`error: gpg failed to sign the data`

In automated scripts or quick environments, you can disable signing explicitly:
```bash
git commit --no-gpg-sign -am "Fix: Your message"
```

---

## 5. Changelog Trailers

For changes that modify user-facing behavior in GitLab core, GitLab requires a changelog trailer in the commit message or an MR label:
```text
Fix workspace clone command for non-ASCII branch names

Closes #596326

Changelog: fixed
```
Common trailers:
- `Changelog: added` (new features)
- `Changelog: fixed` (bug fixes)
- `Changelog: changed` (modifications)
- `Changelog: other` (internal tests/refactoring that don't need a public release note)
