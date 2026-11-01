import { Github, ShieldCheck } from "lucide-react";
import { SITE } from "@/content";

export function Footer() {
  return (
    <footer className="border-t border-white/10">
      <div className="container-page flex flex-col items-start justify-between gap-6 py-10 sm:flex-row sm:items-center">
        <div className="flex items-center gap-3">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-brand to-sand text-sm font-bold text-ink">
            S
          </span>
          <div>
            <div className="text-sm font-semibold text-white">{SITE.name}</div>
            <div className="text-xs text-[var(--text-faint)]">{SITE.coreClaim}</div>
          </div>
        </div>

        <div className="flex flex-col gap-2 text-sm text-[var(--text-dim)] sm:items-end">
          <a
            href={SITE.github}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 transition-colors hover:text-white"
          >
            <Github className="h-4 w-4" /> 在 GitHub 上查看与贡献
          </a>
          <span className="inline-flex items-center gap-2 text-xs text-[var(--text-faint)]">
            <ShieldCheck className="h-3.5 w-3.5" /> 代码 MIT · 文档 CC BY 4.0 · {SITE.version}
          </span>
        </div>
      </div>
    </footer>
  );
}
