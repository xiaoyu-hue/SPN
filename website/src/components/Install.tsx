import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { useI18n } from "@/i18n";
import { Copy, Check } from "lucide-react";
import { useState } from "react";

function CodeBlock({ code, copyAria }: { code: string; copyAria: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <div className="relative">
      <pre className="overflow-x-auto whitespace-pre-wrap break-words rounded-xl bg-black/40 p-4 font-mono text-[0.82rem] leading-relaxed text-emerald-100/90 ring-1 ring-white/10">
        <code>{code}</code>
      </pre>
      <button
        onClick={() => {
          navigator.clipboard?.writeText(code);
          setCopied(true);
          setTimeout(() => setCopied(false), 1500);
        }}
        className="absolute right-2.5 top-2.5 rounded-md bg-white/10 p-1.5 text-white/70 transition-colors hover:bg-white/20 hover:text-white"
        aria-label={copyAria}
      >
        {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
      </button>
    </div>
  );
}

export function Install() {
  const { t } = useI18n();
  return (
    <section id="install" className="section container-page">
      <Reveal>
        <span className="eyebrow">{t.install.eyebrow}</span>
        <h2 className="section-title">{t.install.title}</h2>
        <p className="lead">{t.install.lead}</p>
      </Reveal>

      <Reveal delay={0.05} className="mt-10 grid gap-5 lg:grid-cols-2">
        {t.install.tools.map((tool) => (
          <Glass key={tool.name} refract className="p-5">
            <div className="text-sm font-semibold text-white">{tool.name}</div>
            <div className="mt-3">
              <CodeBlock code={tool.cmd} copyAria={t.install.copyAria} />
            </div>
          </Glass>
        ))}

        <Glass className="p-5 lg:col-span-2">
          <div className="text-xs font-medium uppercase tracking-wider text-brand-soft">
            {t.install.minimal.label}
          </div>
          <p className="mt-2 text-sm leading-relaxed text-[var(--text-dim)]">
            {t.install.minimal.desc}
          </p>
        </Glass>
      </Reveal>

      <Reveal delay={0.08} className="mt-5">
        <Glass className="p-5">
          <div className="text-xs font-medium uppercase tracking-wider text-sand">
            {t.install.verifyTitle}
          </div>
          <p className="mt-2 text-sm leading-relaxed text-[var(--text-dim)]">
            {t.install.verify}
          </p>
        </Glass>
      </Reveal>
    </section>
  );
}
