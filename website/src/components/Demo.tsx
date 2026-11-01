import { useState } from "react";
import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { DEMO_CASES } from "@/content";
import { AlertTriangle, ShieldCheck } from "lucide-react";

export function Demo() {
  const [active, setActive] = useState(0);
  const c = DEMO_CASES[active];

  return (
    <section id="demo" className="section container-page">
      <Reveal>
        <span className="eyebrow">互动演示</span>
        <h2 className="section-title">同样一句话，AI 的边界感天差地别</h2>
        <p className="lead">
          点开看三种典型场景。左边是“没套 SPN”的 AI——直接干、报喜不报忧、用听不懂的词糊弄你；
          右边是“套了 SPN”的 AI——先问、贴证据、把判断权还给你。
        </p>
      </Reveal>

      <Reveal delay={0.05} className="mt-8">
        <div className="flex flex-wrap gap-2">
          {DEMO_CASES.map((d, i) => (
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
              <AlertTriangle className="h-4 w-4" /> 没套 SPN 的 AI
            </div>
            <p className="mt-3 text-sm leading-relaxed text-[var(--text-dim)]">{c.bad.text}</p>
          </div>
          {/* 好 AI */}
          <div className="rounded-2xl bg-allow/10 p-4 ring-1 ring-allow/25">
            <div className="flex items-center gap-2 text-sm font-semibold text-allow">
              <ShieldCheck className="h-4 w-4" /> 套了 SPN 的 AI
            </div>
            <p className="mt-3 text-sm leading-relaxed text-[var(--text)]">{c.good.text}</p>
          </div>
        </Glass>

        <Glass className="mt-4 p-4">
          <div className="text-xs font-medium uppercase tracking-wider text-brand-soft">
            为什么这很关键
          </div>
          <p className="mt-2 text-sm leading-relaxed text-[var(--text-dim)]">{c.why}</p>
        </Glass>
      </Reveal>
    </section>
  );
}
