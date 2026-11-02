import { useEffect, useState } from "react";
import { BookOpen, PlayCircle, Rocket, Download } from "lucide-react";
import { useI18n } from "@/i18n";

const TABS = [
  { href: "#rules", key: "rules", icon: BookOpen },
  { href: "#demo", key: "demo", icon: PlayCircle },
  { href: "#start", key: "start", icon: Rocket },
  { href: "#install", key: "install", icon: Download },
] as const;

export function BottomNav() {
  const { t } = useI18n();
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
    TABS.forEach((tab) => {
      const el = document.getElementById(tab.href.slice(1));
      if (el) obs.observe(el);
    });
    return () => obs.disconnect();
  }, []);

  return (
    <nav aria-label={t.bottomNav.aria} className="bottom-nav">
      {TABS.map((tab) => {
        const Icon = tab.icon;
        const on = active === tab.href;
        return (
          <a
            key={tab.href}
            href={tab.href}
            aria-current={on ? "page" : undefined}
            className="bottom-nav__item"
          >
            <Icon />
            {t.bottomNav[tab.key]}
          </a>
        );
      })}
    </nav>
  );
}
