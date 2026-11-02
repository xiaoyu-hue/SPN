// 全站文案唯一来源（中英双语，结构完全一致）。
// 内容摘抄自 SPN 仓库根目录 AGENTS.md / README.md / references/05，保持与仓库一致。
// 新增文案请同时补 zh 与 en 两份，否则 TypeScript 会报错兜底。

export type Lang = "zh" | "en";

export const zh = {
  meta: {
    htmlLang: "zh-CN",
    title: "SPN · 零基础 × AI 协作规则",
    description:
      "代码是 AI 写的，判断是你做的。一套写给不懂代码的人的 AI 协作规则与安全边界。",
  },
  site: {
    name: "SPN",
    tagline: "零基础 × AI 协作规则",
    coreClaim: "代码是 AI 写的，判断是你做的。",
    intro:
      "SPN（Self-precipitation，自我析出）是一套写给不懂代码的人的 AI 协作规则：在 AI 给出的众多选项里，让你的判断沉淀、成形。AI 提供能力与方案，你负责拍板与划边界。",
    github: "https://github.com/xiaoyu-hue/SPN",
    version: "v1.1.0",
    licenseSlash: "代码 MIT / 文档 CC BY 4.0",
    licenseDot: "代码 MIT · 文档 CC BY 4.0",
  },
  skip: "跳到主要内容",
  nav: {
    links: [
      { href: "#pain", label: "痛点" },
      { href: "#rules", label: "核心规则" },
      { href: "#demo", label: "互动演示" },
      { href: "#start", label: "三步上手" },
      { href: "#skills", label: "技能包" },
      { href: "#install", label: "安装" },
    ],
    githubAria: "在 GitHub 查看",
    quickStart: "快速开始",
    quickStartHref: "#快速开始",
  },
  hero: {
    eyebrowOpen: "开源",
    titleLead1: "代码是 ",
    titleHi1: "AI 写的",
    titleLead2: "判断是 ",
    titleHi2: "你做的",
    primaryBtn: "在 GitHub 查看",
    ghostBtn: "三步上手",
    chatTitle: "与 AI 的协作现场",
    chatYou: "你：",
    chatUser: "帮我把这个项目部署上线。",
    chatAi: "AI：",
    chatAiText:
      "这一步会改变线上且不可逆。我计划：① 推送代码；② 触发部署。确认现在上线吗？",
    chatNote: "红线之上，AI 不替你拍板——这就是 SPN。",
  },
  pain: {
    eyebrow: "为什么需要 SPN",
    title: "不懂代码，用 AI 也有三怕",
    lead: "AI 编程工具默认优化“演示能跑”。对懂代码的人是效率，对不懂代码的人是风险——你无法判断它写的是否正确、是否偷偷扩大了改动范围。",
    items: [
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
    ],
  },
  rules: {
    eyebrow: "核心规则速览",
    title: "谁做决定，什么时候必须停",
    lead: "常见模板写“用什么命令、什么代码风格”；SPN 写“谁做决定、什么时候必须停”。一半篇幅写不能做什么、做不到什么。",
    tabs: [
      { id: "auth", label: "🟢🟡🔴 三档授权" },
      { id: "actions", label: "三个关键动作" },
      { id: "thinking", label: "三视角分析" },
      { id: "debug", label: "调试三步法" },
    ],
    auth: [
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
    ],
    keyActions: [
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
    ],
    thinking: [
      { title: "全力反驳", desc: "假设方案是错的，列出它会在哪些地方翻车。" },
      { title: "切换支持", desc: "反过来，它成立的条件是什么、好处是什么。" },
      { title: "中立对比", desc: "把备选方案并排，按代价 / 风险 / 扩展性客观对比。" },
    ],
    debugSteps: [
      { n: "1", title: "描述报错", desc: "把错误原文贴出来，说清发生在哪一步。" },
      { n: "2", title: "大白话解释原因", desc: "用生活比喻讲清为什么出错，不讲术语。" },
      { n: "3", title: "给修复步骤", desc: "给出可执行的修复，并说明怎么验证修好了。" },
    ],
  },
  demo: {
    eyebrow: "互动演示",
    title: "同样一句话，AI 的边界感天差地别",
    lead: "点开看三种典型场景。左边是“没套 SPN”的 AI——直接干、报喜不报忧、用听不懂的词糊弄你；右边是“套了 SPN”的 AI——先问、贴证据、把判断权还给你。",
    badLabel: "没套 SPN 的 AI",
    goodLabel: "套了 SPN 的 AI",
    whyLabel: "为什么这很关键",
    cases: [
      {
        id: "deploy",
        title: "上线前——先问，还是直接上",
        bad: { who: "AI", text: "直接执行 git push 和部署命令，没有任何确认。" },
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
    ],
  },
  start: {
    eyebrow: "三步上手",
    title: "把规则交给 AI，只要三件事",
    lead: "不是“学一套方法论”，而是“把文件放进项目、按场景取用”。零基础上手，懂中文就行。",
    steps: [
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
    ],
  },
  skills: {
    eyebrow: "技能包",
    title: "不是一本手册，是一组可触发的“专家”",
    lead: "每个技能包是一个具体场景下的护栏：说出触发信号，AI 就切换成对应的审查者。以下是已内置的几个。",
    triggerPrefix: "触发：",
    items: [
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
    ],
  },
  install: {
    eyebrow: "安装指引",
    title: "按你用的工具，复制一条命令",
    lead: "推荐把技能包放进工具的 skills 目录；临时用一次，直接把 SKILL.md 正文贴给 AI 也行。",
    copyAria: "复制",
    tools: [
      {
        name: "CodeBuddy",
        cmd: "cp -r templates/skills/spn-security-check ~/.codebuddy/skills/spn-security-check",
      },
      {
        name: "Cursor / 其他工具",
        cmd: "cp -r templates/skills/spn-security-check ~/.<工具名>/skills/spn-security-check",
      },
      {
        name: "Claude Code（需手动开启）",
        cmd: "echo '@AGENTS.md' > CLAUDE.md   # 在 CLAUDE.md 中引入，避免默认不读 AGENTS.md",
      },
    ],
    minimal: {
      label: "方式二：不装任何东西（最小用法）",
      desc: "直接把某个 SKILL.md 的正文（去掉开头 --- 之间的元数据）整段贴给 AI，效果一样。适合只临时用一次。",
    },
    verifyTitle: "怎么验证生效",
    verify:
      "验证是否生效：新开会话，说出对应触发信号。若 AI 开始逐项排查，并区分“没找到问题”与“没有问题”——说明技能已加载。",
  },
  footer: {
    viewGithub: "在 GitHub 上查看与贡献",
  },
  bottomNav: {
    aria: "底部导航",
    rules: "规则",
    demo: "演示",
    start: "上手",
    install: "安装",
  },
  backToTop: "回到顶部",
  langToggle: {
    show: "EN",
    aria: "Switch to English",
  },
};

export type Content = typeof zh;

export const en: Content = {
  meta: {
    htmlLang: "en",
    title: "SPN · AI Collaboration Rules for Non-Programmers",
    description:
      "The code is written by AI; the judgment is yours. A set of AI collaboration rules and safety boundaries written for people who don't code.",
  },
  site: {
    name: "SPN",
    tagline: "AI collaboration rules for non-programmers",
    coreClaim: "The code is written by AI; the judgment is yours.",
    intro:
      "SPN (Self-precipitation) is a set of AI collaboration rules written for people who don't code: among the many options an AI offers, your judgment settles and takes shape. The AI provides capability and solutions; you make the call and set the boundaries.",
    github: "https://github.com/xiaoyu-hue/SPN",
    version: "v1.1.0",
    licenseSlash: "Code MIT / Docs CC BY 4.0",
    licenseDot: "Code MIT · Docs CC BY 4.0",
  },
  skip: "Skip to main content",
  nav: {
    links: [
      { href: "#pain", label: "Pain points" },
      { href: "#rules", label: "Core rules" },
      { href: "#demo", label: "Demo" },
      { href: "#start", label: "Get started" },
      { href: "#skills", label: "Skills" },
      { href: "#install", label: "Install" },
    ],
    githubAria: "View on GitHub",
    quickStart: "Quick start",
    quickStartHref: "#快速开始",
  },
  hero: {
    eyebrowOpen: "Open source",
    titleLead1: "Code is ",
    titleHi1: "written by AI",
    titleLead2: "the judgment is ",
    titleHi2: "yours",
    primaryBtn: "View on GitHub",
    ghostBtn: "Get started",
    chatTitle: "A live collaboration scene",
    chatYou: "You: ",
    chatUser: "Deploy this project for me.",
    chatAi: "AI: ",
    chatAiText:
      "This step changes production and is irreversible. My plan: 1) push the code; 2) trigger the deploy. Confirm release now?",
    chatNote: "Above the red line, the AI never decides for you — that is SPN.",
  },
  pain: {
    eyebrow: "Why SPN exists",
    title: "Three fears when using AI without reading code",
    lead: "AI coding tools optimize for “the demo runs”. If you read code, that's speed; if you don't, it's risk — you can't tell whether it's correct, or whether the change quietly grew.",
    items: [
      {
        icon: "edit",
        title: "Fear of uncontrolled edits",
        desc: "You can't tell whether what it wrote is correct, or whether it quietly widened the change scope. Safety boundaries are the one part that never shows a visible result.",
      },
      {
        icon: "key",
        title: "Fear of leaking secrets",
        desc: "“Just to test it” — one sentence can send keys, certificates or tokens into your frontend or repo, without you noticing.",
      },
      {
        icon: "check",
        title: "Fear of “done” that isn't done",
        desc: "An AI's “fixed, tests pass” is more harmful than an honest “not verified” — you believe it and only find out after launch.",
      },
    ],
  },
  rules: {
    eyebrow: "Core rules at a glance",
    title: "Who decides, and when you must stop",
    lead: "Common templates spell out “which commands, which code style”; SPN spells out “who decides, when to stop”. Half of it is about what you must not do — and what AI can't do.",
    tabs: [
      { id: "auth", label: "🟢🟡🔴 Authorization tiers" },
      { id: "actions", label: "Three key actions" },
      { id: "thinking", label: "Three-perspective review" },
      { id: "debug", label: "Debug in 3 steps" },
    ],
    auth: [
      {
        tier: "allow",
        title: "Just do it",
        emoji: "🟢",
        items: [
          "Read files, check logs, research, diagnose, review",
          "Edit files in the working directory, run tests, verify locally",
          "Local git commit (reversible, reflog exists)",
          "Run tests, lint and type checks right after edits",
        ],
      },
      {
        tier: "ask",
        title: "Ask before doing",
        emoji: "🟡",
        items: [
          "Delete or overwrite files you didn't create",
          "Change database schema, run data migrations",
          "Add production dependencies, deploy to production, public releases",
          "Outbound actions (sending email, opening PRs, public replies)",
          "Batch operations affecting more than 5 files/records",
          "Rewriting Git history in ways that affect others (push, force-push…)",
        ],
      },
      {
        tier: "forbid",
        title: "Never do this",
        emoji: "🔴",
        items: [
          "Commit .env files, keys, certificates or tokens to the repo",
          "Put service_role / sk_live / private keys in frontend code",
          "Do permission checks only in the frontend — hiding buttons isn't access control",
          "Concatenate SQL or splice user input into commands",
          "Silently skip errors, add implicit fallbacks, fabricate data",
          "Invent code / test results, or claim verification that never ran",
        ],
      },
    ],
    keyActions: [
      {
        n: "01",
        title: "Translate jargon before deciding",
        desc: "Never decide on words you don't understand. Not understanding isn't your failure — it's the speaker's.",
      },
      {
        n: "02",
        title: "Try first, then ask",
        desc: "One test only: can it be undone in one click? If yes, try; if no, ask. This settles most hesitation.",
      },
      {
        n: "03",
        title: "Capability isn't assurance",
        desc: "An AI can write encryption code, but the statement “not yet audited” has to be written by you.",
      },
    ],
    thinking: [
      { title: "Argue against", desc: "Assume the plan is wrong; list where it would break." },
      { title: "Argue for", desc: "Flip it: under what conditions does it hold, and what does it gain?" },
      { title: "Compare neutrally", desc: "Put the options side by side; compare cost / risk / scalability objectively." },
    ],
    debugSteps: [
      { n: "1", title: "Describe the error", desc: "Paste the original message; say exactly where it happened." },
      { n: "2", title: "Explain in plain words", desc: "Use a real-life metaphor for why it failed — no jargon." },
      { n: "3", title: "Give the fix", desc: "Provide an actionable fix, and explain how to verify it's fixed." },
    ],
  },
  demo: {
    eyebrow: "Interactive demo",
    title: "Same sentence, worlds apart in boundary awareness",
    lead: "Open the three typical scenarios. Left: the AI “without SPN” — acts directly, reports only good news, fogs you with jargon. Right: the AI “with SPN” — asks first, shows evidence, hands judgment back to you.",
    badLabel: "AI without SPN",
    goodLabel: "AI with SPN",
    whyLabel: "Why this matters",
    cases: [
      {
        id: "deploy",
        title: "Before release — ask first, or just go",
        bad: { who: "AI", text: "Runs git push and the deploy commands directly, with no confirmation." },
        good: {
          who: "AI",
          text: "Your goal is deploying to a public environment. This step changes production and is irreversible. My plan: 1) push the code; 2) trigger the deploy. Confirm release now?",
        },
        why: "The cost of undoing a release is borne by you, so “goal + impact + acceptance” must be laid out first, and a human must approve.",
      },
      {
        id: "done",
        title: "AI says “done” — trust it, or verify",
        bad: {
          who: "AI",
          text: "“Fixed, tests pass.” You believed it; after launch nothing was fixed. Pressed further, it admits: “I actually never ran the tests.”",
        },
        good: {
          who: "AI",
          text: "Changed the login validation; ran pytest auth/, output below: … (command and results attached). Still unverified: Safari cache behavior untested.",
        },
        why: "The standard for “done” is verifiability, not “the AI says so”. Demanding commands and output keeps the judgment with you.",
      },
      {
        id: "term",
        title: "A term you don't understand — decide, or translate first",
        bad: {
          who: "You",
          text: "AI: “I'll use Redis as the cache layer.” You don't really get it but fear looking clueless, so you say “OK”. Later something breaks and you have no idea what that layer is.",
        },
        good: {
          who: "You",
          text: "You stop it: “What is Redis? What problem does it solve? What happens without it?” Only after the AI explains in plain words do you decide.",
        },
        why: "Terms you don't understand should never be the basis for a decision. Translating comes before judging — the first iron rule of no-code collaboration.",
      },
    ],
  },
  start: {
    eyebrow: "Get started in 3 steps",
    title: "Handing the rules to the AI takes three things",
    lead: "Not “learn a methodology” — “drop the files into the project and use them per scenario”. Zero setup knowledge required.",
    steps: [
      {
        step: "1",
        title: "Copy AGENTS.md to your project root",
        desc: "Tools that support AGENTS.md (Cursor, Codex, Copilot, Gemini CLI, Aider, Windsurf…) load it automatically before work.",
      },
      {
        step: "2",
        title: "Consult references/ as needed",
        desc: "When you hit a concrete problem (going live, writing a README, expressing what you want), open the matching chapter.",
      },
      {
        step: "3",
        title: "Run the review before launch / irreversible calls",
        desc: "Read the decision-review checklist first: think through “downsides / cost of not doing it / when you'd regret it” before acting.",
      },
    ],
  },
  skills: {
    eyebrow: "Skill packs",
    title: "Not a manual — a set of triggerable “experts”",
    lead: "Each skill pack is a guardrail for a concrete scenario: say the trigger phrase and the AI switches into the matching reviewer. These are built in.",
    triggerPrefix: "Trigger: ",
    items: [
      {
        name: "spn-security-check",
        solves: "Plays the attacker before launch: unauthorized reads, privilege escalation, leaked keys, UUID vs sequential IDs, missing rate limits.",
        trigger: "About to go live, deploy publicly, “could this leak data”.",
      },
      {
        name: "spn-decision-review",
        solves: "The three decision questions + alternatives + a decision log before anything irreversible, costly, or public.",
        trigger: "Tech choices, go/no-go, adding a dependency.",
      },
      {
        name: "spn-handoff",
        solves: "Cross-session memory: one HANDOFF.md solves “session amnesia”.",
        trigger: "“This session is ending” “how do I pick this up next time”.",
      },
      {
        name: "spn-term-translator",
        solves: "Translates jargon into plain language, upholding “a person can't be responsible for what they don't understand”.",
        trigger: "“What does this word mean” “explain it in plain words”.",
      },
      {
        name: "spn-docs-sync",
        solves: "The final docs proofread before a release: single source of truth.",
        trigger: "Just changed a feature / about to release / “the docs don't match reality”.",
      },
    ],
  },
  install: {
    eyebrow: "Install guide",
    title: "Copy one command for the tool you use",
    lead: "Drop the skill packs into your tool's skills directory; for one-off use, just paste a SKILL.md body to the AI.",
    copyAria: "Copy",
    tools: [
      {
        name: "CodeBuddy",
        cmd: "cp -r templates/skills/spn-security-check ~/.codebuddy/skills/spn-security-check",
      },
      {
        name: "Cursor / other tools",
        cmd: "cp -r templates/skills/spn-security-check ~/.<tool-name>/skills/spn-security-check",
      },
      {
        name: "Claude Code (manual enable)",
        cmd: "echo '@AGENTS.md' > CLAUDE.md   # import it in CLAUDE.md — Claude doesn't read AGENTS.md by default",
      },
    ],
    minimal: {
      label: "Option B: install nothing (minimal usage)",
      desc: "Paste a SKILL.md's body (minus the metadata between the opening --- markers) straight to the AI — same effect. Best for one-off use.",
    },
    verifyTitle: "How to verify it works",
    verify:
      "Open a new session and say the matching trigger phrase. If the AI starts checking item by item and distinguishes “issue not found” from “no issues found” — the skill is loaded.",
  },
  footer: {
    viewGithub: "View & contribute on GitHub",
  },
  bottomNav: {
    aria: "Bottom navigation",
    rules: "Rules",
    demo: "Demo",
    start: "Start",
    install: "Install",
  },
  backToTop: "Back to top",
  langToggle: {
    show: "中",
    aria: "切换到中文",
  },
};
