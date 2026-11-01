#!/usr/bin/env python3
"""校验技能包是否符合 Agent Skills 规范。

用法：
    python3 scripts/validate_skills.py             # 校验 templates/skills/ 与 skills/
    python3 scripts/validate_skills.py --verbose   # 附带输出每个包的基本信息
    python3 scripts/validate_skills.py --path X    # 指定其它目录

校验的是那些**写错就装不上或触发不了**的硬约束，不管文笔与内容好坏：
    - frontmatter 必须存在且含 name / description
    - name 必须小写连字符、与父目录同名、且不含保留词 claude / anthropic
    - description 不超过 1024 字符（上传校验施加的上限）
    - SKILL.md 正文不能是空壳

为什么不改成报错就中止：一次性列出全部问题，比改一个跑一次更快。
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_DIRS = ["templates/skills", "skills"]
MAX_DESCRIPTION = 1024
RESERVED_WORDS = ("claude", "anthropic")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def find_packages(base_dirs: list) -> list:
    """返回 [(包目录绝对路径, SKILL.md 路径)]。跳过以下划线开头的骨架以外的辅助目录。"""
    pkgs = []
    for rel in base_dirs:
        root = os.path.join(ROOT, rel)
        if not os.path.isdir(root):
            continue
        for entry in sorted(os.listdir(root)):
            full = os.path.join(root, entry)
            if not os.path.isdir(full):
                continue
            skill = os.path.join(full, "SKILL.md")
            if os.path.isfile(skill):
                pkgs.append((full, skill))
    return pkgs


def read_frontmatter(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        stripped = line.strip()
        if ":" not in stripped:
            continue
        key, _, val = stripped.partition(":")
        fields[key.strip()] = val.strip()
    return fields


def body_length(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    body = FRONTMATTER_RE.sub("", text, count=1)
    # 去掉代码块与空行后再算，避免把示例命令当成正文
    lines = [ln for ln in body.splitlines() if ln.strip() and not ln.lstrip().startswith("```")]
    return len("".join(lines))


def check_package(pkg_dir: str, skill_path: str) -> list:
    # --path 可能传入仓库外的绝对路径，此时 relpath 会退化成 ../../..，不如直接显示原路径
    rel = skill_path if os.path.isabs(skill_path) else os.path.relpath(skill_path, ROOT)
    problems = []
    fm = read_frontmatter(skill_path)

    if not fm:
        return [f"{rel}: 缺少 frontmatter（--- 包裹的 name / description）"]

    name = fm.get("name", "")
    description = fm.get("description", "")
    dirname = os.path.basename(pkg_dir)

    if not name:
        problems.append(f"{rel}: frontmatter 缺少 name")
    else:
        if not NAME_RE.match(name):
            problems.append(f"{rel}: name 必须是小写字母数字、连字符分隔（当前 {name!r}）")
        if name != dirname and not dirname.startswith("_"):
            problems.append(f"{rel}: name（{name}）与父目录名（{dirname}）不一致，规范要求同名")
        low = name.lower()
        for word in RESERVED_WORDS:
            if word in low:
                problems.append(f"{rel}: name 不能包含保留词 {word!r}")

    if not description:
        problems.append(f"{rel}: frontmatter 缺少 description（这一行决定 Agent 会不会加载它）")
    elif len(description) > MAX_DESCRIPTION:
        problems.append(
            f"{rel}: description 有 {len(description)} 字符，超出 {MAX_DESCRIPTION} 上限（会被上传校验拒绝）"
        )

    if body_length(skill_path) < 200:
        problems.append(f"{rel}: 正文太短（有效字符 {body_length(skill_path)}），装上去大概率没作用")

    return problems


def main() -> int:
    args = sys.argv[1:]
    verbose = "--verbose" in args
    if "--path" in args:
        i = args.index("--path")
        dirs = [args[i + 1]] if len(args) > i + 1 else DEFAULT_DIRS
    else:
        dirs = DEFAULT_DIRS

    pkgs = find_packages(dirs)
    if not pkgs:
        print(f"✗ 没有找到任何技能包，检查目录是否存在：{dirs}")
        return 1

    problems = []
    for pkg_dir, skill in pkgs:
        problems.extend(check_package(pkg_dir, skill))

    if verbose:
        print(f"扫描 {len(pkgs)} 个技能包：\n")
        for pkg_dir, skill in pkgs:
            fm = read_frontmatter(skill)
            desc = fm.get("description", "")
            print(f"  {fm.get('name', '?'):<24} description {len(desc):>4} 字符  正文 {body_length(skill):>4} 字符")
        print()

    if problems:
        print(f"✗ 发现 {len(problems)} 个问题：\n")
        for p in problems:
            print(f"  ::error:: {p}")
        return 1

    print(f"✓ 规范校验通过：{len(pkgs)} 个技能包")
    return 0


if __name__ == "__main__":
    sys.exit(main())
