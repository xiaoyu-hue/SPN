# 贡献指南（CONTRIBUTING）

谢谢你想让 SPN 更好。这份指南说明本仓库的结构与边界，避免改着改着变成两份互相矛盾的规则。

---

## 一、仓库的两层结构（先读这个）

```
SPN/
├── AGENTS.md        ← 通用规则，所有人用（AI 实际加载执行）
├── SKILL.md         ← 技能入口 / 完整版说明
├── references/      ← 通用规则（共 8 篇）
├── docs/            ← 英文完整镜像
├── skills/
│   ├── spn/         ← 可安装技能包（中文，含 INSTALL.md）
│   └── spn-en/      ← 可安装技能包（英文）
├── scripts/         ← 发布与校验脚本（见下方「第五节」）
├── FACTS.md         ← 带时效的事实登记表（给 CI 读）
└── personal/        ← 作者自用的一层，⚠️ 不是通用规则的一部分
```

- **通用层**（`AGENTS.md` / `SKILL.md` / `references/`）：给所有人用，应保持与技术栈无关、与"个人情况"无关。
- **个人层**（`personal/`）：只放"只对该作者成立"的上下文（他的项目、他的技术栈、他的待办）。处理一般任务时跳过。

---

## 二、唯一的防线：升级规则

> **换个人也成立的规则，一律写到根目录的通用层，不要写进 `personal/`。**

这条不执行，两层就会功能重叠，最后变成两份互相矛盾的规则。
如果你贡献一条新规则，先判断它是否普适：

- 普适 → 加进 `AGENTS.md`（或对应 `references/` 篇章）
- 只对个人成立 → 放进 `personal/`，不要污染通用层

---

## 三、如何新增一条规则

本仓库自己的原则也适用在这里：

1. **踩一次坑加一条，不预先堆砌。** 每条规则最好对应一类真实发生的问题，而不是"听起来有道理"。
2. **新增前先问能不能和现有条目合并。** 避免碎片化。
3. **写进 `AGENTS.md` 的用 AI 能加载执行的语气**（对 AI 下指令）；写进 `references/` 的可以用给人看的讲解语气。
4. **涉及安全、授权、红线的改动，请先开 issue 对齐方向**，再提 PR。
5. **数字不要写死**：会随代码变化的数字（测试数、版本号、条目数）用相对描述，并同步更新。

---

## 四、内容去重约定

同一段内容（如三个真实案例、完成前自收五条）只保留**一份权威叙述**：

- 三个案例的完整叙事 → 仅在 `references/01-协作哲学与判断归属.md`
- 完成前自收 / 诚实汇报 → 权威在 `AGENTS.md`，`SKILL.md` 与 `references/04` 引用或指向
- 其它文件提到时，**链接过去**，不要整段重抄

---

## 五、改了这里，就必须同步那里（否则 CI 会红）

**根目录是唯一规范源。** `docs/`（英文镜像）与 `skills/`（可安装技能包）都是**发布副本**——
不要直接编辑它们，改了也会被覆盖，而且会让"用户装到的规则"和"仓库显示的规则"分叉。

| 你改了规范源 | 必须同步到 | 谁来同步 |
|---|---|---|
| `AGENTS.md` | `skills/spn/AGENTS.md` | **自动**（`sync_snapshots.py`） |
| `docs/AGENTS.md` | `skills/spn-en/AGENTS.md` | **自动** |
| `SKILL.md` | `skills/spn/SKILL.md` | **自动** |
| `docs/SKILL.md` | `skills/spn-en/SKILL.md` | **自动** |
| `references/01`–`08`（中） | `docs/references/*`（英） | **手工**（翻译）

一行命令搞定自动部分：

```bash
python3 scripts/sync_snapshots.py --apply   # 写入
python3 scripts/sync_snapshots.py --check   # 只校验，CI 每次都跑这一步
```

> 包专属措辞（版本头、"30 秒版本"、引用段的提示语）写死在 `scripts/sync_snapshots.py` 的
> `HEADER_*` / `SECTION_*` 常量里。**如果你改了源里被它引用的那几句话，脚本会报错而不是静默漏替换**——
> 按报错提示同步更新常量即可。

### scripts/ 里都有什么

| 脚本 | 干什么 | 什么时候跑 |
|---|---|---|
| `release.py` | 一键发版（默认 dry-run，`--yes` 才写盘推送） | 发版时，手工执行 |
| `sync_snapshots.py` | 规范源 → 发布副本，含一致性校验 | 每次提交（CI）+ 发版时 |
| `doc_lint.py` | 抓入口文件里写死、会失真的数字 | 每次提交（CI） |
| `check_facts.py` | 提醒 `FACTS.md` 里已登记的事实过期了 | 每次提交（CI，非阻塞） |
| `check_links.py` | 全仓库相对链接与锚点自检 | 每次提交 + 发版时 |
| `run_tests.py` | scripts/ 的单元测试 | 每次提交（CI，三系统） |
| `validate_skills.py` | 校验技能包是否符合 Agent Skills 规范 | 每次提交（CI） |

**如果你给 scripts/ 加了功能，必须同步加测试**（`AGENTS.md` 第 92 行对本仓库同样生效）。
新增的时效性数据（调研数字、平台额度、价格）登记进 `FACTS.md`，不要散落在文档里。

---

## 六、许可证分层

- 代码（脚本、CI 配置）→ **MIT**（`LICENSE`）
- 文档（规则、提示词、参考资料）→ **CC BY 4.0**（`LICENSE-DOCS.md`）

贡献即表示你同意你的贡献在相同分层许可证下发布，并适当署名原作者。

---

## 七、翻译

参考资料 `01`–`08` 及 `AGENTS.md` / `SKILL.md` / `SECURITY.md` / `CONTRIBUTING.md` 的英文完整版已统一放在 `docs/`；`personal/` 仍仅中文。
翻译请保持"大白话优先、术语括号解释、如实披露"的原文风格。

---

## 八、提交前的自检

提交前请过一遍下面几项，本地能跑的全跑一遍再推送，会比等 CI 红更快：

```bash
python3 scripts/run_tests.py           # scripts/ 的单元测试
python3 scripts/sync_snapshots.py --check   # 发布副本是否与源一致
python3 scripts/doc_lint.py            # 有没有写死的失真数字
python3 scripts/check_links.py         # 链接与锚点
python3 scripts/check_facts.py         # 有没有该复核的事实
```

检查清单：

- [ ] 改动落在正确的层（通用 / 个人）
- [ ] 没有把同一段内容重复写多遍
- [ ] **只改了规范源，没有直接编辑 `docs/` 或 `skills/` 的发布副本**
- [ ] 已执行 `sync_snapshots.py --apply`（如改了 `AGENTS.md` / `SKILL.md`）
- [ ] 文档里的数字没有写死（时效性数据已登记进 `FACTS.md`）
- [ ] 改动了 `scripts/` 就补了对应的测试
- [ ] 如改动涉及安全红线，已先开 issue 对齐
- [ ] PR 说明写清：你做了什么、为什么、期望效果
