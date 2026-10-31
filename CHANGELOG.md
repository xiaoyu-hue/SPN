# 更新日志

本文件采用 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

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
