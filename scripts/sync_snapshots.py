#!/usr/bin/env python3
"""把「规范源」同步成「发布副本」，并能在 CI 里校验两者是否一致。

背景（为什么要这个脚本）：
    README 说「根目录是唯一规范源」，docs/ 与 skills/ 是发布副本。
    但发版脚本原先只同步版本号、链接 tag 与 AGENTS.md 快照，
    SKILL.md 正文长期靠手工对齐——一旦漏同步，用户装到 AI 里的规则
    就和仓库里的不一样，而当时没有任何 CI 能发现。本文件堵上这个洞。

两种模式：
    python3 scripts/sync_snapshots.py --check   # 只校验，不一致则退出码 1（CI 用）
    python3 scripts/sync_snapshots.py --apply   # 真正写入发布副本（发版时用）
    python3 scripts/sync_snapshots.py --diff    # 打印统一 diff，不写盘（排查用）

同步内容：
    1. AGENTS.md 快照              源 → 技能包（加一行快照说明注释）
    2. SKILL.md 正文               源 → 技能包（反引号/相对链接 → 锁定 tag 的绝对链接）
    3. SKILL.md frontmatter        version 从参数来，其余字段从源继承

设计取舍：
    - 「包专属措辞」（版本头、"30 秒版本"、引用段的标题与提示语）明确写在本文件的
      PKG_* 常量里，不放进源。理由：它是发布副本特有的，塞进规范源会让根目录文件
      出现"本技能包内附"这种自指语句。
    - 只在 *同一语言内* 同步：根 SKILL.md → spn，docs/SKILL.md → spn-en。
      跨语言的差异是翻译，机器不该碰。
    - 只用标准库，Windows / macOS / Linux 行为一致（本项目的目标用户大量在 Windows）。
"""

from __future__ import annotations

import argparse
import difflib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/xiaoyu-hue/SPN"

# ---------------------------------------------------------------- 包专属措辞

# AGENTS.md 快照顶部的说明注释（各包语言不同）
AGENTS_NOTICE_ZH = "<!-- 发布快照：本文件同步自仓库根目录 AGENTS.md。修改规则请改根目录源，再同步到此。 -->\n\n"
AGENTS_NOTICE_EN = (
    "<!-- Release snapshot: synced from docs/AGENTS.md in the repository root. "
    "Edit the source there, then re-sync here. -->\n\n"
)

# SKILL.md 包专属头部：插在 frontmatter 之后、一级标题之后
HEADER_ZH = """> **这是什么**：SPN 的可安装技能包版本。核心规则已完整内联在本文件，无需联网即可生效。
> **版本**：`{version}`（见 frontmatter 的 `metadata.version`，与 tag `v{version}` 一一对应）。
> **规范源**：仓库根目录 `{repo}`（最新版、可参与贡献）。
> **深度参考**：下文链接全部锁定到 `v{version}`，保证你装到的这份与链接指向的内容完全一致；离线时只影响"点开看细节"，不影响本文件内的规则。

> **30 秒版本**：① 听不懂就喊停，让它翻译成人话再拍板；② 能不能一键还原？能就试，不能就问；③ 它说"已完成"不算数，要它贴命令输出。

"""

HEADER_EN = """> **What this is**: the installable skill-package edition of SPN. The core rules are fully inlined here and work offline.
> **Version**: `{version}` (see `metadata.version` in the frontmatter, matching tag `v{version}`).
> **Source of truth**: repository root `{repo}` (latest version, contributions welcome).
> **Deep references**: links below are pinned to `v{version}`, so what you install matches what the links point to; offline you lose the "read more" clicks, never the rules themselves.

> **30-second version**: (1) If you don't understand a word, stop them and make them translate before you decide. (2) Can it be undone with one action? Yes → try it; no → ask first. (3) "Done" doesn't count — make them paste the command output.

"""

