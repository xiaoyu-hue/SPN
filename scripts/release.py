#!/usr/bin/env python3
"""SPN 一键发布：一处填版本号，全仓库同步，校验通过后打 tag 并建 Release。

用法：
    python3 scripts/release.py 1.0.1          # 预览：只打印将要改的内容，不写盘、不推送
    python3 scripts/release.py 1.0.1 --yes    # 真正发布：写盘 → 校验 → 提交 → 打 tag → 推送 → 建 Release

它做六件事（顺序固定，任何一步失败即中止）：
    1. 把 CHANGELOG.md 的 [Unreleased] 内容提升为 [新版本] - 日期，并留一个空的 [Unreleased]
    2. 同步中英 README 的版本徽章、Release 链接、页脚版本号
    3. 同步三个 SKILL.md 的 metadata.version
    4. 把 skills/spn/SKILL.md 里的 GitHub 链接从旧 tag 改到新 tag（保证技能包可复现）
    5. 用根目录 AGENTS.md 刷新技能包内的快照
    6. 跑 doc-lint 规则模拟 + 链接检查，全绿才提交

设计取舍：
    - 默认 dry-run。发布是不可逆动作（公开 tag、公开 Release），必须先看一眼 diff。
    - 用 Python 而不是 bash：Windows 上没有 bash，而本项目的目标用户大量在 Windows。
    - 只依赖标准库与 git / gh 命令，不引入任何第三方包。
"""

from __future__ import annotations

import datetime
import difflib
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BADGE_FILES = ["README.md", "docs/README.md"]
SKILL_FILES = ["SKILL.md", "docs/SKILL.md", "skills/spn/SKILL.md", "skills/spn-en/SKILL.md"]

# 技能包三件套：(包内 SKILL.md, 包内 AGENTS.md 快照, 快照来源, 快照注释)
# 规范要求 name 与父目录同名，所以中英两个包只能分别叫 spn / spn-en。
PACKAGES = [
    (
        "skills/spn/SKILL.md",
        "skills/spn/AGENTS.md",
        "AGENTS.md",
        "<!-- 发布快照：本文件同步自仓库根目录 AGENTS.md。修改规则请改根目录源，再同步到此。 -->\n\n",
    ),
    (
        "skills/spn-en/SKILL.md",
        "skills/spn-en/AGENTS.md",
        "docs/AGENTS.md",
        "<!-- Release snapshot: synced from docs/AGENTS.md in the repository root. "
        "Edit the source there, then re-sync here. -->\n\n",
    ),
]

# 与 .github/workflows/doc-lint.yml 保持一致
LINT_FILES = ["README.md", "AGENTS.md", "SKILL.md"]


def _listdir(rel_dir: str) -> list:
    full = os.path.join(ROOT, rel_dir)
    if not os.path.isdir(full):
        return []
    return [f"{rel_dir}/{n}" for n in sorted(os.listdir(full)) if n.endswith(".md")]


LINT_FILES += _listdir("references")
LINT_FILES += [
    "docs/README.md",
    "docs/AGENTS.md",
    "docs/SKILL.md",
    "docs/SECURITY.md",
    "docs/CONTRIBUTING.md",
]
LINT_FILES += _listdir("docs/references")

HARDCODE_RE = re.compile(
    r"[0-9]{3,}[ \t]*(项测试|个模块|条测试|测试|模块|时间线|工具|书)|v[0-9]+\.[0-9]+\.[0-9]+"
)
LINT_EXCLUDE_RE = re.compile(r"❌|而不是|→|https?://")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def die(msg: str) -> None:
    print(f"\n✗ {msg}")
    sys.exit(1)


def sh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        args, cwd=ROOT, text=True, capture_output=True, check=check
    )


def read(path: str) -> str:
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def current_version() -> str:
    """从 README 的版本徽章读出当前版本（唯一可机器读取的版本锚点）。"""
    m = re.search(r"version-([0-9]+\.[0-9]+\.[0-9]+)-blue", read("README.md"))
    if not m:
        die("README.md 里找不到版本徽章（version-X.Y.Z-blue），无法判断当前版本")
    return m.group(1)


def bump_changelog(text: str, version: str, date: str) -> str:
    m = re.search(r"^## \[Unreleased\][ \t]*\n(.*?)(?=^## \[)", text, re.S | re.M)
    if not m:
        die("CHANGELOG.md 里找不到 '## [Unreleased]' 段落")
    body = m.group(1).strip("\n")
    if not body.strip():
        die("CHANGELOG.md 的 [Unreleased] 是空的：没有待发布内容，先写日志再发版")
    block = f"## [Unreleased]\n\n## [{version}] - {date}\n\n{body}\n\n"
    return text[: m.start()] + block + text[m.end() :]


def bump_readme(text: str, old: str, new: str) -> str:
    text = text.replace(f"version-{old}-blue", f"version-{new}-blue")
    text = text.replace(f"版本 {old}", f"版本 {new}")      # 中文徽章的显示文字
    text = text.replace(f"version {old}", f"version {new}")  # 英文徽章的显示文字
    text = text.replace(f"releases/tag/v{old}", f"releases/tag/v{new}")
    text = text.replace(f"`v{old}`", f"`v{new}`")
    return text


def bump_skill(text: str, old: str, new: str) -> str:
    return re.sub(rf'version:[ \t]*"{re.escape(old)}"', f'version: "{new}"', text)


