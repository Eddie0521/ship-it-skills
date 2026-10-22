# ship-it

[![validate](https://github.com/Eddie0521/ship-it-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Eddie0521/ship-it-skills/actions/workflows/validate.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[中文](README.md) | English

**Make your AI coding agent ship like a reliable engineer: agree on a plan, break it into issues, one PR per issue, merge only when CI is green.**

A set of Agent Skills that works with any agent that reads `SKILL.md`: Claude Code, Codex, Cursor and others.

```bash
npx skills add Eddie0521/ship-it-skills
```

---

## Why

Agents write code fast, and it often goes like this:

- "Add a feature" turns into twenty changed files pushed straight to main.
- CI fails, so the test gets skipped, or the job gets re-run until it passes.
- The plan lives only in a chat transcript and is gone with the session.
- Handing the work to a teammate or another agent means guessing what to give them.

ship-it teaches the agent a proven way of working:

```
new-repo  →  plan-to-issues  →  issue-to-pr  →  pr-to-merge
scaffold      plan, split          one issue,        follow it
              into issues          one PR            until mergeable
                    ↘
                   handoff: give the plan to someone else, then review what comes back
```

The whole idea in one line: **main only holds working code; every piece of work has an issue that says what done means, happens on a branch, ships as a PR, passes CI, and closes its issue on merge.**

## What it looks like

Just talk normally. The `ship-it` entry skill works out where you are and hands off to the right skill.

| You say | Skill | The agent |
| --- | --- | --- |
| "Start a Node CLI project for tracking expenses" | `new-repo` | Scaffolds a passing test, CI, and PR and issue templates, then commits locally. It then asks whether the repo should be public or private and which license to use, and gives you branch-protection steps and a first issue draft. |
| "Let's figure out how to store the data" | `plan-to-issues` | Reads the code first and proposes one approach with its trade-offs. Once you agree, it writes a design doc and drafts issues that can each merge on their own. |
| "Do #3" | `issue-to-pr` | Branches from the latest main, adds code and tests, runs the checks, reviews its own diff, then opens a draft PR with `Closes #3`. |
| "CI on the PR is red" | `pr-to-merge` | Reproduces the failure locally and fixes the root cause. No skipped tests, no re-run roulette. |
| "Hand this plan to another agent" | `handoff` | Makes sure the plan is merged and writes a kickoff brief: what to read, which issue, how to deliver, and when to stop and ask. When the PR comes back, it checks it against the plan. |

**Anything that leaves a trace outside your machine (creating issues, pushing, opening a PR, merging) is shown to you first and waits for your OK.**

## Skills

| Skill | Use it when | What it does |
| --- | --- | --- |
| `ship-it` | Entry point; you don't call it directly | Routes to the right skill and sets the shared rules |
| `new-repo` | New project or empty repo | README, a passing test, CI, PR and issue templates, `.gitignore`, branch-protection steps |
| `plan-to-issues` | You have an idea, or someone handed you a spec | Turns it into a plan (a design doc for big changes), then into issues that can merge independently |
| `issue-to-pr` | There is a clear issue or small task | Branch, small commits, early draft PR, `Closes #N`, self-check before pushing |
| `pr-to-merge` | The PR has conflicts, red CI or review comments | Works through conflicts, then CI, then review; finds root causes; keeps going until it's mergeable |
| `handoff` | The plan is going to someone else or another agent | Picks the delivery format, writes the kickoff brief, reviews the result against tests, invariants and the plan |

## Principles

- **Ask before acting outside your machine.** Local work (branches, code, tests) just happens. Anything that leaves a trace or notifies people is proposed first.
- **The repo's own rules win.** `CONTRIBUTING.md`, PR templates and `AGENTS.md` / `CLAUDE.md` override the skills' defaults.
- **Never:** skip or disable tests to get green, push empty commits to re-trigger CI, force-push someone else's branch, commit secrets, or merge without your OK.
- **Keep the source of truth in the repo.** Plans go in docs, tasks in issues, progress in PRs, so a new person or agent can pick up without losing context.
- **Agent-agnostic.** No assumption that a specific tool exists: use it if it's there, fall back if not.

## Install

### `npx skills add` (recommended, any agent)

```bash
npx skills add Eddie0521/ship-it-skills                                 # interactive
npx skills add Eddie0521/ship-it-skills --list                          # list skills only
npx skills add Eddie0521/ship-it-skills -s '*' -a codex -y              # all skills to Codex, no prompts
npx skills add Eddie0521/ship-it-skills -s ship-it -s issue-to-pr -g    # two skills, user level
```

If you install only some of the skills, include the `ship-it` entry skill.

### Claude Code plugin

```bash
claude plugin marketplace add Eddie0521/ship-it-skills
claude plugin install ship-it@ship-it-skills
```

### Manual

Copy the folders under `plugins/ship-it/skills/` into your agent's skills directory, for example `~/.claude/skills/` or `.agents/skills/`. Keep them side by side, because the skills reference each other as sibling folders.

## Scope

- **GitHub-first**: issues, PRs and Actions. The ideas carry over to other hosts; the commands don't.
- **From idea to merged into main.** Deployments, release tags and publishing to npm are out of scope.
- **Trunk-style branching** (main plus short-lived branches). If a repo uses long-lived develop or release branches, the skills follow the repo's convention.
- **The skill bodies are written in Chinese.** Agents read them fine, and the agent replies in your language.

## Contributing

This repo uses its own workflow: issue → branch → PR → CI (`scripts/validate.py`) → merge. Issues and PRs are welcome. Run `python scripts/validate.py` before committing.

## License

[MIT](LICENSE)
