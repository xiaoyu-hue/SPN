import { motion } from "framer-motion";
import { Github, ArrowRight, ShieldCheck } from "lucide-react";
import { Glass } from "@/components/Glass";
import { useI18n } from "@/i18n";

export function Hero() {
  const { t } = useI18n();
  return (
    <section id="top" className="relative">
      <div className="container-page pb-16 pt-20 sm:pb-24 sm:pt-28">
        <motion.div
          initial={{ opacity: 0, y: 22 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
          className="mx-auto max-w-3xl text-center"
        >
          <span className="eyebrow">
            <ShieldCheck className="h-3.5 w-3.5" /> {t.hero.eyebrowOpen} · {t.site.version} ·{" "}
            {t.site.licenseSlash}
          </span>

          <h1 className="mt-7 font-display text-[clamp(2.4rem,6.5vw,4.5rem)] font-bold leading-[1.05] tracking-tight text-white">
            {t.hero.titleLead1}
            <span className="text-gradient">{t.hero.titleHi1}</span>
            <br />
            {t.hero.titleLead2}
            <span className="text-accent">{t.hero.titleHi2}</span>
          </h1>

          <p className="lead mx-auto text-center text-[1.05rem]">
            {t.site.intro}
          </p>

          <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <a className="btn btn--primary" href={t.site.github} target="_blank" rel="noreferrer">
              <Github className="h-4 w-4" /> {t.hero.primaryBtn}
            </a>
            <a
              className="btn btn--ghost"
              href="#start"
            >
              {t.hero.ghostBtn} <ArrowRight className="h-4 w-4" />
            </a>
          </div>
        </motion.div>

        {/* 漂浮对话卡：展示 AI 在红线前先问（微交互钩子） */}
        <motion.div
          initial={{ opacity: 0, y: 34 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.28, ease: [0.22, 1, 0.36, 1] }}
          className="mx-auto mt-16 max-w-xl"
        >
          <Glass refract sheen className="animate-float p-5 shadow-glass">
            <div className="flex items-center gap-2 text-xs text-[var(--text-faint)]">
              <span className="h-2.5 w-2.5 rounded-full bg-forbid/70" />
              <span className="h-2.5 w-2.5 rounded-full bg-ask/70" />
              <span className="h-2.5 w-2.5 rounded-full bg-allow/70" />
              <span className="ml-2">{t.hero.chatTitle}</span>
            </div>
            <p className="mt-4 text-sm text-[var(--text-dim)]">
              <span className="text-[var(--text-faint)]">{t.hero.chatYou}</span>
              {t.hero.chatUser}
            </p>
            <p className="mt-2 rounded-xl bg-ask/10 p-3 text-sm text-amber-100/90 ring-1 ring-ask/25">
              <span className="font-medium text-ask">{t.hero.chatAi}</span>
              {t.hero.chatAiText}
            </p>
            <p className="mt-3 text-xs text-[var(--text-faint)]">{t.hero.chatNote}</p>
          </Glass>
        </motion.div>
      </div>
    </section>
  );
}