def pin_links(text: str, old: str, new: str) -> str:
    """技能包内的 GitHub 链接锁定到本次 tag，保证安装到的内容可复现。"""
    text = text.replace(f"blob/v{old}/", f"blob/v{new}/")
    text = text.replace("blob/main/", f"blob/v{new}/")
    return text


def lint_problems() -> list:
    problems = []
    for rel in LINT_FILES:
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            continue
        if "references/03" in rel:
            continue  # 教学文档，整篇是反面示例
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                if HARDCODE_RE.search(line) and not LINT_EXCLUDE_RE.search(line):
                    problems.append(f"{rel}:{lineno} 疑似写死数字：{line.strip()[:80]}")
    return problems


def changelog_section(text: str, version: str) -> str:
    m = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.S | re.M)
    return (m.group(1).strip() if m else "").strip()


def main() -> int:
    args = [a for a in sys.argv[1:]]
    apply = "--yes" in args or "-y" in args
    rest = [a for a in args if a not in ("--yes", "-y")]
    if len(rest) != 1 or rest[0] in ("-h", "--help"):
        print(__doc__)
        return 1
    version = rest[0].lstrip("v")
    if not SEMVER_RE.match(version):
        die(f"版本号必须形如 1.0.1（不要带 v 前缀），收到：{version}")

    tag = f"v{version}"
    date = datetime.date.today().isoformat()
    old = current_version()
    if old == version:
        die(f"当前已是 {version}，没有需要发布的变更")

    # 前置检查：分支、工作区、tag 冲突
    branch = sh("git", "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch != "main":
        die(f"当前在 {branch} 分支，请在 main 上发布")
    if sh("git", "status", "--porcelain").stdout.strip():
        print(sh("git", "status", "--short").stdout)
        die("工作区不干净，先提交或丢弃改动")
    if sh("git", "tag", "-l", tag).stdout.strip():
        die(f"本地已存在 tag {tag}")
    if sh("git", "ls-remote", "--tags", "origin", f"refs/tags/{tag}").stdout.strip():
        die(f"远端已存在 tag {tag}")

    # 计算目标内容
    plan = {}
    plan["CHANGELOG.md"] = bump_changelog(read("CHANGELOG.md"), version, date)
    for f in BADGE_FILES:
        plan[f] = bump_readme(read(f), old, version)
    for f in SKILL_FILES:
        plan[f] = bump_skill(read(f), old, version)
    for skill_md, snapshot_md, source_md, notice in PACKAGES:
        plan[skill_md] = pin_links(plan[skill_md], old, version)
        plan[snapshot_md] = notice + read(source_md)

    changed = {f: c for f, c in plan.items() if c != read(f)}
    if not changed:
        die("所有文件都已是最新，没有任何需要写入的改动")

    print(f"\n发布计划：{old} → {version}（tag {tag}，日期 {date}）\n")
    for f, content in changed.items():
        diff = difflib.unified_diff(
            read(f).splitlines(keepends=True),
            content.splitlines(keepends=True),
            fromfile=f"a/{f}",
            tofile=f"b/{f}",
            n=2,
        )
        sys.stdout.writelines(diff)
        print()

    if not apply:
        print("以上为预览。加 --yes 才会真正写盘、提交并推送。")
        return 0

    for f, content in changed.items():
        with open(os.path.join(ROOT, f), "w", encoding="utf-8") as fh:
            fh.write(content)
    print(f"✓ 已写入 {len(changed)} 个文件")

    # 校验
    problems = lint_problems()
    if problems:
        print("\n✗ doc-lint 未通过：")
        for p in problems:
            print("  " + p)
        die("请修正后重新执行（文件已写入，可用 git checkout 撤销）")
    print("✓ doc-lint 通过：未发现写死数字")

    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import check_links  # noqa: E402

    md_count, link_count, link_problems = check_links.check(verbose=False)
    if link_problems:
        print("\n✗ 链接检查未通过：")
        for p in link_problems:
            print("  " + p)
        die("请修正后重新执行")
    print(f"✓ 链接检查通过：{md_count} 个文件、{link_count} 条相对链接")

    # 提交、打 tag、推送
    sh("git", "add", "-A")
    sh("git", "commit", "-m", f"chore(release): {tag}")
    print(f"✓ 已提交 chore(release): {tag}")

    section = changelog_section(read("CHANGELOG.md"), version)
    notes = f"{section}\n\n完整变更见 [CHANGELOG.md](https://github.com/xiaoyu-hue/SPN/blob/main/CHANGELOG.md)。\n"
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tf:
        tf.write(notes)
        notes_path = tf.name

    sh("git", "tag", "-a", tag, "-m", f"SPN {tag}\n\n{section}")
    print(f"✓ 已创建附注 tag {tag}")

    sh("git", "push", "origin", "main")
    sh("git", "push", "origin", tag)
    print(f"✓ 已推送 main 与 {tag}")

    rel = sh(
        "gh", "release", "create", tag,
        "--title", f"SPN {tag}",
        "--notes-file", notes_path,
        "--latest",
        check=False,
    )
    if rel.returncode == 0:
        print(f"✓ Release 已创建：{rel.stdout.strip()}")
    else:
        print("⚠ Release 创建失败（tag 已推送，可稍后重试）：")
        print(rel.stderr.strip())

    os.unlink(notes_path)
    print(f"\n完成：{old} → {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
