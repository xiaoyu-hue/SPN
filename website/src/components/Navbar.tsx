import { useEffect, useState } from "react";
import { Github, BookOpen } from "lucide-react";
import { Logo } from "@/components/Logo";
import { LangToggle } from "@/components/LangToggle";
import { useI18n } from "@/i18n";

export function Navbar() {
  const { t } = useI18n();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header className="sticky top-0 z-50 px-3 pt-3 sm:px-5 sm:pt-4">
      <nav
        className="glass mx-auto flex max-w-6xl items-center justify-between rounded-2xl px-4 py-2.5 transition-shadow"
        style={{
          background: scrolled ? "rgba(10,12,20,0.72)" : "rgba(255,255,255,0.04)",
          boxShadow: scrolled ? "0 14px 40px -18px rgba(0,0,0,0.7)" : undefined,
        }}
      >
        <a href="#top" className="flex items-center gap-2.5">
          <Logo size={32} className="shrink-0" />
          <span className="text-base font-semibold text-white">
            {t.site.name}
            <span className="ml-1.5 hidden text-xs font-normal text-[var(--text-faint)] sm:inline">
              {t.site.tagline}
            </span>
          </span>
        </a>

        <div className="hidden items-center gap-1 lg:flex">
          {t.nav.links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="rounded-lg px-3 py-2 text-sm text-[var(--text-dim)] transition-colors hover:text-white"
            >
              {l.label}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <LangToggle />
          <a
            className="btn btn--ghost px-2.5 py-2"
            href={t.site.github}
            target="_blank"
            rel="noreferrer"
            aria-label={t.nav.githubAria}
          >
            <Github className="h-4 w-4" />
            <span className="hidden sm:inline">GitHub</span>
          </a>
          <a
            className="btn btn--primary hidden whitespace-nowrap sm:inline-flex"
            href={`${t.site.github}${t.nav.quickStartHref}`}
            target="_blank"
            rel="noreferrer"
          >
            <BookOpen className="h-4 w-4" /> {t.nav.quickStart}
          </a>
        </div>
      </nav>
    </header>
  );
}
