#!/usr/bin/env python3
"""检查仓库内 Markdown 的相对链接与锚点是否有效（纯本地，不联网）。

用法：
    python3 scripts/check_links.py            # 检查整个仓库
    python3 scripts/check_links.py --quiet    # 只输出结论

退出码：0 全部有效；1 存在问题。
"""

from __future__ import annotations

import os
import re
import sys
from urllib.parse import unquote

# 仓库根目录 = 本文件的上一级
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "node_modules", ".github"}

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def slugify(text: str) -> str:
    """按 GitHub 规则生成标题锚点：小写、去标点、空格转连字符。"""
    text = text.strip().lower()
    text = re.sub(r"[`*_~]", "", text)
    kept = []
    for ch in text:
        if ch.isalnum() or ch in (" ", "-", "_"):
            kept.append(ch)
        elif ch.isspace():
            kept.append(" ")
    return "".join(kept).replace(" ", "-")


def headings_of(path: str) -> set:
    anchors = set()
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
                if m:
                    anchors.add(slugify(m.group(2)))
    except OSError:
        pass
    return anchors


def check(verbose: bool = True):
    """返回 (md 文件数, 检查的链接数, 问题列表)。"""
    problems = []
    checked = 0
    md_files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".md"):
                md_files.append(os.path.join(dirpath, fn))

    anchor_cache: dict = {}
    for path in sorted(md_files):
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        in_fence = False
        for lineno, line in enumerate(lines, 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for m in LINK_RE.finditer(INLINE_CODE_RE.sub("", line)):
                target = m.group(2)
                if target.startswith(("http://", "https://", "mailto:", "//", "#!")):
                    continue
                checked += 1
                if target.startswith("#"):
                    anchor = unquote(target[1:])
                    if anchor and anchor not in headings_of(path):
                        problems.append(f"锚点缺失 {rel}:{lineno} -> {target}")
                    continue
                file_part, _, anchor = target.partition("#")
                resolved = os.path.normpath(
                    os.path.join(os.path.dirname(path), unquote(file_part))
                )
                if not os.path.exists(resolved):
                    problems.append(f"文件不存在 {rel}:{lineno} -> {target}")
                    continue
                if anchor and resolved.endswith(".md"):
                    if resolved not in anchor_cache:
                        anchor_cache[resolved] = headings_of(resolved)
                    if anchor not in anchor_cache[resolved]:
                        problems.append(f"跨文件锚点缺失 {rel}:{lineno} -> {target}")

    if verbose:
        print(f"扫描 {len(md_files)} 个 Markdown 文件，检查 {checked} 条相对链接")
        for p in problems:
            print("  " + p)
        if not problems:
            print("OK：全部相对链接与锚点有效")
    return len(md_files), checked, problems


def main() -> int:
    quiet = "--quiet" in sys.argv
    _, _, problems = check(verbose=not quiet)
    if problems:
        print(f"发现 {len(problems)} 个链接问题")
        return 1
    if quiet:
        print("OK：链接与锚点全部有效")
    return 0


if __name__ == "__main__":
    sys.exit(main())
