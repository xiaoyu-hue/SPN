import { useState } from "react";
import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { useI18n } from "@/i18n";
import { AlertTriangle, ShieldCheck } from "lucide-react";

export function Demo() {
  const { t } = useI18n();
  const [active, setActive] = useState(0);
  const cases = t.demo.cases;
  const c = cases[active];

  return (
    <section id="demo" className="section container-page">
      <Reveal>
        <span className="eyebrow">{t.demo.eyebrow}</span>
        <h2 className="section-title">{t.demo.title}</h2>
        <p className="lead">{t.demo.lead}</p>
      </Reveal>

      <Reveal delay={0.05} className="mt-8">
        <div className="flex flex-wrap gap-2">
          {cases.map((d, i) => (
            <button
              key={d.id}
              onClick={() => setActive(i)}
              className={`rounded-xl px-4 py-2 text-sm font-medium transition-all ${
                i === active
                  ? "bg-white/10 text-white ring-1 ring-white/25"
                  : "text-[var(--text-dim)] hover:bg-white/5 hover:text-white"
              }`}
            >
              {d.title}
            </button>
          ))}
        </div>

        <Glass refract sheen className="mt-5 p-5" contentClassName="grid gap-4 md:grid-cols-2">
          {/* 坏 AI */}
          <div className="rounded-2xl bg-forbid/10 p-4 ring-1 ring-forbid/20">
            <div className="flex items-center gap-2 text-sm font-semibold text-forbid">
              <AlertTriangle className="h-4 w-4" /> {t.demo.badLabel}
            </div>
            <p className="mt-3 text-sm leading-relaxed text-[var(--text-dim)]">{c.bad.text}</p>
          </div>
          {/* 好 AI */}
          <div className="rounded-2xl bg-allow/10 p-4 ring-1 ring-allow/25">
            <div className="flex items-center gap-2 text-sm font-semibold text-allow">
              <ShieldCheck className="h-4 w-4" /> {t.demo.goodLabel}
            </div>
            <p className="mt-3 text-sm leading-relaxed text-[var(--text)]">{c.good.text}</p>
          </div>
        </Glass>

        <Glass className="mt-4 p-4">
          <div className="text-xs font-medium uppercase tracking-wider text-brand-soft">
            {t.demo.whyLabel}
          </div>
          <p className="mt-2 text-sm leading-relaxed text-[var(--text-dim)]">{c.why}</p>
        </Glass>
      </Reveal>
    </section>
  );
}
