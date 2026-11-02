import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { zh, en, type Content, type Lang } from "@/content";

type I18n = { lang: Lang; setLang: (l: Lang) => void; t: Content };

const LangContext = createContext<I18n | null>(null);
const STORAGE_KEY = "spn-lang";

function initialLang(): Lang {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "zh" || saved === "en") return saved;
  } catch {
    /* localStorage 不可用时走浏览器语言 */
  }
  return typeof navigator !== "undefined" &&
    navigator.language?.toLowerCase().startsWith("zh")
    ? "zh"
    : "en";
}

export function LangProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(initialLang);
  const t = lang === "zh" ? zh : en;

  // 切换语言时同步 <html lang>、标题与 meta 描述
  useEffect(() => {
    document.documentElement.lang = t.meta.htmlLang;
    document.title = t.meta.title;
    document
      .querySelector('meta[name="description"]')
      ?.setAttribute("content", t.meta.description);
  }, [t]);

  const value = useMemo<I18n>(
    () => ({
      lang,
      t,
      setLang: (l: Lang) => {
        setLangState(l);
        try {
          localStorage.setItem(STORAGE_KEY, l);
        } catch {
          /* 忽略存储失败 */
        }
      },
    }),
    [lang, t]
  );

  return <LangContext.Provider value={value}>{children}</LangContext.Provider>;
}

export function useI18n(): I18n {
  const ctx = useContext(LangContext);
  if (!ctx) throw new Error("useI18n 必须在 LangProvider 内使用");
  return ctx;
}
