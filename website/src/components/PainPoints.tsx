import { Pencil, KeyRound, CheckCircle2 } from "lucide-react";
import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { PAINS } from "@/content";

const ICONS: Record<string, typeof Pencil> = {
  edit: Pencil,
  key: KeyRound,
  check: CheckCircle2,
};

export function PainPoints() {
  return (
    <section id="pain" className="section container-page">
      <Reveal>
        <span className="eyebrow">为什么需要 SPN</span>
        <h2 className="section-title">不懂代码，用 AI 也有三怕</h2>
        <p className="lead">
          AI 编程工具默认优化“演示能跑”。对懂代码的人是效率，对不懂代码的人是风险——
          你无法判断它写的是否正确、是否偷偷扩大了改动范围。
        </p>
      </Reveal>

      <div className="mt-10 grid gap-5 md:grid-cols-3">
        {PAINS.map((p, i) => {
          const Icon = ICONS[p.icon] ?? Pencil;
          return (
            <Reveal key={p.title} delay={i * 0.08}>
              <Glass
                refract
                className="group h-full p-6 transition-transform duration-300 hover:-translate-y-1"
              >
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/5 text-brand-soft ring-1 ring-white/10 transition-colors group-hover:bg-white/10">
                  <Icon className="h-5 w-5" />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-white">{p.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-[var(--text-dim)]">
                  {p.desc}
                </p>
              </Glass>
            </Reveal>
          );
        })}
      </div>
    </section>
  );
}
