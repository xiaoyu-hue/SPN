#!/usr/bin/env python3
"""提醒：FACTS.md 里登记的事实该复核了。

用法：
    python3 scripts/check_facts.py                 # 超过复核周期就报警（退出码 0，仅提醒）
    python3 scripts/check_facts.py --strict        # 过期则退出码 1（想硬拦时用）
    python3 scripts/check_facts.py --refresh-stars # 用 gh api 实测 references/06 的 star/许可证

设计取舍（为什么不做成 CI 硬门禁）：
    过期提醒的本质是「该去看一眼了」，不是「这次提交错了」。
    硬拦会导致：想修个错别字的人被迫先去核对平台定价页，最后只能把整个检查关掉——
    一个总被关掉的检查，比一个总是提醒的检查更没用。
    所以默认退出码为 0，只在命令行终端输出醒目的过期清单。
"""

from __future__ import annotations

import datetime
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = os.path.join(ROOT, "FACTS.md")
DEFAULT_PERIOD = 90

TABLE_ROW_RE = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$")
DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
REPO_ROW_RE = re.compile(r"\[([^\]/]+/[^\]]+)\]\(https://github\.com/[^\)\s]+\)")


def parse_rows() -> list:
    """解析 FACTS.md 的登记表，返回 [(事实, 数值, 核查日期, 来源, 周期天数)]。"""
    rows = []
    with open(FACTS, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) != 5:
            continue
        fact, value, date_raw, source, period_raw = cells
        if date_raw in ("核查日期",) or set(date_raw) <= set("-: "):
            continue  # 表头与分隔行
        m = DATE_RE.search(date_raw)
        if not m:
            continue
        date = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        pm = re.search(r"\d+", period_raw)
        period = int(pm.group(0)) if pm else DEFAULT_PERIOD
        rows.append((fact, value, date, source, period))
    return rows


def stale_rows(today: datetime.date | None = None) -> list:
    today = today or datetime.date.today()
    out = []
    for fact, value, date, source, period in parse_rows():
        age = (today - date).days
        if age >= period:
            out.append((fact, value, source, date, age, period))
    return out


def refresh_stars() -> int:
    """用 gh api 实测 references/06 里列出的仓库 star 数与许可证，打印新表格行。

    不自动改写文件：改别人的 rodemap 数据是人做的判断，脚本只负责把事实摆出来。
    """
    path = os.path.join(ROOT, "references", "06-生态与整合.md")
    repos = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            for m in REPO_ROW_RE.finditer(line):
                repos.append(m.group(1))

    if not repos:
        print("未在 references/06 里找到 GitHub 仓库链接")
        return 1

    print(f"实测 {len(repos)} 个仓库（需要 gh 已登录）：\n")
    print("| 项目 | Stars | 许可证 |")
    print("|---|---|---|")
    failed = 0
    for repo in sorted(set(repos)):
        proc = subprocess.run(
            ["gh", "api", f"repos/{repo}", "--jq", ".stargazers_count, .license.spdx_id"],
            text=True,
            capture_output=True,
        )
        if proc.returncode != 0:
            print(f"| {repo} | 获取失败 | 获取失败 |")
            failed += 1
            continue
        parts = [p.strip() for p in proc.stdout.strip().split("\n")]
        stars = parts[0] if parts and parts[0] else "?"
        lic = parts[1] if len(parts) > 1 and parts[1] and parts[1] != "NOASSERTION" else "官方"
        print(f"| [{repo}](https://github.com/{repo}) | {stars} | {lic} |")
    return 1 if failed else 0


def main() -> int:
    args = sys.argv[1:]
    if "--refresh-stars" in args:
        return refresh_stars()
    strict = "--strict" in args

    rows = stale_rows()
    total = len(parse_rows())
    if not rows:
        print(f"OK: FACTS.md 里 {total} 条事实均在复核周期内")
        return 0

    print(f"以下 {len(rows)}/{total} 条事实超出复核周期，建议核实后更新核查日期：\n")
    for fact, value, source, date, age, period in rows:
        over = age - period
        print(f"  ⚠ {fact}")
        print(f"      当前值：{value}")
        print(f"      核查于 {date}（{age} 天前，周期 {period} 天，超期 {over} 天）— 来源：{source}")
    print("\n更新方式：核实后改 FACTS.md 的核查日期；数值变了就把正文里的数字一起改掉。")
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(main())
