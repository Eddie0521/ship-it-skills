---
name: new-repo
description: 给新项目（或刚建、几乎是空的仓库）搭好 issue/PR 工作流的骨架：README、可运行的测试命令、CI（GitHub Actions）、PR 模板、issue 模板、.gitignore、分支保护的设置步骤，以及第一批 issue。用户说"新开一个项目""帮我建个仓库""初始化项目""项目刚起步想规范一点""加个 CI""加 PR 模板"时用这个技能，即使用户只提了其中一两样。English — bootstrap a new repo, scaffold project with CI and PR template, set up branch protection.
---

# new-repo：给新项目搭骨架

目标：**第一天就让"不走 PR、不过 CI 就进不了 main"成立**。骨架越晚搭，越多代码是在没人把关的情况下写进去的。

> 共用规矩（详见 `ship-it` 技能）：对外操作（建远程仓库、推送、改仓库设置、建 issue）先给方案、等确认；本地文件和本地提交可以直接做，做完汇报。仓库已有的规矩优先。

## 1. 先问清楚（缺什么问什么，能从上下文看出来的不要问）

- 语言 / 运行时（Node、Python、Go……），以及包管理器。
- 仓库放哪：已经有远程仓库了吗？公开还是私有？
- 一个人做还是多人协作（决定分支保护要多严格）。

## 2. 要建的文件

按技术栈从 `assets/` 里挑模板，改成项目的实际情况（项目名、命令、版本号），不要原样照抄占位符。

| 文件 | 内容 | 模板 |
| --- | --- | --- |
| `README.md` | 这是什么、怎么装、怎么跑、怎么测试、怎么贡献（指向流程） | 按项目现写 |
| 测试命令 | 哪怕只有一个冒烟测试，也要让 `npm test` / `pytest` / `go test ./...` 能跑通并且是绿的 | 按项目现写 |
| `.github/workflows/ci.yml` | 推送和 PR 时：装依赖 → lint（如果有）→ 测试 | `assets/ci-node.yml`、`assets/ci-python.yml`、`assets/ci-generic.yml` |
| `.github/pull_request_template.md` | 做了什么 / 关联 issue / 怎么验证 / 回滚 / 风险 | `assets/pull_request_template.md` |
| `.github/ISSUE_TEMPLATE/` | 任务和 bug 两种 | `assets/issue-task.md`、`assets/issue-bug.md` |
| `.gitignore` | 依赖目录、构建产物、`.env`、本地数据、编辑器文件 | 按技术栈现写 |
| `LICENSE` | 公开仓库要有；问用户选哪种，不确定就推荐 MIT | — |

为什么测试命令必须先跑通：CI 第一次跑就红，大家会习惯性忽略红色，CI 就废了。

## 3. 第一个提交

骨架是唯一可以直接进 main 的提交（还没有 main 可以 PR 进去）。

1. `git init -b main`（已有仓库就跳过），本地提交：`chore: 项目骨架`。
2. **给用户看**：文件列表 + 关键文件内容（CI、PR 模板），确认后再推送。
3. 还没有远程仓库的：给出建仓命令或网页步骤，用户确认后再建。公开仓库要特别提醒：推上去就是全世界可见。
4. 推送后看一眼 Actions 页面，第一次 CI 要是绿的。是红的就先修，再做下一步。

## 4. 分支保护

这一步在 GitHub 网页上做，或者用 API。**改的是仓库设置，要用户确认**。

网页：仓库 → Settings → Branches（或 Rules → Rulesets）→ 给 `main` 加规则：
- 合并前必须走 Pull Request；
- 必须通过状态检查，选上 CI 那个 job；
- 多人协作再加：至少 1 个批准；有新提交时作废旧的批准。
- 一个人的项目：不勾"需要批准"（自己不能批准自己），但前两条要留。

给用户写清楚点哪里；如果有 `gh` 命令行并且用户同意，也可以用 `gh api` 设置。

## 5. 第一批 issue

如果用户已经说了要做什么，转 `plan-to-issues` 拆 issue。没有的话，至少建议一个："写第一个真正的功能 + 测试"，让流程马上转起来。

## 6. 交付时告诉用户

- 建了哪些文件、各自干什么（一句话）。
- 之后每件事怎么走：开 issue → 开分支 → 开 PR（写 `Closes #N`）→ CI 绿 → 合并。
- 还有哪些需要他亲手做的（比如分支保护、仓库可见性）。
