# ship-it

[![validate](https://github.com/Eddie0521/ship-it-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Eddie0521/ship-it-skills/actions/workflows/validate.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

中文 | [English](README.en.md)

**让 AI 编程助手像靠谱的工程师一样交付：先有方案，再拆 issue，一件事一个 PR，CI 绿了才合并。**

一套 agent 技能（Agent Skills），Claude Code、Codex、Cursor 等支持 `SKILL.md` 的 agent 都能用。

```bash
npx skills add Eddie0521/ship-it-skills
```

---

## 为什么需要它

让 AI 写代码很快，但很容易变成这样：

- 一句"帮我加个功能"，改了二十个文件，直接推到 main；
- CI 挂了，就把测试跳过，或者一遍遍重跑；
- 方案只存在聊天记录里，换个会话就没了；
- 想把活交给另一个人或另一个 agent，不知道该给什么。

ship-it 把一套成熟的工作方式教给 agent：

```
new-repo  →  plan-to-issues  →  issue-to-pr  →  pr-to-merge
 搭骨架        讨论方案、拆 issue    一个 issue 一个 PR    跟到能合并
                    ↘
                   handoff：交给别人或另一个 agent 去做，再验收回来
```

核心只有一句话：**main 只放能用的版本；每件事都有一个 issue 说清楚要什么，在分支上做，用 PR 交付，CI 把关，合并时顺手关掉 issue。**

## 用起来是什么样

装好以后不用记命令，照常说话就行，入口技能 `ship-it` 会判断你在哪一步。比如：

> **你**：我想做个命令行记账工具，用 Node，先把项目搭起来。
>
> **agent**（`new-repo`）：建好 `package.json`、一个能跑通的测试、CI、PR 模板和 issue 模板，在本地提交。然后停下来问你：仓库公开还是私有？用什么许可证？并附上分支保护的设置步骤，和第一个 issue 的草稿。

> **你**：我们讨论下记账的数据怎么存。
>
> **agent**（`plan-to-issues`）：先读代码，给出一个有倾向的方案和取舍，列出需要你拍板的点。定稿后写进 `docs/`，拆成 4 个能各自独立合并的 issue，给你看过再建。

> **你**：做一下 #3。
>
> **agent**（`issue-to-pr`）：从最新的 main 开分支，写代码和测试，跑完检查，自查一遍 diff，开一个写了 `Closes #3` 的草稿 PR。

> **你**：PR 的 CI 挂了。
>
> **agent**（`pr-to-merge`）：先在本地复现，找到根因再修，不跳过测试，也不靠重跑碰运气。

> **你**：这个方案交给另一个 agent 去实现吧。
>
> **agent**（`handoff`）：确认方案已经合并进 main，写一份开工指令：读什么、做哪个 issue、怎么交付、什么情况必须停下来问人。给你看过之后再派出去，交回的 PR 按方案逐条验收。

**所有对外操作，比如建 issue、推送、开 PR、合并，agent 都会先给你看草稿或 diff，等你点头再做。**

## 技能一览

| 技能 | 什么时候用 | 做什么 |
| --- | --- | --- |
| `ship-it` | 入口，不用手动调 | 判断你在哪一步，转给下面的技能；定下所有技能共用的规矩 |
| `new-repo` | 新项目、空仓库 | README、能跑通的测试、CI、PR 和 issue 模板、`.gitignore`、分支保护步骤 |
| `plan-to-issues` | 有想法要讨论；或者拿到别人给的需求 | 讨论出方案，大事先写设计文档，再拆成能独立合并的 issue |
| `issue-to-pr` | 有一个明确的 issue 或小任务 | 开分支、小步提交、尽早开草稿 PR、`Closes #N`、推送前自证 |
| `pr-to-merge` | PR 有冲突、CI 红了、有评审意见 | 按"冲突 → CI → 评审"的顺序处理，找根因，直到能合并 |
| `handoff` | 方案要交给别人或另一个 agent | 选交付形式、写开工指令、按测试 / 不变量 / 方案偏差验收 |

## 设计原则

- **对外操作先确认**：本地的事（建分支、写代码、跑测试）直接做；会留下痕迹或通知别人的事，先给方案。
- **仓库自己的规矩优先**：`CONTRIBUTING.md`、PR 模板、`AGENTS.md` / `CLAUDE.md` 说了算，技能只是默认做法。
- **绝不**：跳过或禁用测试来让 CI 变绿，推空提交触发 CI，在别人的分支上 force-push，提交密钥，未经确认就合并。
- **源头留在仓库里**：方案进文档，任务进 issue，进度在 PR。换人、换 agent 都不丢上下文。
- **和具体 agent 无关**：不假设一定有某个工具，写法是"有就用，没有就退一步"。

## 安装

### `npx skills add`（推荐，任何 agent）

用 [skills](https://github.com/vercel-labs/skills) 命令行安装。它会列出 6 个技能，检测你装了哪些 agent，让你勾选：

```bash
npx skills add Eddie0521/ship-it-skills
```

常用参数：

```bash
npx skills add Eddie0521/ship-it-skills --list                          # 只看有哪些技能
npx skills add Eddie0521/ship-it-skills -s '*' -a codex -y              # 全部装给 Codex，不提问
npx skills add Eddie0521/ship-it-skills -s ship-it -s issue-to-pr -g    # 只装两个，装到用户级
```

只装一部分时，建议带上入口 `ship-it`。

### Claude Code 插件

```bash
claude plugin marketplace add Eddie0521/ship-it-skills
claude plugin install ship-it@ship-it-skills
```

技能名会带插件前缀，比如 `/ship-it:plan-to-issues`。平时不用手动调用。

### 手动

把 `plugins/ship-it/skills/` 下的技能目录复制到你的 agent 读技能的地方，比如 `~/.claude/skills/` 或项目里的 `.agents/skills/`。技能之间按同级目录互相引用，要放在同一个父目录下。

## 适用范围

- **以 GitHub 为主**：issue、PR、Actions。别的平台思路相同，具体命令要自己换。
- **管"从想法到合并进 main"**：部署上线、发版打 tag、发布到 npm 不在范围内。
- **分支模型是"main + 短分支"**：仓库如果用 develop / release 那种长期分支，技能会按仓库现有的约定来，不会硬改成 main。
- **技能正文是中文**：agent 读起来没有问题，回复会跟着你用的语言走。

## 参与

这个仓库自己也按这套流程走：开 issue → 分支 → PR → CI（`scripts/validate.py`）→ 合并。欢迎提 issue 和 PR。

```
plugins/ship-it/skills/<技能名>/SKILL.md   # 技能本体（npx skills 和 Claude 插件都从这里读）
plugins/ship-it/skills/new-repo/assets/    # CI、PR 模板、issue 模板
plugins/ship-it/.claude-plugin/plugin.json # Claude Code 插件清单
.claude-plugin/marketplace.json            # Claude Code 插件市场入口
evals/ship-it/                             # 测试用例，不随技能安装
scripts/validate.py                        # 结构检查，CI 也跑它
```

改了技能，提交前先跑 `python scripts/validate.py`。想看技能对 agent 行为的实际影响，可以跑测试用例（需要 Claude Code）：

```bash
cp -r evals/ship-it plugins/ship-it/skills/ship-it/evals
cd plugins/ship-it/skills/ship-it && claude plugin eval . --allow-tools Write,Edit,Bash
rm -rf evals   # 跑完删掉，别提交
```

## 许可

[MIT](LICENSE)
