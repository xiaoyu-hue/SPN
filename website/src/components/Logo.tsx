import { useId } from "react";

/**
 * SPN 标志：玻璃边界 + 渐变描边 S + 一颗已"析出"沉淀的小液滴。
 * 概念：在 AI 给出的众多选项里，你的判断像结晶一样沉淀、成形（自我析出）。
 */
export function Logo({ size = 32, className }: { size?: number; className?: string }) {
  const raw = useId();
  const u = raw.replace(/[:]/g, "");
  const sg = `lg-sg-${u}`;
  const bord = `lg-bord-${u}`;
  const drop = `lg-drop-${u}`;
  const glow = `lg-glow-${u}`;

  return (
    <svg
      viewBox="0 0 32 32"
      width={size}
      height={size}
      className={className}
      role="img"
      aria-label="SPN"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id={sg} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#9aa6ff" />
          <stop offset="1" stopColor="#e7c39a" />
        </linearGradient>
        <linearGradient id={bord} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#9aa6ff" stopOpacity="0.7" />
          <stop offset="1" stopColor="#e7c39a" stopOpacity="0.45" />
        </linearGradient>
        <radialGradient id={drop} cx="0.5" cy="0.35" r="0.7">
          <stop offset="0" stopColor="#c2cbff" />
          <stop offset="1" stopColor="#8b9bff" />
        </radialGradient>
        <filter id={glow} x="-60%" y="-60%" width="220%" height="220%">
          <feGaussianBlur stdDeviation="1.1" result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* 玻璃边界（你定边界的主张） */}
      <rect
        x="1.5"
        y="1.5"
        width="29"
        height="29"
        rx="8"
        fill="#06070d"
        stroke={`url(#${bord})`}
        strokeWidth="1.4"
      />
      {/* 顶部高光，玻璃体积感 */}
      <path
        d="M5.5 4.6 Q16 2.7 26.5 4.6"
        fill="none"
        stroke="#ffffff"
        strokeOpacity="0.22"
        strokeWidth="1"
        strokeLinecap="round"
      />
      {/* S：渐变描边 */}
      <path
        d="M21.4 10.6 C21.4 7.6 10.6 7.6 10.6 12 C10.6 15.3 21.4 15.6 21.4 19.8 C21.4 24.2 10.6 24 10.6 21"
        fill="none"
        stroke={`url(#${sg})`}
        strokeWidth="3"
        strokeLinecap="round"
      />
      {/* 已析出沉淀的小液滴 */}
      <circle cx="16" cy="25.4" r="1.9" fill={`url(#${drop})`} filter={`url(#${glow})`} />
    </svg>
  );
}
