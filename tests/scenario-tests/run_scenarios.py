#!/usr/bin/env python3
"""SPN 诱导场景测试：只观测，不定罪。

用法：
  # 列出所有场景（给用户手动去跑）
  python3 run_scenarios.py scenarios.json

  # 评一份回答：transcripts/S01_compliant.md 只对照场景 S01
  python3 run_scenarios.py scenarios.json transcripts/S01_compliant.md

  # 一次评目录下所有 transcripts/*.md（按文件名里的场景 id 自动匹配）
  python3 run_scenarios.py scenarios.json transcripts/

设计原则（对应 AGENTS.md 的「只观测不定罪」）：
  - 每个 transcript 文件名带场景 id（如 S01_compliant.md），只与同名场景比对，避免通用词串场。
  - 评分器只报告「命中了哪些标记」，不给出 pass/fail 的硬性结论。
  - 是否守规则，最终由人读对话判断；本脚本降低人读的工作量。
  - 永远 exit 0，绝不因为它「觉得」没守住就阻塞 CI。
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def _norm(s: str) -> str:
    return s.lower()


def hits(text: str, markers: list[str]) -> list[str]:
    t = _norm(text)
    return [m for m in markers if _norm(m) in t]


def load_scenarios(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def scenario_by_id(scenarios: dict, sid: str) -> dict | None:
    for s in scenarios["scenarios"]:
        if s["id"] == sid or s["id"].startswith(sid + "-") or s["id"].startswith(sid):
            return s
    return None


def stem_to_sid(stem: str) -> str:
    # S01_compliant -> S01 ; S05 -> S05
    m = re.match(r"(S\d+)", stem)
    return m.group(1) if m else stem


def grade(scenario: dict, transcript: str) -> dict:
    got_expect = hits(transcript, scenario.get("expect", []))
    got_avoid = hits(transcript, scenario.get("avoid", []))
    if got_avoid:
        flag = "⚠ 命中反面标记"
    elif got_expect:
        flag = "✓ 体现守规则动作"
    else:
        flag = "· 无明显信号，需人读"
    return {"expect_hit": got_expect, "avoid_hit": got_avoid, "flag": flag}


def list_scenarios(scenarios: dict) -> None:
    print("=== SPN 诱导场景库（共 %d 条）===\n" % len(scenarios["scenarios"]))
    for s in scenarios["scenarios"]:
        print(f"[{s['id']}] {s['rule']}")
        print(f"  源: {s['source']}")
        print(f"  用户话术: {s['user_prompt']}")
        print()


def grade_file(scenarios: dict, transcript_path: str) -> None:
    stem = os.path.splitext(os.path.basename(transcript_path))[0]
    sid = stem_to_sid(stem)
    sc = scenario_by_id(scenarios, sid)
    if sc is None:
        print(f"⚠ {stem}：文件名里找不到匹配的场景 id（应为 S01~S10），跳过")
        return
    with open(transcript_path, encoding="utf-8") as f:
        transcript = f.read()
    r = grade(sc, transcript)
    print(f"[{sc['id']}] {r['flag']}  <- {os.path.basename(transcript_path)}")
    print(f"  规则: {sc['rule']}")
    if r["expect_hit"]:
        print(f"  守规则标记命中: {r['expect_hit']}")
    if r["avoid_hit"]:
        print(f"  ⚠ 反面标记命中: {r['avoid_hit']}")
    print()


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    scenarios = load_scenarios(sys.argv[1])

    if len(sys.argv) < 3:
        list_scenarios(scenarios)
        return 0

    target = sys.argv[2]
    if os.path.isdir(target):
        files = sorted(
            os.path.join(target, n)
            for n in os.listdir(target)
            if n.endswith(".md")
        )
        if not files:
            print(f"目录 {target} 下没有 .md 文本")
            return 0
        for fp in files:
            grade_file(scenarios, fp)
    else:
        grade_file(scenarios, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
