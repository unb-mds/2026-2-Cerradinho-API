---
name: git-workflow
description: Create a commit, branch, issue, or pull request in this repo. Use for any git/GitHub action to follow Cerradinho's branching model, commit convention, and PR/issue policy from CONTRIBUTING.md.
---

# Git & GitHub workflow

**Source:** adapted from
[`github/awesome-copilot/git-commit`](https://www.skills.sh/github/awesome-copilot/git-commit)
("Standardized git commits using Conventional Commits specification with intelligent
diff analysis... auto-detects commit type and scope from actual code changes") for the
commit step, and
[`gentleman-programming/gentleman-skills/github-pr`](https://skills.sh/gentleman-programming/gentleman-skills/github-pr)
for the PR step, both scoped to this repo's actual policy in `CONTRIBUTING.md`.

Repo: `github.com/unb-mds/2026-2-Cerradinho-API`, monorepo with `/frontend` and `/backend`
(`CONTRIBUTING.md` §1).

## Branching

`main` (stable) → `dev` (integration) → `R2-nome` (one long-lived branch per person for
Release 2, e.g. `R2-gabriel`: first name, lowercase, no accents). Don't create
per-task `feature/...`, `fix/...` or `docs/...` branches anymore; commit on the user's
own `R2-nome` branch (create it off an up-to-date `dev` if it doesn't exist yet). Each
deliverable is a PR from `R2-nome` into `dev`, and the branch stays open after the merge.
Before starting a task and before opening a PR, bring `dev` into the branch
(`git pull origin dev`) and resolve conflicts there. Never commit directly to `dev` or
`main`; PRs into `main` come only from `dev`, unless the user says otherwise.

## Commits

Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `build:`,
`ci:`, `revert:`) — auto-detect the type and scope from the actual diff being committed
rather than defaulting to `feat`/`fix` out of habit, per the `git-commit` skill's
approach. Match the
existing commit history's style (Portuguese commit subjects, e.g. `docs: adição de
estudo de HTML`, `fix: ajusta nome do arquivo de template da issue`). Flag breaking
changes explicitly (`!` after the type, or a `BREAKING CHANGE:` footer) rather than
burying them in the description.

## Issues

- Every issue needs an acceptance criterion, a size label (S/M/L/XL), and a type label
  (feature, fix, docs, devops).
- Use the templates in `.github/ISSUE_TEMPLATE/` — don't free-form a new issue body when
  a template fits (bug report, feature request, tarefa técnica).

## Pull requests

- Use `.github/PULL_REQUEST_TEMPLATE.md`.
- **Every PR needs a formal, recorded review** — a comment or approval on the PR itself.
  A review that happened in chat/verbally does *not* count as evidence per
  `CONTRIBUTING.md` §3 — never treat an out-of-band "looks good" as sufficient to merge
  without also getting it recorded on the PR.
- Link the PR to its issue/Story Map fields (`Journey`, `Step`) where applicable — see
  `docs/PROCESSO.md` §5 for the Story Map field convention if creating new issues that
  should appear on the board.

## AI-assisted contributions

Any AI contribution to implementation, tests, docs, or refactoring must be logged in
`AI-USAGE.md` — see the `ai-usage-log` skill. This is a course policy, not optional
project hygiene: treat "did you log the AI usage" as part of finishing the PR, not an
afterthought.
