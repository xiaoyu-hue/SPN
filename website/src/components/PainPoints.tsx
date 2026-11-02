import { Pencil, KeyRound, CheckCircle2 } from "lucide-react";
import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { useI18n } from "@/i18n";

const ICONS: Record<string, typeof Pencil> = {
  edit: Pencil,
  key: KeyRound,
  check: CheckCircle2,
};

export function PainPoints() {
  const { t } = useI18n();
  return (
    <section id="pain" className="section container-page">
      <Reveal>
        <span className="eyebrow">{t.pain.eyebrow}</span>
        <h2 className="section-title">{t.pain.title}</h2>
        <p className="lead">{t.pain.lead}</p>
      </Reveal>

      <div className="mt-10 grid gap-5 md:grid-cols-3">
        {t.pain.items.map((p, i) => {
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
