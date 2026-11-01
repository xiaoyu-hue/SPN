import { Reveal } from "@/components/effects/Reveal";
import { Glass } from "@/components/Glass";
import { INSTALL } from "@/content";
import { Copy, Check } from "lucide-react";
import { useState } from "react";

function CodeBlock({ code }: { code: string }) {
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
        aria-label="复制"
      >
        {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
      </button>
    </div>
  );
}

export function Install() {
  const tools = [
    INSTALL.tools.codebuddy,
    INSTALL.tools.cursor,
    INSTALL.tools.claude,
  ];
  return (
    <section id="install" className="section container-page">
      <Reveal>
        <span className="eyebrow">安装指引</span>
        <h2 className="section-title">按你用的工具，复制一条命令</h2>
        <p className="lead">
          推荐把技能包放进工具的 skills 目录；临时用一次，直接把 SKILL.md 正文贴给 AI 也行。
        </p>
      </Reveal>

      <Reveal delay={0.05} className="mt-10 grid gap-5 lg:grid-cols-2">
        {tools.map((t) => (
          <Glass key={t.name} refract className="p-5">
            <div className="text-sm font-semibold text-white">{t.name}</div>
            <div className="mt-3">
              <CodeBlock code={t.cmd} />
            </div>
          </Glass>
        ))}

        <Glass className="p-5 lg:col-span-2">
          <div className="text-xs font-medium uppercase tracking-wider text-brand-soft">
            {INSTALL.minimal.label}
          </div>
          <p className="mt-2 text-sm leading-relaxed text-[var(--text-dim)]">
            {INSTALL.minimal.desc}
          </p>
        </Glass>
      </Reveal>

      <Reveal delay={0.08} className="mt-5">
        <Glass className="p-5">
          <div className="text-xs font-medium uppercase tracking-wider text-sand">
            怎么验证生效
          </div>
          <p className="mt-2 text-sm leading-relaxed text-[var(--text-dim)]">
            {INSTALL.verify}
          </p>
        </Glass>
      </Reveal>
    </section>
  );
}
