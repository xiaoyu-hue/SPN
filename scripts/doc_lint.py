#!/usr/bin/env python3
"""检查文档里有没有「写死、会随时间失真的数字」。

用法：
    python3 scripts/doc_lint.py

退出码：0 通过；1 发现疑似写死的数字。

为什么不用一两个 grep 凑合（历史版本的教训）：
    原先的 CI 用 grep 扫描，但存在两个问题，导致它长期输出「OK: 未发现写死数字」
    却什么都没拦住：
      1. 正则只覆盖几个特定中文量词，抓不到 `500MB`、`¥19.9`、`38 万个` 这类最常见写法；
      2. 「排除含 → 的行」是**整行豁免**——一行里只要有一个箭头，这一行的写死数字就全部放行，
         而教学句式天然爱用箭头，等于给规则挖了个洞。
    本文件改成：先剔除明确的豁免片段（教学示例、URL），再匹配。豁免对象是**片段**不是整行。

职责边界（很重要，别越界）：
    本检查只管「最常被直接拷走、必须保持干净」的文件：README / AGENTS / SKILL 及其英文镜像。
    references/ 下那些带核查日期的调研数据（安全事件样本量、平台免费额度等）属于「已登记的事实」，
    由 scripts/check_facts.py 单独管时效性——因为对它们的正确处理是「标注日期、定期复核」，
    而不是删掉精确值。
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPO = "xiaoyu-hue/SPN"

# 只查会被人直接拷走的文件。references/ 交给 check_facts.py 管。
LINT_FILES = [
    "README.md",
    "AGENTS.md",
    "SKILL.md",
    "docs/README.md",
    "docs/AGENTS.md",
    "docs/SKILL.md",
    "docs/SECURITY.md",
    "docs/CONTRIBUTING.md",
]

# 教学文档：整篇都是「别写死数字」的反面示例，一个活靶子。
EXCLUDE_FILES = {"references/03", "docs/references/03"}

# ------------------------------------------------------------------ 模式

PATTERNS: list = [
    (r"\b\d{3,}\s*(?:项测试|个模块|条测试|个文件|测试|模块|工具|书|人|项目|应用|网站|插件)\b", "数量"),
    (r"\b\d+(?:\.\d+)?\s*(?:MB|GB|KB|TB)\b", "容量"),
    (r"[¥$€￥]\s?\d+(?:\.\d+)?", "金额"),
    (r"\b\d+(?:\.\d+)?\s*万\b", "万级数量"),
    (r"\b\d{1,3}(?:,\d{3})+\b", "带千分位的数量"),
    (r"\bv\d+\.\d+\.\d+\b", "版本号"),
]

URL_RE = re.compile(r"https?://\S+")
CODE_RE = re.compile(r"`[^`\n]*`")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]\n]*\]\([^)\n]*\)")
BADGE_IMG_RE = re.compile(r"!\[[^\]\n]*\]\([^)\n]*\)")
# 豁免判据一：`旧写法` → `新写法` 的完整对照。要求**两端都被包裹**才豁免，
# 避免出现「`573 项测试` → 详见报表」这种半截结构也能逃过检查。
TEACHING_PAIR_RE = re.compile(
    r"[`\"'“][^`\"'\n”]*[`\"'”]\s*(?:→|->)\s*[`\"'“][^`\"'\n”]*[`\"'”]"
)
# 豁免判据二：同行出现教学提示词（"而不是…"），此时被引号包裹的数字视为示例。
# 两个条件缺一不可：只加个箭头已不足以放行——这正是旧版本被绕过的漏洞所在。
TEACHING_HINT_RE = re.compile(r"而不是|用相对描述|应写为|改成|不要写死|别写死|示例")
QUOTED_NUMBER_RE = re.compile(r"[`\"'“][^`\"'\n”]*\d[^`\"'\n”]*[`\"'”]")
# 「看起来制造oulder动ps颈"? 统一在这里维护白名单
ALLOWED_RE = re.compile(
    r"影响超过\s*\d+\s*个文件"
)


def strip_exempt(text: str) -> str:
    """按**片段**剔除豁免内容，剩下的才是真正需要检查的文本。"""
    text = BADGE_IMG_RE.sub(" ", text)      # 徽章里必然有版本号
    text = MARKDOWN_LINK_RE.sub(" ", text)  # 链接本身可能含版本/日期
    text = URL_RE.sub(" ", text)            # 裸 URL，同上
    text = ALLOWED_RE.sub(" ", text)
    text = TEACHING_PAIR_RE.sub(" ", text)  # `573 项测试` → `数百项测试` 这类示范
    if TEACHING_HINT_RE.search(text):
        text = QUOTED_NUMBER_RE.sub(" ", text)  # 「"573 项测试"而不是..." 这类对照示范
    return text


def scan(path: str) -> list:
    problems = []
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    in_fence = False
    for lineno, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue  # 代码块里的示例命令不算文档正文

        probe = strip_exempt(line)
        for pattern, kind in PATTERNS:
            m = re.search(pattern, probe)
            if m:
                rel = os.path.relpath(path, ROOT) if os.path.isabs(path) else path
                problems.append(f"{rel}:{lineno} [{kind}] {m.group(0)!r} — {line.strip()[:70]}")
                break
    return problems


def targets(diff_files: list | None = None) -> list:
    """待检查文件列表。传 diff_files 时只检查其中属于 LINT_FILES 的部分（发版时用）。"""
    wanted = LINT_FILES
    if diff_files is not None:
        wanted = [f for f in LINT_FILES if f in diff_files]
    return [
        rel
        for rel in wanted
        if os.path.isfile(os.path.join(ROOT, rel))
        and not any(x in rel for x in EXCLUDE_FILES)
    ]


def problems_of(diff_files: list | None = None) -> list:
    """返回问题列表（相对路径:行号 ...），CI 与 release.py 共用这一个入口。"""
    problems = []
    for rel in targets(diff_files):
        problems.extend(scan(os.path.join(ROOT, rel)))
    return problems


def main() -> int:
    problems = problems_of()

    if problems:
        print("发现疑似写死的数字（会随迭代失真）：\n")
        for p in problems:
            print(f"  ::error file={p.split(':')[0]}:: {p}")
        print(
            "\n处理方式，按推荐顺序：\n"
            "  1. 改成相对描述：'573 项测试' → '测试积累到数百项'\n"
            "  2. 搬到 FACTS.md 并标注核查日期（适合保留精确值更有说服力的调研数据）\n"
            "  3. 明确标注 '截至 vX.Y.Z' 或具体日期\n"
        )
        return 1

    print(f"OK: {len(LINT_FILES)} 个入口文件未发现写死数字")
    return 0


if __name__ == "__main__":
    sys.exit(main())
