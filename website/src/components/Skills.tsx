import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { SKILLS } from "@/content";
import { Sparkles, Zap } from "lucide-react";

export function Skills() {
  return (
    <section id="skills" className="section container-page">
      <Reveal>
        <span className="eyebrow">技能包</span>
        <h2 className="section-title">不是一本手册，是一组可触发的“专家”</h2>
        <p className="lead">
          每个技能包是一个具体场景下的护栏：说出触发信号，AI 就切换成对应的审查者。
          以下是已内置的几个。
        </p>
      </Reveal>

      <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {SKILLS.map((s, i) => (
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
                  <span className="text-[var(--text-dim)]">触发：</span>
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
