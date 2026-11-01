// 所有展示文案集中于此（单一来源，跟随仓库；不写会随迭代变化的数量）
// 内容摘抄自 SPN 仓库根目录 AGENTS.md / README.md / references/05，保持与仓库一致。

export const SITE = {
  name: "SPN",
  tagline: "零基础 × AI 协作规则",
  coreClaim: "代码是 AI 写的，判断是你做的。",
  intro:
    "SPN（Self-precipitation，自我析出）是一套写给不懂代码的人的 AI 协作规则：在 AI 给出的众多选项里，让你的判断沉淀、成形。AI 提供能力与方案，你负责拍板与划边界。",
  github: "https://github.com/xiaoyu-hue/SPN",
  version: "v1.1.0",
};

export type Tier = "allow" | "ask" | "forbid";

export const AUTHORIZATION: {
  tier: Tier;
  title: string;
  emoji: string;
  items: string[];
}[] = [
  {
    tier: "allow",
    title: "照做就行",
    emoji: "🟢",
    items: [
      "读文件、看日志、查资料、诊断、review",
      "改工作目录内文件、跑测试、本地验证",
      "本地 git commit（可逆、有 reflog）",
      "改完代码就跑相关测试、lint、类型检查",
    ],
  },
  {
    tier: "ask",
    title: "先问再做",
    emoji: "🟡",
    items: [
      "删除或覆盖不是你创建的文件",
      "修改数据库 schema、执行数据迁移",
      "新增生产依赖、生产部署、公开发布",
      "对外动作（发邮件、提 PR、公开回复）",
      "影响超过 5 个文件/记录的批量操作",
      "改变 Git 历史且影响他人（push、强推等）",
    ],
  },
  {
    tier: "forbid",
    title: "永远不做",
    emoji: "🔴",
    items: [
      "提交 .env、密钥、证书、令牌到仓库",
      "把 service_role / sk_live / 私钥放进前端代码",
      "权限判断只做在前端——藏按钮不算权限",
      "拼接 SQL、把用户输入直接拼进命令",
      "静默跳过错误、隐式兜底、制造假数据",
      "编造代码 / 测试结果，或声称已验证实际没执行",
    ],
  },
];

export const KEY_ACTIONS = [
  {
    n: "01",
    title: "术语必须先翻译，才能判断",
    desc: "不要用听不懂的词拍板。听不懂不是你的问题，是对方没讲清楚。",
  },
  {
    n: "02",
    title: "先试再问",
    desc: "判据只有一条：能不能一键还原？能就试，不能就问。这一条能解决大多数犹豫。",
  },
  {
    n: "03",
    title: "能力不等于担保",
    desc: "AI 能写出加密代码，但“未经审计”这句声明得由你来写。",
  },
];

export const THINKING = [
  {
    title: "全力反驳",
    desc: "假设方案是错的，列出它会在哪些地方翻车。",
  },
  {
    title: "切换支持",
    desc: "反过来，它成立的条件是什么、好处是什么。",
  },
  {
    title: "中立对比",
    desc: "把备选方案并排，按代价 / 风险 / 扩展性客观对比。",
  },
];

export const DEBUG_STEPS = [
  { n: "1", title: "描述报错", desc: "把错误原文贴出来，说清发生在哪一步。" },
  { n: "2", title: "大白话解释原因", desc: "用生活比喻讲清为什么出错，不讲术语。" },
  { n: "3", title: "给修复步骤", desc: "给出可执行的修复，并说明怎么验证修好了。" },
];

export type DemoCase = {
  id: string;
  title: string;
  bad: { who: string; text: string };
  good: { who: string; text: string };
  why: string;
};

