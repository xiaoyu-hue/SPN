/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // 深墨基底 + 克制点缀（非霓虹紫蓝）；品牌色用偏冷的雾蓝，单一暖砂色作高级感强调
        ink: "#06070d",
        surface: "#0b0d16",
        line: "rgba(255,255,255,0.10)",
        brand: {
          DEFAULT: "#8b9bff", // 雾蓝（克制，非饱和靛）
          soft: "#aab4ff",
        },
        sand: "#e7c39a", // 暖砂强调色（编辑级质感，避开 AI 味的蓝紫）
        // 三档授权语义色（与仓库一致，略降饱和以融入暗色）
        allow: "#5fd38b",
        ask: "#f2c14e",
        forbid: "#f0888a",
      },
      fontFamily: {
        sans: ["Noto Sans SC", "PingFang SC", "Microsoft YaHei", "system-ui", "sans-serif"],
        display: ["Space Grotesk", "Noto Sans SC", "system-ui", "sans-serif"],
        serif: ["Instrument Serif", "Noto Serif SC", "serif"],
        mono: ["JetBrains Mono", "SFMono-Regular", "Menlo", "Consolas", "monospace"],
      },
      borderRadius: {
        xl: "0.9rem",
        "2xl": "1.35rem",
        "3xl": "1.9rem",
      },
      boxShadow: {
        glass: "0 18px 50px -20px rgba(0,0,0,0.65)",
      },
      keyframes: {
        shimmer: {
          "0%": { backgroundPosition: "0% 50%" },
          "100%": { backgroundPosition: "200% 50%" },
        },
        float: {
          "0%,100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        beam: {
          "0%": { transform: "translateX(-100%)" },
          "100%": { transform: "translateX(100%)" },
        },
        drift: {
          "0%": { transform: "translate3d(0,0,0) scale(1)" },
          "100%": { transform: "translate3d(2%, -2%, 0) scale(1.06)" },
        },
      },
      animation: {
        float: "float 7s ease-in-out infinite",
        beam: "beam 5s linear infinite",
        drift: "drift 26s ease-in-out infinite alternate",
      },
    },
  },
  plugins: [],
};
