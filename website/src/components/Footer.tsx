import { Github, ShieldCheck } from "lucide-react";
import { Logo } from "@/components/Logo";
import { useI18n } from "@/i18n";

export function Footer() {
  const { t } = useI18n();
  return (
    <footer className="border-t border-white/10">
      <div className="container-page flex flex-col items-start justify-between gap-6 py-10 sm:flex-row sm:items-center">
        <div className="flex items-center gap-3">
          <Logo size={36} className="shrink-0" />
          <div>
            <div className="text-sm font-semibold text-white">{t.site.name}</div>
            <div className="text-xs text-[var(--text-faint)]">{t.site.coreClaim}</div>
          </div>
        </div>

        <div className="flex flex-col gap-2 text-sm text-[var(--text-dim)] sm:items-end">
          <a
            href={t.site.github}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 transition-colors hover:text-white"
          >
            <Github className="h-4 w-4" /> {t.footer.viewGithub}
          </a>
          <span className="inline-flex items-center gap-2 text-xs text-[var(--text-faint)]">
            <ShieldCheck className="h-3.5 w-3.5" /> {t.site.licenseDot} · {t.site.version}
          </span>
        </div>
      </div>
    </footer>
  );
}
