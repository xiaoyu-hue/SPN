import { motion } from "framer-motion";
import type { ReactNode } from "react";

// 滚动进入视口时的微交互：淡入 + 上移。prefers-reduced-motion 由 main.tsx 的
// <MotionConfig reducedMotion="user"> 统一接管，开启后这里直接跳到终态、不再播放动画。
export function Reveal({
  children,
  delay = 0,
  className,
}: {
  children: ReactNode;
  delay?: number;
  className?: string;
}) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.5, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  );
}
