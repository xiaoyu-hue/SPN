import { motion } from "framer-motion";
import { Github, ArrowRight, ShieldCheck } from "lucide-react";
import { Glass } from "@/components/Glass";
import { SITE } from "@/content";

export function Hero() {
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
            <ShieldCheck className="h-3.5 w-3.5" /> 开源 · {SITE.version} · 代码 MIT / 文档 CC BY 4.0
          </span>

          <h1 className="mt-7 font-display text-[clamp(2.4rem,6.5vw,4.5rem)] font-bold leading-[1.05] tracking-tight text-white">
            代码是 <span className="text-gradient">AI 写的</span>
            <br />
            判断是 <span className="text-accent">你做的</span>
          </h1>

          <p className="lead mx-auto text-center text-[1.05rem]">
            {SITE.intro}
          </p>

          <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <a className="btn btn--primary" href={SITE.github} target="_blank" rel="noreferrer">
              <Github className="h-4 w-4" /> 在 GitHub 查看
            </a>
            <a
              className="btn btn--ghost"
              href="#start"
            >
              三步上手 <ArrowRight className="h-4 w-4" />
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
              <span className="ml-2">与 AI 的协作现场</span>
            </div>
            <p className="mt-4 text-sm text-[var(--text-dim)]">
              <span className="text-[var(--text-faint)]">你：</span>帮我把这个项目部署上线。
            </p>
            <p className="mt-2 rounded-xl bg-ask/10 p-3 text-sm text-amber-100/90 ring-1 ring-ask/25">
              <span className="font-medium text-ask">AI：</span>这一步会改变线上且不可逆。我计划：①
              推送代码；② 触发部署。确认现在上线吗？
            </p>
            <p className="mt-3 text-xs text-[var(--text-faint)]">
              红线之上，AI 不替你拍板——这就是 SPN。
            </p>
          </Glass>
        </motion.div>
      </div>
    </section>
  );
}
