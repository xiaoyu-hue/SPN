import { useEffect, useState } from "react";
import { ArrowUp } from "lucide-react";
import { useI18n } from "@/i18n";

export function BackToTop() {
  const { t } = useI18n();
  const [show, setShow] = useState(false);

  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > 600);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <button
      type="button"
      className={`back-to-top${show ? " back-to-top--show" : ""}`}
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
      aria-label={t.backToTop}
      tabIndex={show ? 0 : -1}
    >
      <ArrowUp className="h-5 w-5" />
    </button>
  );
}
