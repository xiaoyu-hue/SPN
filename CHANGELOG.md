# 更新日志

本文件采用 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

尚未发布的改动记在 `[Unreleased]` 下；发版时执行 `python3 scripts/release.py <版本号> --yes`，脚本会自动把它提升为版本小节。

## [Unreleased]

### 新增

- `scripts/release.py` —— 一键发版：把 `[Unreleased]` 提升为版本小节、同步中英 README 徽章与链接、同步三个 `SKILL.md` 的版本号、把技能包链接锁定到新 tag、刷新技能包快照，跑完校验再提交、打 tag、建 Release。默认 dry-run，加 `--yes` 才写盘推送
- `scripts/check_links.py` —— 全仓库 Markdown 相对链接与锚点自检（纯本地、不联网），可单独运行

### 变更

- 技能包 `skills/spn/` 专业化：通过 Agent Skills 官方校验器；深度参考链接由 `blob/main` 锁定到当前 tag（保证装到的内容可复现）；补齐 05、06 两篇索引并统一"含英文版"标注；移除对外部使用者无意义的内部历史措辞与 `personal/` 提示
- `skills/spn/INSTALL.md` 重写：包内容说明、按工具选方式的决策表、Claude Code / CodeBuddy 已验证路径、生效验证三信号、升级与卸载、常见问题
- `skills/spn/SKILL.md` 顶部新增"30 秒版本"，便于快速判断规则是否被加载

### 工程化

- `doc-lint` 新增「技能包快照与根目录一致」检查：`skills/spn/AGENTS.md` 偏离根目录 `AGENTS.md` 时 CI 失败，防止两份副本漂移
- `doc-lint` 排除规则由硬编码 `v1.0.0` 改为排除含 `http(s)://` 的行：发版后 Release 链接中的版本号不再误报（原先升到 1.0.1 就会让 CI 变红）
- `doc-quality` 的 `actions/checkout` 由 v4 升到 v7，与 `doc-lint` 对齐

## [1.0.0] - 2026-10-31

面向开源社区的首个正式版本。项目统一命名为 **SPN**（Self-precipitation，自我析出）：在 AI 给出的众多选项里，让属于你自己的判断沉淀、成形。

### 规则内容

- **三层结构**：`AGENTS.md`（AI 实际加载执行的规则）、`SKILL.md`（技能入口与完整说明）、`references/01`–`08`（分主题详解）
- `references/07` 决策审查清单、`references/08` 文档同步规范 —— 决定前先反问、发布前先同步，可直接套用到任意项目
- `references/06` 生态与整合 —— 策展式索引同类项目、技能、工具与 MCP；只引用不复制，保留各自许可证

### 双语与可安装

- `docs/` 英文完整镜像，与中文版一一对应；中文源保持中文命名，英文版使用英文文件名
- `skills/spn/` 可直接安装的 Agent Skill 包（Anthropic Agent Skills 格式），含 Cursor / Codex / Copilot / Gemini CLI 等平台的安装说明

### 许可证

- 分层许可：文档 **CC BY 4.0**（知识共享署名 4.0 国际许可协议），代码 **MIT**

### 工程化与质量保障

- CI 三道：`doc-lint`（禁止写死会随迭代变化的数字）、`secret-scan`（gitleaks 密钥扫描）、`doc-quality`（lychee 死链 + vale 术语）
- Dependabot 维护 GitHub Actions 版本；配套 `CONTRIBUTING.md`、`SECURITY.md`、issue 与 PR 模板

### 已知局限

- 面向不懂代码的使用者优化，专业开发者可能觉得冗余，请遵循所在团队规范
- 不能替代专业安全审计；安全自查示例以 Supabase / Postgres 为主，其他后端需自行调整
