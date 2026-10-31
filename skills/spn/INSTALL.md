# 安装 SPN 技能包

本目录是一个**自包含、可直接被 AI Agent 加载**的技能包。核心规则完整内联在 `SKILL.md`，深度参考按版本号锁定到 GitHub，离线时不影响核心规则。

## 包里有什么

| 文件 | 作用 | 谁读它 |
|---|---|---|
| `SKILL.md` | 技能本体：元数据 + 完整规则（约 200 行） | Agent（识别到 `spn` 技能时加载） |
| `AGENTS.md` | 精简版规则，可直接拷进项目根目录 | Agent（开工前自动加载） |
| `INSTALL.md` | 本文件，给人看 | 你 |

`SKILL.md` 已通过 Agent Skills 官方校验器（`agentskills validate`）。

> **需要英文版？** 见 [`skills/spn-en/`](../spn-en/INSTALL.md)。技能规范要求 `name` 与父目录同名，所以英文包目录名只能是 `spn-en`，不能两个都叫 `spn`。

## 先选一种方式

| 你的情况 | 用哪种 | 用时 |
|---|---|---|
| 用 Claude Code / CodeBuddy 等支持 skills 目录的工具 | **方式一** | 1 分钟 |
| 用支持 `AGENTS.md` 的工具（Cursor、Codex、Aider、Windsurf 等） | **方式二** | 30 秒 |
| 用 Gemini CLI 或 GitHub Copilot | **方式三** | 1 分钟 |
| 不确定自己的工具支持什么 | **方式二**（最通用） | 30 秒 |

---

## 方式一：作为 Agent Skills 安装

把整个 `spn/` 目录放进工具的技能目录。**目录名必须保持 `spn`**（技能规范要求 `name` 与父目录同名，否则校验不通过）。

**Claude Code**

```bash
# 用户级：所有项目生效
cp -r skills/spn ~/.claude/skills/spn

# 项目级：随项目走，团队共享
mkdir -p .claude/skills
cp -r skills/spn .claude/skills/spn
```

Windows PowerShell：

```powershell
Copy-Item -Recurse skills\spn "$env:USERPROFILE\.claude\skills\spn"
```

**CodeBuddy**

```bash
cp -r skills/spn ~/.codebuddy/skills/spn
```

**其它工具**：路径通常是 `~/.<工具名>/skills/` 或项目内 `.<工具名>/skills/`，以该工具文档为准。

## 方式二：作为 AGENTS.md 规则基线（最通用）

`AGENTS.md` 是 Agent 实际加载执行的精简规则。拷进**任意项目的根目录**即可：

```bash
cp skills/spn/AGENTS.md 你的项目/AGENTS.md
```

支持 AGENTS.md 的工具（Cursor、Codex、Copilot、Gemini CLI、Aider、Windsurf 等）会在开工前自动加载。

> **Claude Code 特别说明**：存在 `CLAUDE.md` 时，Claude Code 默认不读 `AGENTS.md`。稳妥做法是以 `AGENTS.md` 作为共享基线，再写一层薄的专属文件：
>
> ```bash
> echo "@AGENTS.md" > CLAUDE.md
> ```

## 方式三：Gemini CLI / GitHub Copilot 的专属文件

这两个工具认自己的文件名。**建薄文件指向规则本体**，不要让规则出现第二份：

```bash
# Gemini CLI
cp skills/spn/AGENTS.md GEMINI.md

# GitHub Copilot
mkdir -p .github
cp skills/spn/AGENTS.md .github/copilot-instructions.md
```

---

## 验证是否生效

新开一个会话，说这句：

> 我不懂代码，但想用 AI 做个网页应用。先别写代码，按 SPN 的规则来。

**三条可观察的行为**，出现两条以上说明已生效：

1. 它先问清目标与"做完的标志"，而不是直接开写
2. 你问到不懂的词时，它主动翻译成大白话
3. 提到删除、上线、付费时，它停下来等你确认

如果它直接开始写代码，说明规则没被加载——检查文件是否放对了位置。

## 升级

技能包版本与仓库 tag 一一对应（见 `SKILL.md` 的 `metadata.version`）。升级时重新拷一次覆盖：

```bash
cp -r skills/spn ~/.claude/skills/spn   # 覆盖旧版本
```

想固定在某一个版本，从 Release 页下载对应 tag 的仓库快照，别用 `main`。

## 卸载

删掉目录即可，本技能包不写入任何全局配置、不联网、不留残留：

```bash
rm -rf ~/.claude/skills/spn
```

## 常见问题

**Q：`references/` 点不开？**
链接锁定到发布 tag 且需要联网。核心规则已内联在 `SKILL.md`，离线只影响"点开看细节"。

**Q：能不能改规则？**
可以。改**仓库根目录**的 `AGENTS.md` / `references/`，再同步到技能包——两份副本的一致性由 CI 强制检查（`doc-lint`）。直接改包内副本会导致 CI 失败。

**Q：为什么技能包里的 `AGENTS.md` 顶部多一行注释？**
那是"发布快照"标记，提醒改规则请回根目录。CI 比对时会自动忽略这一行。

## 许可证

技能包内全部内容随仓库以 **CC BY 4.0**（知识共享署名 4.0 国际许可协议）提供，可自由使用、再分发、修改，需署名。详见仓库 `LICENSE-DOCS.md`。
