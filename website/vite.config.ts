import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

// 相对 base：本地预览（/）与 GitHub Pages 子路径（/SPN/）下都能正确加载资源
export default defineConfig({
  base: "./",
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
