import { useEffect, useState } from "react";
import { BookOpen, PlayCircle, Rocket, Download } from "lucide-react";

const TABS = [
  { href: "#rules", label: "规则", icon: BookOpen },
  { href: "#demo", label: "演示", icon: PlayCircle },
  { href: "#start", label: "上手", icon: Rocket },
  { href: "#install", label: "安装", icon: Download },
];

export function BottomNav() {
  const [active, setActive] = useState<string>("#rules");

  useEffect(() => {
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) setActive("#" + (e.target as HTMLElement).id);
        });
      },
      { rootMargin: "-45% 0px -45% 0px" }
    );
    TABS.forEach((t) => {
      const el = document.getElementById(t.href.slice(1));
      if (el) obs.observe(el);
    });
    return () => obs.disconnect();
  }, []);

  return (
    <nav aria-label="底部导航" className="bottom-nav">
      {TABS.map((t) => {
        const Icon = t.icon;
        const on = active === t.href;
        return (
          <a
            key={t.href}
            href={t.href}
            aria-current={on ? "page" : undefined}
            className="bottom-nav__item"
          >
            <Icon />
            {t.label}
          </a>
        );
      })}
    </nav>
  );
}
