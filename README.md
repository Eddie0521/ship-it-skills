# ship-it-skills

一套 Claude 技能，教 Claude 用 GitHub 的方式推进软件工作：

```
搭骨架 → 讨论方案 → issue（待办）→ 分支 → PR（交付）→ CI（把关）→ 评审 → 合并，自动关 issue
```

核心只有一句话：**main 只放能用的版本；每件事都有一个 issue 说清楚要什么，在分支上做，用 PR 交付，CI 把关，合并时顺手关掉 issue。**

## 技能

一个入口，加上按项目生命周期排的五个子技能。入口判断你在哪一步，再转给对应的子技能；子技能也能被直接触发。

```
new-repo          搭骨架
    ↓
plan-to-issues    讨论方案 → 定稿 → 拆 issue（别人给来的方案也从这里进）
    ↓
issue-to-pr       一个 issue → 一个 PR
    ↓
pr-to-merge       持续跟进 PR 到能合并

handoff           旁支：方案定稿后交给别人做，再验收回来
```

| 技能 | 负责 |
| --- | --- |
| `ship-it` | 入口：判断在哪一步、转到子技能；定下所有子技能共用的规矩 |
| `new-repo` | 新项目搭骨架：README、测试命令、CI、PR 模板、issue 模板、.gitignore、分支保护 |
| `plan-to-issues` | 和你讨论方案，或者消化别人给来的方案；大事先写设计文档，再拆成可独立交付的 issue |
| `issue-to-pr` | 一个 issue 做成一个 PR：开分支、小步提交、草稿 PR、`Closes #N`、推送前自证 |
| `pr-to-merge` | 把 PR 推到能合并：冲突 → CI → 评审意见，找根因，不跳过测试 |
| `handoff` | 我们的方案交给别人：选交付形式、写开工消息、按测试 / 不变量 / 方案偏差验收 |

所有子技能共用的规矩：

- **对外操作先给方案，确认再做**：建 issue、推送、开 PR、合并、改仓库设置之前，先把草稿和 diff 给你看。
- **仓库自己的规矩优先**：CONTRIBUTING、PR 模板、CLAUDE.md 等。
- **绝不**：跳过测试来让 CI 变绿，推空提交触发 CI，在别人的分支上 force-push，提交密钥，未经确认就合并。

## 安装

### 任何 agent：`npx skills add`（推荐）

用 [skills](https://github.com/vercel-labs/skills) 命令行装，支持 Claude Code、Codex、Cursor 等多种 agent：

```bash
npx skills add Eddie0521/ship-it-skills
```

它会列出 6 个技能、检测你装了哪些 agent，让你勾选。常用参数：

```bash
npx skills add Eddie0521/ship-it-skills --list                  # 只看有哪些技能，不安装
npx skills add Eddie0521/ship-it-skills -s '*' -a codex -y      # 全部技能装给 Codex，不提问
npx skills add Eddie0521/ship-it-skills -s ship-it -s issue-to-pr -g   # 只装两个，装到用户级（所有项目可用）
```

只装部分技能时，建议带上入口 `ship-it`：它负责判断你在哪一步，再转给对应的子技能。

### Claude Code 插件

```bash
claude plugin marketplace add Eddie0521/ship-it-skills
claude plugin install ship-it@ship-it-skills
```

装好后技能名带插件前缀，比如 `/ship-it:plan-to-issues`。一般不用手动调用，说出你的场景就会触发。

### 手动

把 `plugins/ship-it/skills/` 下的技能目录复制到你的 agent 读技能的地方，比如 Claude Code 的 `~/.claude/skills/`，或者项目里的 `.agents/skills/`。技能之间按同级目录互相引用，所以要放在同一个父目录下。

## 目录

```
plugins/ship-it/skills/<技能名>/SKILL.md   # 每个技能一个目录（npx skills 和 Claude 插件都从这里读）
plugins/ship-it/skills/new-repo/assets/    # CI、PR 模板、issue 模板
plugins/ship-it/.claude-plugin/plugin.json # Claude Code 插件清单
.claude-plugin/marketplace.json            # 让这个仓库能被当作 Claude Code 插件市场添加
evals/ship-it/                             # 测试用例（claude plugin eval 的格式），不随技能安装
scripts/validate.py                        # 结构检查，CI 也跑它
```

## 参与

这个仓库自己也按这套流程走：开 issue → 分支 → PR → CI（`scripts/validate.py`）→ 合并。

技能正文要和具体 agent 无关：不假设一定有某个工具，用"有就用，没有就退一步"的写法。

改了技能，最好跑一下测试用例。用例放在 `evals/`，不随技能安装；要用 `claude plugin eval` 跑的话，先复制到技能目录下：

```bash
cp -r evals/ship-it plugins/ship-it/skills/ship-it/evals
cd plugins/ship-it/skills/ship-it && claude plugin eval . --allow-tools Write,Edit,Bash
rm -rf evals   # 跑完删掉，别提交
```

## 许可

MIT
