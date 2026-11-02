#!/usr/bin/env python3
"""SPN 合规检查：扫描 git diff 中的「永远不做」红线模式。

SPN 的 L3（自动化兜底）：规则写得再好，AI 也可能不守。本脚本在 CI / 提交前
自动抓「硬违规」——密钥泄露、RLS 形同虚设、SQL 拼接、危险删除等，
把「永远不做」从一句口号变成一道可被机器拦下的关卡。

扫描范围只覆盖「看起来像应用代码」的文件（.py/.js/.ts/.sql/.env 等），
并主动跳过 SPN 自身的文档与工具目录（docs/ references/ scripts/ .github/
website/ tests/ 等）——这些地方出现的红线词是教学示例或工具自身代码，
不应被误报。

用法：
  python3 scripts/spn_compliance.py                扫当前未提交改动
  python3 scripts/spn_compliance.py --base main   扫 main..HEAD 的差异
  python3 scripts/spn_compliance.py file.py       只扫指定文件

命中红线：打印问题并退出非零（CI 变红）。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# 红线模式：仅在应用代码里查，避免误伤 SPN 自身的规则文档
RED_LINE_PATTERNS = [
    ("密钥/令牌泄露", __import__("re").compile(
        r"(service_role|sk_live|sk_test|ghp_[A-Za-z0-9]{20,}|glpat-[\w-]{20,}|"
        r"AIza[0-9A-Za-z_\-]{35}|AKIA[0-9A-Z]{16})")),
    ("RLS 形同虚设 (USING true)", __import__("re").compile(r"using\s*\(\s*true\s*\)", __import__("re").IGNORECASE)),
    ("疑似 SQL 拼接", __import__("re").compile(
        r"(select|insert|update|delete|from|where).*[\"'`].*\+.*", __import__("re").IGNORECASE)),
    ("危险递归删除", __import__("re").compile(r"rm\s+-rf\s+(/|\.\./|~|\*)", __import__("re").IGNORECASE)),
]

# 跳过这些目录（SPN 自身文档/工具/构建产物，里面的红线词是教学或工具自身）
SKIP_DIRS = {
    "docs", "references", "scripts", ".github", "website", "tests",
    ".codebuddy", ".workbuddy", "node_modules", "dist", "build", ".git",
}

APP_EXT = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".sql", ".rb", ".go", ".java",
    ".php", ".env", ".json", ".yaml", ".yml", ".sh",
}


def get_diff_files(base: str | None) -> list[Path]:
    if base:
        cmd = ["git", "diff", "--name-only", f"{base}...HEAD"]
    else:
        cmd = ["git", "diff", "--name-only", "--cached"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        out = subprocess.run(["git", "diff", "--name-only"],
                             capture_output=True, text=True).stdout
    return [Path(p) for p in out.splitlines() if p.strip()]


def should_scan(path: Path) -> bool:
    if path.suffix.lower() == ".md":
        return False  # 文档一律不扫
    if path.suffix.lower() not in APP_EXT:
        return False
    if set(path.parts) & SKIP_DIRS:
        return False
    return True


def scan_line(line: str) -> list[str]:
    import re
    hits: list[str] = []
    for name, pat in RED_LINE_PATTERNS:
        if pat.search(line):
            hits.append(name)
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="SPN 合规检查")
    ap.add_argument("files", nargs="*", help="只扫这些文件（默认扫 git diff）")
    ap.add_argument("--base", help="与哪个分支比较（如 main）")
    args = ap.parse_args()

    files = [Path(f) for f in args.files] if args.files else get_diff_files(args.base)

    issues: list[tuple[Path, int, str, str]] = []
    for f in files:
        if not should_scan(f):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for name in scan_line(line):
                issues.append((f, i, name, line.strip()[:120]))

    if not issues:
        print("✓ SPN 合规检查通过：未发现红线模式")
        return 0
    print(f"✗ 发现 {len(issues)} 处疑似违反 SPN「永远不做」的红线：\n")
    for f, i, name, snippet in issues:
        print(f"  [{name}] {f}:{i}")
        print(f"      {snippet}\n")
    print("请复核：这些可能是真实违规，也可能是误报（依赖或示例里的关键词）。")
    print("『永远不做』完整清单见 AGENTS.md。确认确属误报可加 --allow 跳过（不推荐）。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
