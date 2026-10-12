# Chapter 3: Writing Code & Passing GitLab CI

GitLab CI is notoriously thorough. A standard merge request pipeline runs dozens of linters, security scanners, predictive test runners, and cross-framework integration tests.

---

## 1. Understanding Key Pipeline Stages

| Stage | Common Jobs | What They Check |
| :--- | :--- | :--- |
| **prepare** | `detect-tests`, `retrieve-tests-metadata` | Calculates predictive test sets based on git diff |
| **lint** | `danger-review`, `eslint`, `haml-lint`, `rubocop` | Code style, commit messages, security rules |
| **test-frontend** | `jest predictive 1/4..4/4`, `jest vue3 predictive` | Unit and component specs in Jest / Vue Test Utils |
| **test** | `rspec-ee unit`, `rspec-ee integration`, `rspec system` | Rails backend specs against PostgreSQL |
| **post-test** | `rspec:coverage`, `fail-pipeline-early` | Code coverage thresholds |

---

## 2. Frontend Case Study: Apollo GraphQL Field Stripping

### The Symptom
In Vue 3 / Jest specs using `createMockApollo`, you pass a complete mock response:
```javascript
const mockResponse = {
  data: {
    aiCatalogItem: {
      ...mockAgent,
      configurationForProject: mockAgentConfigurationForProject,
      configurationForGroup: mockItemConfigurationForGroup,
    }
  }
};
```
However, asserting `expect(resolveVersionSpy).toHaveBeenCalledWith(mockResponse.data.aiCatalogItem)` fails in tests:
```text
- Expected: contains "configurationForGroup"
+ Received: does NOT contain "configurationForGroup"
```

### The Root Cause
In GraphQL query definitions, specific fields often contain conditional directives:
```graphql
configurationForGroup(groupId: $groupId) @include(if: $hasGroup) { ... }
```
When a test mounts the component in an explore area (`isGlobalNamespace: true`), `$hasGroup` evaluates to `false`. Apollo Client's mock execution engine **strips** `@include(if: false)` fields from the emitted result before passing it to computed properties!

### The Solution
Use Jest's `expect.objectContaining()` against the base object rather than demanding stripped fields:
```javascript
expect(resolveVersionSpy).toHaveBeenCalledWith(expect.objectContaining(mockItem), {
  isGlobalNamespace: true,
  isGroupNamespace: false,
});
```

---

## 3. Backend Case Study: Validating API Parameters

### The Problem
API endpoints using Grape or Rails controllers may accept zero or negative integers in pagination parameters (`page=0` or `page=-1`), causing database query syntax errors or unexpected behavior.

### The Fix
Add explicit validation constraints:
```ruby
params do
  requires :id, type: String, desc: 'The ID of the project'
  optional :page, type: Integer, values: ->(v) { v > 0 }, default: 1, desc: 'Current page number'
  optional :per_page, type: Integer, values: ->(v) { v > 0 && v <= 100 }, default: 20, desc: 'Number of items per page'
end
```
Always pair backend changes with an RSpec test:
```ruby
it 'returns 400 Bad Request when page is 0 or negative' do
  get api("/projects/#{project.id}/repository/branches", user), params: { page: 0 }

  expect(response).to have_gitlab_http_status(:bad_request)
end
```

---

## 4. Retrying Flaky Jobs and Bridge Downstreams

Sometimes an upstream bridge job like `start-as-if-foss` fails due to a runner system error (`runner_system_failure`) rather than your code.

- **On Community Forks**: If an upstream pipeline fails on `refs/merge-requests/.../merge`, you cannot directly retry maintainer jobs with 403 Forbidden.
- **The Solution**: Rebase your branch against the latest `upstream/master` and force-push. This triggers a fresh pipeline clean of stale master artifacts:
  ```bash
  git fetch upstream master
  git rebase upstream/master
  git push --force origin your-branch
  ```
