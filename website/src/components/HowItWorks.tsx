import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { useI18n } from "@/i18n";

export function HowItWorks() {
  const { t } = useI18n();
  return (
    <section id="start" className="section container-page">
      <Reveal>
        <span className="eyebrow">{t.start.eyebrow}</span>
        <h2 className="section-title">{t.start.title}</h2>
        <p className="lead">{t.start.lead}</p>
      </Reveal>

      <div className="mt-10 grid gap-5 md:grid-cols-3">
        {t.start.steps.map((s, i) => (
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
