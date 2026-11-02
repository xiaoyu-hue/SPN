import { useState } from "react";
import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { useI18n } from "@/i18n";

const TIER_STYLE: Record<string, string> = {
  allow: "text-allow",
  ask: "text-ask",
  forbid: "text-forbid",
};

function AuthPanel() {
  const { t } = useI18n();
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {t.rules.auth.map((a) => (
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
  const { t } = useI18n();
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {t.rules.keyActions.map((a) => (
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
  const { t } = useI18n();
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {t.rules.thinking.map((th, i) => (
        <Glass key={th.title} className="p-5">
          <div className="flex items-center gap-2">
            <span className="flex h-7 w-7 items-center justify-center rounded-full bg-white/10 text-xs font-bold text-brand-soft">
              {i + 1}
            </span>
            <h4 className="font-semibold text-white">{th.title}</h4>
          </div>
          <p className="mt-3 text-sm leading-relaxed text-[var(--text-dim)]">{th.desc}</p>
        </Glass>
      ))}
    </div>
  );
}

function DebugPanel() {
  const { t } = useI18n();
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {t.rules.debugSteps.map((s) => (
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
  const { t } = useI18n();
  const [tab, setTab] = useState<string>("auth");
  const Panel = PANELS[tab];

  return (
    <section id="rules" className="section container-page">
      <Reveal>
        <span className="eyebrow">{t.rules.eyebrow}</span>
        <h2 className="section-title">{t.rules.title}</h2>
        <p className="lead">{t.rules.lead}</p>
      </Reveal>

      <Reveal delay={0.05} className="mt-8">
        <div className="flex flex-wrap gap-2">
          {t.rules.tabs.map((tb) => (
            <button
              key={tb.id}
              onClick={() => setTab(tb.id)}
              className={`rounded-xl px-4 py-2 text-sm font-medium transition-all ${
                tab === tb.id
                  ? "bg-white/10 text-white ring-1 ring-white/25"
                  : "text-[var(--text-dim)] hover:bg-white/5 hover:text-white"
              }`}
            >
              {tb.label}
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