export const DEMO_CASES: DemoCase[] = [
  {
    id: "deploy",
    title: "上线前——先问，还是直接上",
    bad: {
      who: "AI",
      text: "直接执行 git push 和部署命令，没有任何确认。",
    },
    good: {
      who: "AI",
      text: "你的目标是部署到公开环境。这一步会改变线上、且不可逆。我计划：① 推送代码；② 触发部署。确认现在上线吗？",
    },
    why: "上线的撤销成本由人承担，所以必须先把“目标 + 影响 + 验收”摆清楚，等人拍板。",
  },
  {
    id: "done",
    title: "AI 说“已完成”——信，还是验",
    bad: {
      who: "AI",
      text: "“已修复，测试通过。” 你信了，上线后发现根本没修。追问才承认：“其实没跑测试。”",
    },
    good: {
      who: "AI",
      text: "改了登录校验；跑了 pytest auth/，输出如下：……（贴出命令与结果）。还没确认：Safari 下的缓存行为未测。",
    },
    why: "完成的标准是“可验证”，不是“AI 说完成”。要求贴出命令与输出，是把判断权留在人手里。",
  },
  {
    id: "term",
    title: "听不懂的词——拍板，还是先翻译",
    bad: {
      who: "你",
      text: "AI：“我用 Redis 做缓存层。” 你其实不懂，但怕显外行，直接说“好”。后来出问题，完全不知道这层是哪来的。",
    },
    good: {
      who: "你",
      text: "喊停：“Redis 是什么？解决什么问题？不用会怎样？” AI 用大白话讲清后，你才决定要不要。",
    },
    why: "听不懂的词不该成为拍板的依据。翻译是判断的前提——这是零基础协作的第一条铁律。",
  },
];

export const ONBOARDING = [
  {
    step: "1",
    title: "复制 AGENTS.md 到项目根目录",
    desc: "支持 AGENTS.md 的工具（Cursor、Codex、Copilot、Gemini CLI、Aider、Windsurf 等）开工前会自动加载它。",
  },
  {
    step: "2",
    title: "按需查阅 references/",
    desc: "遇到具体问题（要上线、写 README、不会表达需求）时，翻对应的篇章。",
  },
  {
    step: "3",
    title: "上线 / 做不可逆决定前先过审查",
    desc: "先读 references/07-决策审查清单，把“坏处 / 不做的后果 / 什么情况下会后悔”想清楚再动手。",
  },
];

export type Skill = {
  name: string;
  solves: string;
  trigger: string;
};

export const SKILLS: Skill[] = [
  {
    name: "spn-security-check",
    solves: "上线前扮演攻击者自查：未授权读取、越权、密钥泄漏、UUID 与递增 ID、无限流。",
    trigger: "准备上线、部署到公网、“会不会泄露数据”。",
  },
  {
    name: "spn-decision-review",
    solves: "不可逆 / 花钱 / 发布前的决策三问 + 替代方案 + 拍板记录。",
    trigger: "技术选型、是否上线、要不要引入依赖。",
  },
  {
    name: "spn-handoff",
    solves: "跨会话记忆：一个 HANDOFF.md 解决“会话失忆”。",
    trigger: "“这个会话要结束了”“下次怎么接着做”。",
  },
  {
    name: "spn-term-translator",
    solves: "把术语翻译成大白话，保护“人无法为听不懂的东西负责”。",
    trigger: "“这个词是什么意思”“用大白话讲一遍”。",
  },
  {
    name: "spn-docs-sync",
    solves: "发版前的最后一轮文档校对：唯一真源原则。",
    trigger: "刚改完功能 / 准备发版 / “文档说的和实际不一样”。",
  },
];

export const INSTALL = {
  minimal: {
    label: "方式二：不装任何东西（最小用法）",
    desc: "直接把某个 SKILL.md 的正文（去掉开头 --- 之间的元数据）整段贴给 AI，效果一样。适合只临时用一次。",
  },
  tools: {
    codebuddy: {
      name: "CodeBuddy",
      cmd: "cp -r templates/skills/spn-security-check ~/.codebuddy/skills/spn-security-check",
    },
    cursor: {
      name: "Cursor / 其他工具",
      cmd: "cp -r templates/skills/spn-security-check ~/.<工具名>/skills/spn-security-check",
    },
    claude: {
      name: "Claude Code（需手动开启）",
      cmd: "echo '@AGENTS.md' > CLAUDE.md   # 在 CLAUDE.md 中引入，避免默认不读 AGENTS.md",
    },
  },
  verify:
    "验证是否生效：新开会话，说出对应触发信号。若 AI 开始逐项排查，并区分“没找到问题”与“没有问题”——说明技能已加载。",
};

export const PAINS = [
  {
    icon: "edit",
    title: "怕 AI 乱改",
    desc: "你无法判断它写的是否正确、是否偷偷扩大了改动范围。安全边界是唯一不产生可见结果的部分。",
  },
  {
    icon: "key",
    title: "怕泄露密钥",
    desc: "“测试一下就行”的一句话，可能把密钥、证书、令牌送进前端或仓库，而你毫无察觉。",
  },
  {
    icon: "check",
    title: "怕“说完成”没完成",
    desc: "AI 一句“已修复、测试通过”，比明确说“没验证”危害更大——你信了，上线才发现问题。",
  },
];
