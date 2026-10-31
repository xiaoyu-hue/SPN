# 安装 SPN 技能包（skills/spn/）

本目录是一个**自包含、可被 AI Agent 直接加载**的技能包。核心规则已内联在 `SKILL.md` 中，深度参考文档通过 GitHub 链接引用（离线不影响核心规则使用）。

## 方式一：作为 Agent Skills 安装（推荐，Claude Code / Cursor / Codex / Windsurf 等）

把整个 `spn/` 目录放到 Agent 的 skills 目录下即可，不同工具路径略有差异：

```bash
# Claude Code（项目级，放在仓库里随项目走）
mkdir -p .claude/skills
cp -r skills/spn .claude/skills/spn

# Claude Code（用户级，对所有项目生效）
# macOS / Linux:
cp -r skills/spn ~/.claude/skills/spn
# Windows (PowerShell):
# Copy-Item -Recurse skills/spn $env:USERPROFILE\.claude\skills\spn

# Cursor（项目级）
mkdir -p .cursor/skills
cp -r skills/spn .cursor/skills/spn
```

放入后，Agent 在对话中识别到 `spn` 技能即可自动遵循其中的协作规则。

## 方式二：作为 AGENTS.md 规则基线（最通用）

`AGENTS.md` 是 Agent 实际加载执行的精简规则。把它拷进**任意项目根目录**，支持 AGENTS.md 的工具（Cursor、Codex、Copilot、Gemini CLI、Aider、Windsurf 等）会在开工前自动加载：

```bash
cp skills/spn/AGENTS.md 你的项目/AGENTS.md
```

> 提示：Claude Code 在自身配置文件存在时默认不读 AGENTS.md，需要手动导入。稳妥做法是用 AGENTS.md 作共享基线，再写一层薄的工具专属文件（例如在 `CLAUDE.md` 里写 `@AGENTS.md`）。

## 方式三：CodeBuddy / WorkBuddy

将 `skills/spn/` 整体放入本工具的技能目录（如 `~/.codebuddy/skills/spn/`），工具即可识别并调用该技能。

## 方式四：Gemini CLI / GitHub Copilot 的薄适配文件

部分工具不读取 `AGENTS.md` 或 skills 目录，而是认自己的专属文件。做法是**建一个薄文件，把 SPN 规则嵌进去**（规则本体仍以仓库根目录为唯一真相，避免多份漂移）：

### Gemini CLI
项目根建 `GEMINI.md`，内容即为 `skills/spn/AGENTS.md`：

```bash
cp skills/spn/AGENTS.md GEMINI.md
```

### GitHub Copilot
仓库建 `.github/copilot-instructions.md`，内容同上：

```bash
mkdir -p .github
cp skills/spn/AGENTS.md .github/copilot-instructions.md
```

> 这类「薄适配文件」只负责把规则喂给对应工具。要改规则，改根目录源，再重新 `cp` 覆盖即可。

---

## 验证是否生效

在加载了该技能的会话里说一句：「我不懂代码，但想用 AI 做个网页应用，先别写代码，按 SPN 的规则来。」

若它先让你确认目标与验收标准、遇到不懂的词主动翻译、对删库/上线/付费等要求先问你——说明规则已生效。

## 更新

本技能包的规范源在仓库根目录（`https://github.com/xiaoyu-hue/SPN`）。升级时重新执行上面的 `cp` 命令覆盖即可。

## 许可证

技能包内全部内容随仓库以 **CC BY 4.0** 提供（见仓库 `LICENSE-DOCS.md`）。可自由使用、再分发、修改，需署名。
