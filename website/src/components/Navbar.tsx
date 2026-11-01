import { useEffect, useState } from "react";
import { Github, BookOpen } from "lucide-react";
import { SITE } from "@/content";
import { Logo } from "@/components/Logo";

const LINKS = [
  { href: "#pain", label: "痛点" },
  { href: "#rules", label: "核心规则" },
  { href: "#demo", label: "互动演示" },
  { href: "#start", label: "三步上手" },
  { href: "#skills", label: "技能包" },
  { href: "#install", label: "安装" },
];

export function Navbar() {
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

        <div className="flex items-center gap-2">
          <a
            className="btn btn--ghost px-2.5 py-2"
            href={SITE.github}
            target="_blank"
            rel="noreferrer"
            aria-label="在 GitHub 查看"
          >
            <Github className="h-4 w-4" />
            <span className="hidden sm:inline">GitHub</span>
          </a>
          <a
            className="btn btn--primary hidden sm:inline-flex"
            href={`${SITE.github}#快速开始`}
            target="_blank"
            rel="noreferrer"
          >
            <BookOpen className="h-4 w-4" /> 快速开始
          </a>
        </div>
      </nav>
    </header>
  );
}
