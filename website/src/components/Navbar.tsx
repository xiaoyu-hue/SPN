import { useEffect, useState } from "react";
import { Github, BookOpen, Menu, X } from "lucide-react";
import { SITE } from "@/content";

const LINKS = [
  { href: "#pain", label: "痛点" },
  { href: "#rules", label: "核心规则" },
  { href: "#demo", label: "互动演示" },
  { href: "#start", label: "三步上手" },
  { href: "#skills", label: "技能包" },
  { href: "#install", label: "安装" },
];

export function Navbar() {
  const [open, setOpen] = useState(false);
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
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-brand to-sand text-sm font-bold text-ink">
            S
          </span>
          <span className="text-base font-semibold text-white">
            {SITE.name}
            <span className="ml-1.5 hidden text-xs font-normal text-[var(--text-faint)] sm:inline">
              {SITE.tagline}
            </span>
          </span>
        </a>

        <div className="hidden items-center gap-1 md:flex">
          {LINKS.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="rounded-lg px-3 py-2 text-sm text-[var(--text-dim)] transition-colors hover:text-white"
            >
              {l.label}
            </a>
          ))}
        </div>

        <div className="hidden items-center gap-2 md:flex">
          <a
            className="btn btn--ghost"
            href={SITE.github}
            target="_blank"
            rel="noreferrer"
          >
            <Github className="h-4 w-4" /> GitHub
          </a>
          <a
            className="btn btn--primary"
            href={`${SITE.github}#快速开始`}
            target="_blank"
            rel="noreferrer"
          >
            <BookOpen className="h-4 w-4" /> 快速开始
          </a>
        </div>

        <button
          className="btn btn--ghost px-2.5 py-2 md:hidden"
          onClick={() => setOpen((v) => !v)}
          aria-label="菜单"
        >
          {open ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
        </button>
      </nav>

      {open && (
        <div className="glass mx-auto mt-2 max-w-6xl rounded-2xl p-3 md:hidden">
          <div className="grid grid-cols-2 gap-1">
            {LINKS.map((l) => (
              <a
                key={l.href}
                href={l.href}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-2.5 text-sm text-[var(--text-dim)] transition-colors hover:bg-white/5 hover:text-white"
              >
                {l.label}
              </a>
            ))}
          </div>
          <div className="mt-2 flex gap-2">
            <a className="btn btn--ghost flex-1" href={SITE.github} target="_blank" rel="noreferrer">
              <Github className="h-4 w-4" /> GitHub
            </a>
            <a
              className="btn btn--primary flex-1"
              href={`${SITE.github}#快速开始`}
              target="_blank"
              rel="noreferrer"
            >
              <BookOpen className="h-4 w-4" /> 快速开始
            </a>
          </div>
        </div>
      )}
    </header>
  );
}
