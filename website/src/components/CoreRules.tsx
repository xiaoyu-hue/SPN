import { useState } from "react";
import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import {
  AUTHORIZATION,
  KEY_ACTIONS,
  THINKING,
  DEBUG_STEPS,
} from "@/content";

const TIER_STYLE: Record<string, string> = {
  allow: "text-allow",
  ask: "text-ask",
  forbid: "text-forbid",
};

const TABS = [
  { id: "auth", label: "🟢🟡🔴 三档授权" },
  { id: "actions", label: "三个关键动作" },
  { id: "thinking", label: "三视角分析" },
  { id: "debug", label: "调试三步法" },
] as const;

function AuthPanel() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {AUTHORIZATION.map((a) => (
        <Glass key={a.tier} className="p-5">
          <div className={`text-lg font-semibold ${TIER_STYLE[a.tier]}`}>
            {a.emoji} {a.title}
          </div>
          <ul className="mt-3 space-y-2">
            {a.items.map((it) => (
              <li key={it} className="flex gap-2 text-sm text-[var(--text-dim)]">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-white/30" />
                {it}
              </li>
            ))}
          </ul>
        </Glass>
      ))}
    </div>
  );
}

function ActionsPanel() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {KEY_ACTIONS.map((a) => (
        <Glass key={a.n} className="p-5">
          <div className="font-mono text-sm text-brand-soft">{a.n}</div>
          <h4 className="mt-2 font-semibold text-white">{a.title}</h4>
          <p className="mt-2 text-sm leading-relaxed text-[var(--text-dim)]">{a.desc}</p>
        </Glass>
      ))}
    </div>
  );
}

function ThinkingPanel() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {THINKING.map((t, i) => (
        <Glass key={t.title} className="p-5">
          <div className="flex items-center gap-2">
            <span className="flex h-7 w-7 items-center justify-center rounded-full bg-white/10 text-xs font-bold text-brand-soft">
              {i + 1}
            </span>
            <h4 className="font-semibold text-white">{t.title}</h4>
          </div>
          <p className="mt-3 text-sm leading-relaxed text-[var(--text-dim)]">{t.desc}</p>
        </Glass>
      ))}
    </div>
  );
}

function DebugPanel() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {DEBUG_STEPS.map((s) => (
        <Glass key={s.n} className="p-5">
          <div className="font-mono text-2xl font-bold text-brand-soft">{s.n}</div>
          <h4 className="mt-2 font-semibold text-white">{s.title}</h4>
          <p className="mt-2 text-sm leading-relaxed text-[var(--text-dim)]">{s.desc}</p>
        </Glass>
      ))}
    </div>
  );
}

const PANELS: Record<string, () => JSX.Element> = {
  auth: AuthPanel,
  actions: ActionsPanel,
  thinking: ThinkingPanel,
  debug: DebugPanel,
};

export function CoreRules() {
  const [tab, setTab] = useState<(typeof TABS)[number]["id"]>("auth");
  const Panel = PANELS[tab];

  return (
    <section id="rules" className="section container-page">
      <Reveal>
        <span className="eyebrow">核心规则速览</span>
        <h2 className="section-title">谁做决定，什么时候必须停</h2>
        <p className="lead">
          常见模板写“用什么命令、什么代码风格”；SPN 写“谁做决定、什么时候必须停”。
          一半篇幅写不能做什么、做不到什么。
        </p>
      </Reveal>

      <Reveal delay={0.05} className="mt-8">
        <div className="flex flex-wrap gap-2">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`rounded-xl px-4 py-2 text-sm font-medium transition-all ${
                tab === t.id
                  ? "bg-white/10 text-white ring-1 ring-white/25"
                  : "text-[var(--text-dim)] hover:bg-white/5 hover:text-white"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
        <div className="mt-5">
          <Panel />
        </div>
      </Reveal>
    </section>
  );
}
