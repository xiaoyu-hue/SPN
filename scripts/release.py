#!/usr/bin/env python3
"""SPN 一键发布：一处填版本号，全仓库同步，校验通过后打 tag 并建 Release。

用法：
    python3 scripts/release.py 1.0.1          # 预览：只打印将要改的内容，不写盘、不推送
    python3 scripts/release.py 1.0.1 --yes    # 真正发布：写盘 → 校验 → 提交 → 打 tag → 推送 → 建 Release

它做五件事（顺序固定，任何一步失败即中止）：
    1. 把 CHANGELOG.md 的 [Unreleased] 内容提升为 [新版本] - 日期，并留一个空的 [Unreleased]
    2. 同步中英 README 的版本徽章、Release 链接、页脚版本号
    3. 同步 SKILL.md 的 metadata.version（仅规范源两份：根目录与 docs/）
    4. 由 sync_snapshots.py 生成两个技能包的 SKILL.md 正文（链接锁定到新 tag）与 AGENTS.md 快照
    5. 跑 doc-lint 规则模拟 + 链接检查，全绿才提交

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
# 技能包副本（skills/spn/SKILL.md、skills/spn-en/SKILL.md）的版本号与正文
# 已由 sync_snapshots.py 统一生成，这里只处理真正独立的规范源文件。
SKILL_FILES = ["SKILL.md", "docs/SKILL.md"]

# 技能包副本（skills/spn/SKILL.md、skills/spn-en/SKILL.md）的版本号与正文
# 这里不再手写 PACKAGES —— 两份同步逻辑各写一遍正是当初 SKILL.md 正文漏同步的原因。

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")

# 数字写死检查由 scripts/doc_lint.py 单独实现，发版时直接复用同一个入口——
# 复制一份正则到本文件，就是它后来与 CI 行为漂移、名存实亡的原因。


def die(msg: str) -> None:
    print(f"\n✗ {msg}")
    sys.exit(1)


def remote_tag_exists(tag: str) -> bool:
    """查远端是否已有同名 tag。

    两个健壮性处理（都是被现实教过的）：
      - 加超时：网络挂起时发版脚本会卡死，而使用者看不出是卡了还是坏了。
      - 失败时给中文原因：直接抛 subprocess traceback 对不看代码的人是灾难，
        必须说清"连不上远端"以及下一步该做什么。
    """
    r = sh(
        "git", "ls-remote", "--tags", "origin", f"refs/tags/{tag}",
        check=False, timeout=30,
    )
    if r.returncode != 0:
        die(
            "查不到远端仓库，无法确认 tag 是否被占用。\n"
            "  先运行 git remote -v 看看 origin 是否配好；\n"
            "  如果是网络问题，修复后重来即可（本次没有改动任何文件）。"
        )
    return bool(r.stdout.strip())


def sh(*args: str, check: bool = True, timeout: int | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        args, cwd=ROOT, text=True, capture_output=True, check=check, timeout=timeout
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
    if remote_tag_exists(tag):
        die(f"远端已存在 tag {tag}")

    # 计算目标内容
    plan = {}
    plan["CHANGELOG.md"] = bump_changelog(read("CHANGELOG.md"), version, date)
    for f in BADGE_FILES:
        plan[f] = bump_readme(read(f), old, version)
    for f in SKILL_FILES:
        plan[f] = bump_skill(read(f), old, version)

    # 发布副本（技能包的 SKILL.md 正文 + AGENTS.md 快照）统一由 sync_snapshots 生成，
    # 避免"版本号在这里改、正文在别处改"的两处逻辑各写一遍。
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import sync_snapshots  # noqa: E402

    try:
        plan.update(sync_snapshots.plan(version))
    except ValueError as exc:
        die(f"发布副本生成失败：{exc}")

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
    import doc_lint  # noqa: E402

    problems = doc_lint.problems_of(diff_files=list(changed))
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

    # 推送失败是常态（远端有新提交、权限不足、网络断了），此时本地已经提交并打好 tag，
    # 使用者需要知道"现在是什么状态、怎么收拾"，而不是看一段 traceback。
    for ref in ("main", tag):
        r = sh("git", "push", "origin", ref, check=False, timeout=120)
        if r.returncode == 0:
            print(f"✓ 已推送 {ref}")
            continue
        print(f"\n✗ 推送 {ref} 失败：")
        detail = (r.stderr.strip() or r.stdout.strip()).replace("\n", "\n  ")
        print("  " + detail)
        print(
            f"\n当前状态：本地已提交并且 tag {tag} 已建好，但没推到远端——远端还停在旧版本。\n"
            f"\n最常见的两个原因：\n"
            f"  1. 远端有你本地没有的提交 → 先 git pull --rebase 再重新推送\n"
            f"  2. 没有推送权限或没登录 → 检查权限后重试\n"
            f"\n重推这两步就行：\n"
            f"    git push origin main\n    git push origin {tag}\n"
            f"\n想彻底撤销这次发版尝试（⚠ 会丢弃本地那次 release 提交，"
            f"执行前确认没有其他重要改动）：\n"
            f"    git tag -d {tag} && git reset --hard HEAD~1\n"
        )
        sys.exit(1)

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