# 「引用文件」段落：包版本用的标题，以及替换第一段 blockquote 的提示语
SECTION_ZH = {
    "title_from": "## 引用文件（通用层）",
    "title_to": "## 引用文件（深度参考，按需点开）",
    "blockquote_from": "> ⚠️ `personal/` 目录是作者自用的补充层，**不是通用规则的一部分**，处理一般任务时跳过。",
    "blockquote_to": (
        "> 下表链接锁定到本技能包对应版本，离线时点不开属正常，本文件内联的规则不受影响。\n"
        "> 全部 8 篇均提供英文版（仓库 `docs/` 目录）。"
    ),
    "tail_from": "`AGENTS.md`（根目录）是可直接拷进任何项目的精简版，内容与本文件一致但更短，且是 AI 实际加载执行的版本。",
    "tail_to": (
        "`AGENTS.md`（本技能包内附）是可拷进任意项目的精简版，与仓库根目录同一份内容，"
        "也是 AI 实际加载执行的版本。规则只允许在根目录修改，再同步到本包——这条一致性由 CI 强制检查。"
    ),
}

SECTION_EN = {
    "title_from": "## Reference files (universal layer)",
    "title_to": "## Reference files (deep detail, open as needed)",
    "blockquote_from": "> NOTE: `personal/` is the author's own layer, **not part of the general rules** — skip it for normal tasks.",
    "blockquote_to": (
        "> Links are pinned to this package's version; not opening offline is normal and doesn't affect the inlined rules.\n"
        "> A Chinese edition of every file lives in the repository root."
    ),
    "tail_from": (
        "`AGENTS.md` (root) is the trimmed version you can drop straight into any project; "
        "its content matches this file but is shorter, and is the version the AI actually loads and executes."
    ),
    "tail_to": (
        "`AGENTS.md` (bundled with this package) is the trimmed version you can drop into any project; "
        "it's the same content as the repository root's English `AGENTS.md`, and the version the AI actually loads. "
        "Rules may only be edited at the root and then synced here — CI enforces that."
    ),
}

PACKAGES = [
    {
        "name": "spn",
        "skill_src": "SKILL.md",
        "skill_dst": "skills/spn/SKILL.md",
        "agents_src": "AGENTS.md",
        "agents_dst": "skills/spn/AGENTS.md",
        "agents_notice": AGENTS_NOTICE_ZH,
        "header": HEADER_ZH,
        "section": SECTION_ZH,
        "ref_prefix": "",
    },
    {
        "name": "spn-en",
        "skill_src": "docs/SKILL.md",
        "skill_dst": "skills/spn-en/SKILL.md",
        "agents_src": "docs/AGENTS.md",
        "agents_dst": "skills/spn-en/AGENTS.md",
        "agents_notice": AGENTS_NOTICE_EN,
        "header": HEADER_EN,
        "section": SECTION_EN,
        "ref_prefix": "docs/",
    },
]

# ---------------------------------------------------------------- 基础工具

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
DOC_PATH_RE = re.compile(r"`((?:docs/)?references/[^\s`]+\.md)`")
FENCE_RE = re.compile(r"^```")


def read(path: str) -> str:
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path: str, content: str) -> None:
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(content)


