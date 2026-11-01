import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { ONBOARDING } from "@/content";

export function HowItWorks() {
  return (
    <section id="start" className="section container-page">
      <Reveal>
        <span className="eyebrow">三步上手</span>
        <h2 className="section-title">把规则交给 AI，只要三件事</h2>
        <p className="lead">
          不是“学一套方法论”，而是“把文件放进项目、按场景取用”。零基础上手，懂中文就行。
        </p>
      </Reveal>

      <div className="mt-10 grid gap-5 md:grid-cols-3">
        {ONBOARDING.map((s, i) => (
          <Reveal key={s.step} delay={i * 0.08}>
            <Glass refract className="h-full p-6">
              <div className="flex items-center gap-3">
                <span className="font-mono text-3xl font-bold text-brand-soft">{s.step}</span>
                <span className="h-px flex-1 bg-white/10" />
              </div>
              <h3 className="mt-4 text-lg font-semibold text-white">{s.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-[var(--text-dim)]">{s.desc}</p>
            </Glass>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
