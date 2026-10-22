---
name: issue-to-pr
description: 把一个 issue 或小任务做成一个可合并的 PR：读 issue、从最新的 main 开分支、小步提交、尽早开草稿 PR、写 Closes #N、推送前自证（测试 / lint / 自查 diff）、按模板写 PR 描述，CI 绿后转为可评审，等确认后合并并关闭 issue。用户说"做一下 #12""按这个 issue 写代码""修这个 bug 并提 PR""实现这个功能"，或者明显要改代码交付时用这个技能。English — implement an issue, open a pull request, ship a task, fix and submit PR.
---

# issue-to-pr：一个 issue → 一个 PR

> 共用规矩（详见 `ship-it` 技能）：推送、开 PR、转为可评审、合并之前给用户看并等确认；本地建分支、改代码、跑测试、本地提交可以直接做，做完汇报。

## 1. 开工前

- **读 issue**：目标是什么？"怎么算做完"列了哪些？有依赖的 issue 没合并吗？验收标准不清楚就先问，别自己脑补。
- **读仓库的规矩**：PR 模板、CONTRIBUTING、AGENTS.md / CLAUDE.md 这类给 agent 的说明、提交信息格式（看 `git log`）、测试和 lint 命令（看 CI 配置）。
- **从最新的 main 开分支**：
  ```bash
  git fetch origin
  git checkout -b <类型>/<issue号>-<简短描述> origin/main     # 例：fix/12-login-timeout
  ```
  分支名按仓库惯例；没有惯例就用 `feat/`、`fix/`、`docs/`、`chore/` 加 issue 号。
- **给 fork 来的原项目提 PR 时**：分支要从原项目的最新 main 拉（`git remote add upstream <原仓库>`、`git fetch upstream`，从 `upstream/main` 开分支），不要从你 fork 里可能落后的 main 拉；按原项目的 CONTRIBUTING 来；PR 的 base 是原项目的 main，head 是你 fork 上的分支。

## 2. 做的过程中

- **先确认现状**：先跑一遍测试，知道哪些本来就是红的，免得之后算到自己头上。
- **小步提交**：每个提交做一件能说清楚的事，提交信息说"为什么"。
- **代码写得像周围的代码**：命名、注释密度、错误处理的方式都照着来。
- **测试跟着改**：issue 的每条验收标准，尽量都有对应的测试。修 bug 先写一个能复现它的测试，看它变红，再修到绿。
- **不顺手做别的事**：发现无关的问题，记下来，建议另开 issue。
- **尽早开草稿 PR**（用户确认后）：有了第一个像样的提交就可以开。CI 会早早开始跑，方向不对也能早点被看到。

## 3. 推送前自证

1. 跑仓库自己的全部检查：测试、lint、类型检查、格式化。
2. 用挑刺的眼光读一遍 `git diff origin/main...HEAD`：
   - 有没有调试代码、`console.log`、注释掉的代码、密钥？
   - 有没有改了无关的文件？
   - CI 会因为什么拒绝它？
   - issue 的每条验收标准都满足了吗？
3. 有界面改动的，截前后对比图。

## 4. PR 描述

仓库有模板就按模板填；没有就用这个结构：

```markdown
## 关联 issue
Closes #12

## 做了什么
- 

## 和 issue / 设计不一致的地方
（没有就写"无"）

## 怎么验证的
- 测试：（命令 + 结果）
- 新增的测试：
- 截图：（有界面改动时）

## 怎么回滚

## 风险 / 遗留
```

`Closes #12`（或 `Fixes`、`Resolves`）写在 PR 描述里，PR 合进默认分支时 GitHub 会自动关闭这个 issue。一个 PR 关多个 issue，就每个写一行。

## 5. 收尾

1. CI 绿了 → 把草稿转为可评审（用户确认后）。
2. 有评审意见、冲突或 CI 变红 → 转 `pr-to-merge`。
3. 可以合并时，向用户汇报：CI 状态、评审状态、会关掉哪些 issue、合并方式（merge / squash / rebase，按仓库惯例）。**用户确认后再合并**。
4. 合并后：确认 issue 已自动关闭；删除远程分支（如果仓库没自动删）；本地切回 main 并拉取更新。
