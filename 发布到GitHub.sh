#!/bin/bash
# 把 SPN 规则包发布到 GitHub 的脚本
# 用法（先改下面三个变量，或用环境变量覆盖）：
#   GITHUB_USER=xiaoyu-hue
#   REPO_NAME=SPN
#   VISIBILITY=private      # private 或 public
#
# ⚠️ 安全：本脚本不读取、不内置任何 token。请用已登录的 gh（gh auth login）来推送，
#    或在下方 git 命令前用环境变量注入；切勿把 token 写进本文件或提交到仓库。
#
# 前置条件：
#   1. 装好 git
#   2. 已配置 GitHub 凭据（推荐 gh auth login，或 SSH key）
#   3. 在 GitHub 网页端先创建一个空仓库（不要勾选 README / .gitignore / LICENSE）
#
# 跑之前先在 GitHub 网页建好空仓库，再回来执行本脚本。

set -e

GITHUB_USER="${GITHUB_USER:-xiaoyu-hue}"
REPO_NAME="${REPO_NAME:-SPN}"
VISIBILITY="${VISIBILITY:-private}"

echo "=== 目标仓库：$GITHUB_USER/$REPO_NAME ($VISIBILITY) ==="
read -p "确认无误？[y/N] " confirm
[ "$confirm" != "y" ] && echo "已取消" && exit 1

# 1. 初始化
git init -b main
git add .
git commit -m "feat: SPN · 零基础 × AI Agent 协作规则包 v1.0.0

从作者多个真实上线项目提炼的 AI 协作规则：
- 判断归属：代码是 AI 写的，判断是你做的
- 三档授权：照做就行 / 先问再做 / 永远不做
- 上线前安全自查（RLS、密钥、越权测试）+ 零基础免代码路径
- 文档与局限披露模板
- 23 条可直接复制的提示词
- 分层许可证：代码 MIT / 文档 CC BY 4.0"

# 2. 关联远程并推送
if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
fi
git push -u origin main

# 3. 打 tag
git tag -a v1.0.0 -m "v1.0.0: 首个正式版本"
git push origin v1.0.0

echo ""
echo "=== 推送完成 ==="
echo "接下来在网页端创建 Release："
echo "  https://github.com/$GITHUB_USER/$REPO_NAME/releases/new?tag=v1.0.0"
echo "标题填：v1.0.0 — 代码是 AI 写的，判断是你做的"
echo "正文直接复制 RELEASE_NOTES_v1.0.0.md 的内容"
echo ""
echo "另外建议开启（免费）："
echo "  Settings → Code security → 勾选 Dependency alerts / Secret scanning"
echo ""
echo "当前为 $VISIBILITY。完善后再在网页端改为 public 即可。"
