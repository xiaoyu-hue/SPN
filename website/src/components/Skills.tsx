import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { useI18n } from "@/i18n";
import { Sparkles, Zap } from "lucide-react";

export function Skills() {
  const { t } = useI18n();
  return (
    <section id="skills" className="section container-page">
      <Reveal>
        <span className="eyebrow">{t.skills.eyebrow}</span>
        <h2 className="section-title">{t.skills.title}</h2>
        <p className="lead">{t.skills.lead}</p>
      </Reveal>

      <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {t.skills.items.map((s, i) => (
          <Reveal key={s.name} delay={(i % 3) * 0.07}>
            <Glass className="flex h-full flex-col p-6">
              <div className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-brand-soft" />
                <code className="font-mono text-sm text-white">{s.name}</code>
              </div>
              <p className="mt-3 text-sm leading-relaxed text-[var(--text-dim)]">{s.solves}</p>
              <div className="mt-auto flex items-start gap-2 pt-4 text-xs text-[var(--text-faint)]">
                <Zap className="mt-0.5 h-3.5 w-3.5 shrink-0 text-sand" />
                <span>
                  <span className="text-[var(--text-dim)]">{t.skills.triggerPrefix}</span>
                  {s.trigger}
                </span>
              </div>
            </Glass>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
