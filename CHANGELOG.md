# 更新日志

本文件采用 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式。
版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增
- `docs/` — 英文完整镜像：README、AGENTS、SKILL、SECURITY、CONTRIBUTING 及全部 4 篇 references 的英文版，与中文版结构一一对应
- `skills/spn/` — 自包含、可安装的技能包（Anthropic Agent Skills 格式）：带 frontmatter 的 `SKILL.md`、可直接加载的 `AGENTS.md` 副本、各平台安装说明 `INSTALL.md`；深度参考走 GitHub 链接避免重复

### 修复
- `LICENSE-DOCS.md` 覆盖范围与仓库实际结构对齐：删除不存在的文件引用（`SECURITY.en` / `CODE_OF_CONDUCT` / `GLOBAL.md`），修正"纯文档仓库却列出 js/css/tests 等代码"的 MIT 范围误述，新增 `docs/` 与 `skills/` 的 CC BY 4.0 覆盖
- 根 README / CONTRIBUTING 的仓库结构与翻译说明同步到新增的 `docs/`、`skills/`

### 工程化
- `.github/dependabot.yml` — 针对仓库唯一的"依赖"（GitHub Actions）开启版本更新
- `doc-lint.yml` 扫描范围由 `README.md` / `AGENTS.md` 扩展至 `SKILL.md`、`references/` 与英文镜像 `docs/`（教学文档 `03` 与"写死值 → 相对描述"反例句式按约定排除）

### 安全与文档质量 CI（P0）
- `.github/workflows/secret-scan.yml` + `.gitleaks.toml` — gitleaks 密钥扫描（非阻塞，确认无误报后改为阻断）；文档中作为反例出现的密钥名（`sk_live` / `service_role` / `YOUR_ANON_KEY` / `anon key`）已加入 allowlist
- `.github/workflows/doc-quality.yml` + `lychee.toml` / `.vale.ini` / `styles/SPN/` — 英文镜像死链检查（lychee）与术语一致（vale，仅 `docs/`，建议级），均非阻塞，避免误杀文档

---

## [1.0.0] - 2026-10-31

面向开源社区的首个正式版本（原以 `ai-collab-rules` 名义发布，本仓库统一命名为 **SPN**）。

### 新增

**核心文件**
- `SKILL.md` — 技能入口：角色分工、三档授权、五次握手、零基础三个关键动作、糊弄识别表、完成前自收
- `AGENTS.md` — 可直接放进任何项目根目录、由 AI 实际加载执行的精简版规则
- `README.md` / `README.en.md` — 中英文说明、快速上手、与常见模板的差异对比
- `LICENSE`（MIT，代码）/ `LICENSE-DOCS.md`（CC BY 4.0，文档）— **分层开源许可证**

**参考资料**
- `references/01-协作哲学与判断归属.md`（**含英文版 `.en.md`**）
  - 判断归属表；三个真实判断案例（首次上线 / 风格融合 / 安全边界声明）
  - "先试再问 vs 先问再试"的撤销成本判据
  - 术语翻译机制；六条"AI 在糊弄你"的信号（含编造库名的识别）
  - 从纯前端到全栈的身份变化：工具作者 → 数据保管人
- `references/02-上线前安全自查.md`（**含英文版 `.en.md`**）
  - 数据库权限三步检查（含可执行 SQL 与 curl 复现命令）
  - 密钥检查（含 grep 命令、git 历史泄漏处理）
  - 越权测试：注册两个账号互相读数据
  - 免费安全扫描工具对比表 + 静态检查的能力边界说明
  - **新增「零基础友好：让 AI 替你跑检查」**——免终端/SQL 的提示词路径（解决受众能力与要求错位的硬伤）
  - 新增「其他后端适配思路」附录（Supabase / Neon / Cloudflare D1 对比）
- `references/03-文档、局限披露与事实维护.md`
  - README 骨架；"做不到什么"三种句式（含"主动防止被误读"句式）
  - 四类项目的局限写法范例；维护状态写法；许可证选择对照表
- `references/04-提示词库.md`
  - 按使用场景分 A–H 八类，**共 23 条**可直接复制的提示词
  - 含通用角色设定、"我不懂技术"约束、PRD 公式、先调研后编码
  - 含 HANDOFF.md 跨会话交接方案与模板、QBS 法、寓言讲概念
  - 附五条使用心法

**工程化与治理（本次补齐的专业化缺口）**
- `CONTRIBUTING.md` — 贡献指南：两层结构、通用/个人升级防线、如何新增一条规则、许可证分层
- `SECURITY.md` — 安全问题的负责任披露渠道
- `.gitignore` — 标准忽略文件（密钥、构建产物、编辑器文件等）
- `.github/ISSUE_TEMPLATE/`（Bug / 提案）+ `PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/doc-lint.yml` — **文档狗粮 CI**：自动扫描 `README.md` / `AGENTS.md` 里的硬编码数字，落实本项目"数字不写死"原则
- `AGENTS.md` 补入 **三视角分析** 与 **调试三步法**（原 v1.0.0 缺失、但作者已在用的实践）

### 设计取舍

- **不写技术栈推荐**。原作者的个人版含一套 React 生态技术栈清单，但那只适用于特定生态，
  放进通用版会误导使用其他技术栈的人 → 已移入个人版
- **保留真实判断案例**。三个案例来自作者实际项目，比抽象原则更有说服力，且具备普适性
- **安全事件数据标注核实时间**。文中引用的 CVE、调查报告均标注"核实于 2026-10"，
  提醒使用者复核，避免把时点数据当永久事实
- **分层许可证**：代码 MIT（最大自由度）、文档 CC BY 4.0（只需署名），比原 CC BY-NC 更利于大众传播
- **内容去重**：三个案例的完整叙事只保留在 `references/01`，README / SKILL 改为指向，避免同一段讲 5 遍

### 已知局限

- 针对**不懂代码的使用者**优化，专业开发者用会嫌冗余
- 安全自查的 SQL 与命令以 Supabase / Postgres 为例，其他后端需按对应机制调整
- 不能替代专业安全审计
- `03`、`04` 及 `personal/` 目前仅中文
