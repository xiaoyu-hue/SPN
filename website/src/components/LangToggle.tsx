import { useI18n } from "@/i18n";

/** 中/EN 切换按钮：点击切换全站语言并记住选择（localStorage）。 */
export function LangToggle() {
  const { lang, setLang, t } = useI18n();
  return (
    <button
      type="button"
      onClick={() => setLang(lang === "zh" ? "en" : "zh")}
      className="btn btn--ghost px-2.5 py-2 font-mono text-xs tracking-wide"
      aria-label={t.langToggle.aria}
      title={t.langToggle.aria}
    >
      {t.langToggle.show}
    </button>
  );
}