def split_frontmatter(text: str) -> tuple:
    """返回 (frontmatter 原文含分隔符, 正文)。没有 frontmatter 时前者为空串。"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(0), text[m.end():]


def render_frontmatter(src_text: str, pkg_name: str, version: str) -> str:
    """frontmatter：name 跟随目录名（Agent Skills 规范要求），其余字段继承源。"""
    fm, _ = split_frontmatter(src_text)
    if not fm:
        raise ValueError("源文件缺少 frontmatter")

    fields = {}
    for line in fm.splitlines()[1:-1]:
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        # 支持一层嵌套：metadata 下的 author。写成通用结构会让配置变复杂，
        # 而这两个字段就是本项目 frontmatter 的全部嵌套需求，不必为假想场景加抽象。
        if line.startswith(("  ", "\t")):
            key, _, val = stripped.partition(":")
            if key in ("author",):
                fields[key] = val.strip()
            continue
        key, _, val = stripped.partition(":")
        fields[key.strip()] = val.strip()

    out = [
        "---",
        f"name: {pkg_name}",
        f"description: {fields.get('description', '')}",
        f"license: {fields.get('license', '')}",
        "metadata:",
        f"  author: {fields.get('author', '')}",
        f'  version: "{version}"',
        "---\n",
    ]
    # 再加一个换行：正文自带的时间才能让 frontmatter 与 `# ` 标题之间留出空行
    return "\n".join(out) + "\n"


def linkify_outside_code(text: str, version: str, ref_prefix: str = "") -> str:
    """把仓库内相对 .md 链接换成锁定 tag 的绝对链接（代码块内的保持不动）。

    ref_prefix：源里写的是"从源文件出发"的相对路径，而生成出来的 URL 是"从仓库根
    出发"的。英文技能包的源在 docs/ 下，references 也在 docs/ 下，两者又要指向
    docs/references/，所以这里补一层前缀。

    跳过：外链、锚点、mailto、以及不以 .md 结尾的目标（防止把 `docs/` 这类
    目录引用错误地变成死链）。
    """
    base = f"{REPO}/blob/v{version}/"
    lines = text.split("\n")
    in_fence = False
    out = []

    # 不用 urllib.parse.quote：它会把中文转成 %E5%8D%8F... ，而 GitHub 的 blob URL
    # 里中文路径直接写 UTF-8 原样即可访问，保留原文可读性更好、人也更容易核对。
    # 真正必须转码的只有空格。
    def to_abs(path: str) -> str:
        return base + (ref_prefix + path).replace(" ", "%20")

    for line in lines:
        if FENCE_RE.match(line.lstrip()):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        def _md(match: re.Match) -> str:
            label, target = match.group(1), match.group(2)
            if target.startswith(("http://", "https://", "mailto:", "//", "#")):
                return match.group(0)
            if not target.endswith(".md"):
                return match.group(0)
            return f"[{label}]({to_abs(target)})"

        line = MD_LINK_RE.sub(_md, line)

        def _doc(match: re.Match) -> str:
            path = match.group(1)
            stem = path.rsplit("/", 1)[-1][: -len(".md")]
            return f"[{stem}]({to_abs(path)})"

        line = DOC_PATH_RE.sub(_doc, line)
        out.append(line)

    return "\n".join(out)


def normalize_ref_labels(text: str) -> str:
    """把 [`references/01-foo.md`](references/01-foo.md) 统一成 [01-foo](references/01-foo.md)。

    「显示文字=完整路径」是源文件的历史写法，进到包里会变成又长又难读的链接。
    统一成短名后，中英文显示出一致的观感，label 也不再需要跟着文件名改。
    """
    def repl(m: re.Match) -> str:
        label, target = m.group(1), m.group(2)
        stem = target.rsplit("/", 1)[-1].removesuffix(".md")
        if label.strip("`") == target:
            return f"[{stem}]({target})"
        return m.group(0)

    return MD_LINK_RE.sub(repl, text)


def inject_header(body: str, header_tpl: str, version: str) -> str:
    """把包专属头部插在「一级标题 + 其后的引言」之后、第一个二级标题之前。"""
    header = header_tpl.format(version=version, repo=REPO)
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("## "):
            insert_at = i
            while insert_at > 0 and lines[insert_at - 1].strip() == "":
                insert_at -= 1
            lines[insert_at:insert_at] = [""] + header.rstrip("\n").split("\n")
            break
    else:
        lines.extend(header.rstrip("\n").split("\n"))
    return "\n".join(lines)


def apply_section_overrides(body: str, cfg: dict) -> str:
    """把「引用文件」段落替换成包版本的措辞。失败的替换要报错，不能静默跳过。"""
    missing = []
    for key in ("title_from", "blockquote_from", "tail_from"):
        needle = cfg[key]
        if needle not in body:
            missing.append(key)
    if missing:
        raise ValueError(
            f"源文件中找不到约定锚点 {missing}：包专属措辞写死在 sync_snapshots.py，"
            f"改了源里的对应句子就要同步改这里（宁可报错，不要静默漏替换）"
        )

    body = body.replace(cfg["title_from"], cfg["title_to"], 1)
    body = body.replace(cfg["blockquote_from"], cfg["blockquote_to"], 1)
    body = body.replace(cfg["tail_from"], cfg["tail_to"], 1)
    return body


# ---------------------------------------------------------------- 生成

def build_agents_snapshot(src_text: str, notice: str) -> str:
    return notice + src_text


def build_skill(src_path: str, pkg: dict, version: str) -> str:
    src = read(src_path)
    fm_src, src_body = split_frontmatter(src)
    _ = fm_src  # 保留以便将来扩展；此处仅用于确保源确实带 frontmatter

    body = src_body.lstrip("\n")
    body = normalize_ref_labels(body)
    body = linkify_outside_code(body, version, pkg.get("ref_prefix", ""))
    body = apply_section_overrides(body, pkg["section"])
    body = inject_header(body, pkg["header"], version)

    return render_frontmatter(src, pkg["name"], version) + body


def plan(version: str) -> dict:
    """返回 {目标相对路径: 应写入的内容}，供 release.py 与预览共用。"""
    out = {}
    for pkg in PACKAGES:
        out[pkg["agents_dst"]] = build_agents_snapshot(
            read(pkg["agents_src"]), pkg["agents_notice"]
        )
        out[pkg["skill_dst"]] = build_skill(pkg["skill_src"], pkg, version)
    return out


def check_all(version: str) -> list:
    """返回 [(目标相对路径, 期望内容, 实际内容)]，空列表代表全部一致。"""
    diffs = []
    for dst, expected in plan(version).items():
        actual = read(dst)
        if actual != expected:
            diffs.append((dst, expected, actual))
    return diffs


# ---------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description="同步 / 校验 SPN 的发布副本")
    ap.add_argument("version", nargs="?", help="目标版本号，如 1.0.1")
    ap.add_argument("--check", action="store_true", help="只校验，不一致退出码 1")
    ap.add_argument("--apply", action="store_true", help="写入发布副本")
    ap.add_argument("--diff", action="store_true", help="打印 diff 但不写盘")
    args = ap.parse_args()

    version = (args.version or "").lstrip("v")
    if not version:
        # 从 README 徽章读当前版本，保证与 release.py 的唯一锚点一致
        m = re.search(r"version-([0-9]+\.[0-9]+\.[0-9]+)-blue", read("README.md"))
        if not m:
            print("✗ 无法从 README.md 读出版本号，请显式传入：python3 scripts/sync_snapshots.py 1.0.1")
            return 1
        version = m.group(1)

    try:
        diffs = check_all(version)
    except ValueError as exc:
        print(f"✗ {exc}")
        return 1

    if not diffs:
        print(f"✓ 发布副本与规范源一致（v{version}）：{len(PACKAGES) * 2} 个目标文件")
        return 0

    print(f"发现 {len(diffs)} 个文件需要同步（v{version}）：\n")
    for dst, expected, actual in diffs:
        print("=" * 70)
        print(f"--- {dst}")
        sys.stdout.writelines(
            difflib.unified_diff(
                actual.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=f"当前/{dst}",
                tofile=f"同步后/{dst}",
                n=1,
            )
        )
        print()

    if args.apply:
        for dst, expected, _ in diffs:
            write(dst, expected)
            print(f"✓ 已写入 {dst}")
        print(f"\n完成，共 {len(diffs)} 个文件。请复核 diff 后再提交。")
        return 0

    if args.check:
        print("修复：python3 scripts/sync_snapshots.py --apply（发版会自动调用）")
        return 1

    print("以上为预览。用 --apply 写入，或 --check 只做校验（CI 模式）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
