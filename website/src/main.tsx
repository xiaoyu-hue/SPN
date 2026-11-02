import React from "react";
import ReactDOM from "react-dom/client";
import { MotionConfig } from "framer-motion";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    {/* reducedMotion="user"：尊重系统“减少动效”设置，关闭所有 framer 渐入/位移动画，
        避免前庭敏感用户在无意中被迫观看滚动动画（仅 CSS 媒体查询管不到 JS 动画）。 */}
    <MotionConfig reducedMotion="user">
      <App />
    </MotionConfig>
  </React.StrictMode>
);
