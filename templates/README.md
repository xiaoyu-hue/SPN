# SPN 技能模板集

把 SPN 的通用规则**按场景切成可独立安装的小包**。

和直接用整份 `AGENTS.md` 的区别：那份是常驻基线（每次开工都加载），
这些是**按需触发**——遇到具体场景时，Agent 才把对应的正文读进来。
好处是不用把 8 篇 references 常驻在上下文里，也更容易分享给只需要某一块的人。

## 目录

| 技能 | 解决什么 | 从 SPN 哪里来 |
|---|---|---|
| [`spn-security-check`](./skills/spn-security-check/SKILL.md) | 上线前扮演攻击者自查；重点是那些"看不出问题但正在泄露"的权限错误 | `references/02` |
| [`spn-decision-review`](./skills/spn-decision-review/SKILL.md) | 不可逆 / 花钱 / 发布前的决策三问 + 替代方案 + 拍板记录 | `references/07` |
| [`spn-handoff`](./skills/spn-handoff/SKILL.md) | 跨会话记忆；一个 md 文件解决"I 会话失忆" | `references/04` G 段 |
| [`spn-term-translator`](./skills/spn-term-translator/SKILL.md) | 术语翻译成人话；保护"人无法为听不懂的东西负责" | `references/04` F1 |
| [`spn-docs-sync`](./skills/spn-docs-sync/SKILL.md) | 发版前的最后一轮文档校对；唯一真源原则 | `references/08` |
| [`_skeleton`](./skills/_skeleton/SKILL.md) | 空白骨架，从零写新技能时复制它 | — |

---

## 一、`SKILL.md` 的硬性约束

规范来源：[Anthropic Agent Skills](https://github.com/anthropics/skills)（官方文档在 `agentskills.io`）。
下面几条是**写错就装不上 / 触发不了**的，其余都可以自由发挥。

| 约束 | 具体要求 | 为什么 |
|---|---|---|
| **frontmatter 必需字段** | 只有两个：`name` 和 `description` | 规范的最小要求；`license` / `metadata` 是可选的补充信息 |
| **`name` 格式** | 小写，空格用连字符替代 | 不符合会被拒绝解析 |
| **`name` 不能含保留词** | 不得包含 `claude` 或 `anthropic` | 官方最佳实践明确禁止；一旦用了，作为自定义技能上传会失败 |
| **`name` 与目录同名** | 规范要求 | 所以中英两个包不能都叫 `spn`，英文包只能叫 `spn-en` |
| **`description` 长度** | ≤ 1024 字符 | 这是上传校验施加的限制，超了直接失败 |
| **单文件自包含** | 目录下的 `SKILL.md` 里要有完整正文 | 深层内容可以通过相对链接外挂，但核心规则必须内联，否则离线就失效 |

用本仓库的脚本自检：

```bash
python3 scripts/validate_skills.py            # 检查 templates/ 与 skills/ 下所有技能包
python3 scripts/validate_skills.py --verbose  # 顺带看看每个包的基本信息
```

---

## 二、`description` 怎么写才触发得了

**这是整个 SKILL.md 里最值钱的一行。** Agent 决定要不要加载这个技能，靠的就是它。

### 句式（照这个填）

```
当用户【场景 / 触发信号】，需要【他想达成什么】时使用：【你会具体做什么】。覆盖【关键词】。
```

对比一下就知道差别：

| 写法 | 效果 |
|---|---|
| ❌ `一个关于安全审查的技能` | 只描述了"它是什么"，Agent 不知道何时该用 |
| ✅ `当用户准备上线、部署到公网...时使用：扮演攻击者自查未授权读取、越权访问、密钥泄漏...` | 有触发场景 + 有具体动作 + 有可检索关键词 |

### 三条经验

1. **写触发条件，不写功能介绍。** Agent 是在用户的**原话**里找信号，不是在查说明书。
2. **把用户的抱怨原话放进去。** 比如 `spn-security-check` 里写了"泄漏数据"、
   `spn-handoff` 里写了"下次怎么接着做"——用户真的会这么说。
3. **结尾补关键词。** "覆盖 XXX、YYY、ZZZ" 这一句能显著提高语义召回率。

---

## 三、怎么用

放进你的 Agent 能识别的 skills 目录即可（各工具位置不同）：

```bash
# 示例：Claude Code 的项目级技能
mkdir -p .claude/skills
cp -r templates/skills/spn-security-check .claude/skills/

# 只想把规则塞进对话、不装成技能也行：
# 直接把 SKILL.md 的正文（去掉 frontmatter）复制给 Agent
```

**最小用法**：不装任何东西，把某个 `SKILL.md` 的正文整段贴给 AI，效果一样。

---

## 四、这些模板遵守的规则

它们自己也按 SPN 的原则写的：

- **不吹能力** — 每个都有「边界」一节，写清它覆盖不了什么
- **不替人做决定** — `spn-decision-review` 明确要求"把代价说完再问要不要继续"
- **说实话优先** — `spn-security-check` 要求"没找到问题"和"没有问题"必须区分开
- **保护边界声明** — 涉及安全的声明由人自己写，AI 不代笔
