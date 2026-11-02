#!/usr/bin/env python3
"""SPN 规则安装器。

把 AGENTS.md（或精简版 AGENTS.minimal.md）放到当前 AI 编程工具「强制读取」的位置，
并验证它确实就位。

SPN 最大的坑不是「规则写得好不好」，而是「AI 根本没读规则」。
不同工具加载 AGENTS.md 的行为不一致：有的默认读，有的（如 Claude Code）默认不读，
有的只读自己专属的配置文件。本脚本把规则放到对应工具「一定会读」的位置，
直接解决「加载确定性」（L1）。

使用：
  python3 scripts/install.py                自动探测并安装到当前目录
  python3 scripts/install.py --minimal      用精简版基线 AGENTS.minimal.md
  python3 scripts/install.py --tool claude  指定工具（跳过探测）
  python3 scripts/install.py --target DIR    安装到指定项目目录
  python3 scripts/install.py --dry-run       只报告会做什么，不写任何文件

支持的工具与放置位置：
  claude    项目根 CLAUDE.md 追加 `@AGENTS.md`（Claude Code 的加载入口）
  codebuddy 复制 skills/spn 到 ~/.codebuddy/skills/spn（或项目 .codebuddy/skills）
  cursor    复制 AGENTS.md 到项目根（Cursor 原生读取）+ 写 .cursor/rules 入口
  gemini    复制 AGENTS.md 到项目根 GEMINI.md
  copilot   复制 AGENTS.md 到 .github/copilot-instructions.md
  generic   复制 AGENTS.md 到项目根（兜底）
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FULL = REPO_ROOT / "AGENTS.md"
MINIMAL = REPO_ROOT / "AGENTS.minimal.md"

# 各工具的探测标记：在 target 目录下找这些文件/目录来判断用户用哪个工具
TOOL_MARKERS = {
    "claude": ["CLAUDE.md", ".claude"],
    "codebuddy": [".codebuddy", ".workbuddy"],
    "cursor": [".cursor", ".cursorrules"],
    "gemini": ["GEMINI.md"],
    "copilot": [".github"],
}


def detect_tool(target: Path) -> str | None:
    for tool, markers in TOOL_MARKERS.items():
        for m in markers:
            if (target / m).exists():
                return tool
    return None


def install_claude(target: Path, src_file: Path, dry: bool) -> bool:
    claude = target / "CLAUDE.md"
    directive = f"@{(src_file.name)}\n"
    existing = claude.read_text(encoding="utf-8") if claude.exists() else ""
    if directive.strip() in existing:
        print(f"  ✓ {claude} 已包含加载指令，跳过")
        return True
    if dry:
        print(f"  [dry-run] 会在 {claude} 追加: {directive.strip()}")
        return True
    with claude.open("a", encoding="utf-8") as f:
        f.write("\n" + directive)
    print(f"  ✓ 已在 {claude} 追加 `@{src_file.name}` 加载指令")
    return True


def install_generic(target: Path, src_file: Path, dry: bool) -> bool:
    dst = target / src_file.name
    if dry:
        print(f"  [dry-run] 会复制 {src_file.name} -> {dst}")
        return True
    shutil.copy2(src_file, dst)
    print(f"  ✓ 已复制 {src_file.name} -> {dst}")
    return True


def install_cursor(target: Path, src_file: Path, dry: bool) -> bool:
    install_generic(target, src_file, dry)
    rules_dir = target / ".cursor" / "rules"
    rules_file = rules_dir / "spn-agent-rules.md"
    content = (
        f"# SPN 协作规则\n\n"
        f"本规则来自 SPN（https://github.com/xiaoyu-hue/SPN）。\n"
        f"完整规则见项目根目录的 `{src_file.name}`，AI 开工前应加载并遵守。\n"
    )
    if dry:
        print(f"  [dry-run] 会写 {rules_file}")
        return True
    rules_dir.mkdir(parents=True, exist_ok=True)
    rules_file.write_text(content, encoding="utf-8")
    print(f"  ✓ 已写 {rules_file}（指向根规则）")
    return True


def install_codebuddy(target: Path, src_file: Path, dry: bool) -> bool:
    skills_src = REPO_ROOT / "skills" / "spn"
    if not skills_src.exists():
        print("  ! skills/spn 不存在，回退为复制 AGENTS.md 到根目录")
        return install_generic(target, src_file, dry)
    dest = Path.home() / ".codebuddy" / "skills" / "spn"
    if dry:
        print(f"  [dry-run] 会复制技能包 {skills_src} -> {dest}")
        return True
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(skills_src, dest)
    print(f"  ✓ 已安装技能包到 {dest}")
    return True


def install_gemini(target: Path, src_file: Path, dry: bool) -> bool:
    dst = target / "GEMINI.md"
    if dry:
        print(f"  [dry-run] 会复制 {src_file.name} -> {dst}")
        return True
    shutil.copy2(src_file, dst)
    print(f"  ✓ 已复制 {src_file.name} -> GEMINI.md")
    return True


def install_copilot(target: Path, src_file: Path, dry: bool) -> bool:
    dst = target / ".github" / "copilot-instructions.md"
    if dry:
        print(f"  [dry-run] 会复制 {src_file.name} -> {dst}")
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_file, dst)
    print(f"  ✓ 已复制 {src_file.name} -> .github/copilot-instructions.md")
    return True


INSTALLERS = {
    "claude": install_claude,
    "codebuddy": install_codebuddy,
    "cursor": install_cursor,
    "gemini": install_gemini,
    "copilot": install_copilot,
    "generic": install_generic,
}


def main() -> int:
    ap = argparse.ArgumentParser(description="SPN 规则安装器")
    ap.add_argument("--minimal", action="store_true", help="用精简版 AGENTS.minimal.md")
    ap.add_argument("--tool", choices=list(INSTALLERS.keys()), help="指定工具（默认自动探测）")
    ap.add_argument("--target", default=".", help="目标项目目录（默认当前目录）")
    ap.add_argument("--dry-run", action="store_true", help="只报告，不写文件")
    args = ap.parse_args()

    src = MINIMAL if args.minimal else FULL
    if not src.exists():
        print(f"! 找不到 {src}", file=sys.stderr)
        return 2

    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"! 目标目录不存在: {target}", file=sys.stderr)
        return 2

    tool = args.tool or detect_tool(target) or "generic"
    print(f"源规则:   {src.name}")
    print(f"目标目录: {target}")
    print(f"检测工具: {tool}" + ("（自动探测）" if not args.tool else "（指定）"))
    print("---")

    ok = INSTALLERS[tool](target, src, args.dry_run)
    if not ok:
        return 1
    print("---")
    if args.dry_run:
        print("dry-run 完成，未改动任何文件。")
    else:
        print("安装完成。验证：新开一个会话，让 AI 复述「开工前三句话」；能复述即加载成功。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
