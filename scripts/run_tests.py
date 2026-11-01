#!/usr/bin/env python3
"""scripts/ 下 MIT 代码的单元测试（纯标准库，不需要 pytest）。

用法：
    python3 scripts/run_tests.py
    python3 scripts/run_tests.py -v

为什么要有这个文件：
    AGENTS.md 第 92 行写着「新增或修改功能逻辑必须同步写测试」。
    本仓库的 MIT 代码长期零测试，等于自己的规则没对自己生效。
    用标准库 unittest 而不是 pytest：本项目承诺"只用标准库"，
    多一个第三方依赖就多一层安装门槛，与目标用户（不懂命令行的人）不符。
"""

from __future__ import annotations

import contextlib
import datetime
import io
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_facts  # noqa: E402
import check_links  # noqa: E402
import doc_lint  # noqa: E402
import release  # noqa: E402
import sync_snapshots  # noqa: E402
import validate_skills  # noqa: E402

sys.path.insert(0, os.path.join(ROOT, "tests", "scenario-tests"))
import run_scenarios  # noqa: E402


class TestSlugify(unittest.TestCase):
    """锚点生成必须与 GitHub 实际行为一致，否则会在别人的仓库里误报。"""

    def test_ascii_lowercase_and_spaces(self):
        self.assertEqual(check_links.slugify("Hello World"), "hello-world")

    def test_punctuation_dropped(self):
        self.assertEqual(check_links.slugify("一、上线前安全自查！"), "一上线前安全自查")

    def test_leading_hash_and_emphasis_stripped(self):
        self.assertEqual(check_links.slugify("## **`AGENTS.md`** 用法"), "agentsmd-用法")

    def test_consecutive_hyphens_collapsed(self):
        self.assertEqual(check_links.slugify("a  --  b"), "a-b")

    def test_emoji_removed(self):
        self.assertEqual(check_links.slugify("一、🚀 快速开始"), "一-快速开始")

    def test_trailing_hyphen_trimmed(self):
        self.assertEqual(check_links.slugify("what is this -"), "what-is-this")

    def test_chinese_preserved(self):
        self.assertEqual(check_links.slugify("参考文献"), "参考文献")


class TestHeadings(unittest.TestCase):
    def test_duplicate_headings_get_numeric_suffix(self):
        """GitHub 对重复标题加 -1 / -2。缺这条会误报，而误报会阻塞发版。"""
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("# 步骤\n\n## 步骤\n\n## 步骤\n\n## 结语\n")
            path = f.name
        try:
            self.assertEqual(
                sorted(check_links.headings_of(path)),
                sorted(["步骤", "步骤-1", "步骤-2", "结语"]),
            )
        finally:
            os.unlink(path)

    def test_missing_file_returns_empty(self):
        self.assertEqual(check_links.headings_of("/nonexistent/path.md"), set())


class TestCheckLinks(unittest.TestCase):
    def test_reports_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "a.md"), "w", encoding="utf-8") as f:
                f.write("[broken](nope.md)\n")
            old_root = check_links.ROOT
            check_links.ROOT = d
            try:
                _, _, problems = check_links.check(verbose=False)
            finally:
                check_links.ROOT = old_root
            self.assertEqual(len(problems), 1)
            self.assertIn("文件不存在", problems[0])

    def test_ignores_external_links(self):
        """外链可达性由 lychee 管，本地脚本不要越界。"""
        line = "[x](https://example.com) [y](#anchor)\n"
        self.assertEqual(check_links.LINK_RE.findall(line), [("x", "https://example.com"), ("y", "#anchor")])

    def test_skips_links_inside_code_fence(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "a.md"), "w", encoding="utf-8") as f:
                f.write("```\n[ignored](nope.md)\n```\n\n[real](nope.md)\n")
            old_root = check_links.ROOT
            check_links.ROOT = d
            try:
                _, checked, problems = check_links.check(verbose=False)
            finally:
                check_links.ROOT = old_root
            self.assertEqual(checked, 1, "代码块里的链接不该计入")
            self.assertEqual(len(problems), 1, "只有代码块外那条该报错")


class TestDocLint(unittest.TestCase):
    def hit(self, text: str) -> bool:
        import re

        probe = doc_lint.strip_exempt(text)
        return any(re.search(p, probe) for p, _ in doc_lint.PATTERNS)

    def test_catches_counts(self):
        self.assertTrue(self.hit("本周新增 573 项测试"))

    def test_catches_capacity(self):
        self.assertTrue(self.hit("免费额度 500MB 够用了"))

    def test_catches_price(self):
        self.assertTrue(self.hit("付费版每月 ¥19.9"))

    def test_catches_wan_scale(self):
        self.assertTrue(self.hit("已有 1.6 万 用户"))

    def test_catches_thousand_separator(self):
        self.assertTrue(self.hit("扫描了 1,645 个应用"))

    def test_catches_version_number(self):
        self.assertTrue(self.hit("当前版本 v1.2.3 已发布"))

    def test_exempts_complete_teaching_pair(self):
        """`旧写法` → `新写法` 的完整对照是示范，不是写死。"""
        self.assertFalse(self.hit("**相对描述**：`573 项测试` → `测试积累到数百项`"))

    def test_half_teaching_pair_is_not_exempt(self):
        """这是旧版本被绕过的洞：只在一侧加引号就想放行，必须仍然被抓住。"""
        self.assertTrue(self.hit("本周新增 `573 项测试` → 详见报表"))

    def test_arrow_alone_does_not_exempt(self):
        """最关键的一条：随手一个箭头不该让写死数字通行。"""
        self.assertTrue(self.hit("免费额度 500MB 够用了 → 详见官网"))

    def test_urls_are_stripped(self):
        self.assertFalse(self.hit("见 https://x/releases/tag/v1.0.0 的说明"))

    def test_clean_prose_passes(self):
        self.assertFalse(self.hit("这条规则每月检查一次，还没发挥作用"))


class TestReleaseHelpers(unittest.TestCase):
    def test_bump_changelog_empty_unreleased_raises(self):
        """空 CHANGELOG 必须中止发版——不然会打出一个没有任何内容的 Release。"""
        changelog = "## [Unreleased]\n\n## [1.0.0] - 2026-10-31\n\nold\n"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as cm:
                release.bump_changelog(changelog, "1.0.1", "2026-11-01")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("[Unreleased] 是空的", buf.getvalue())

    def test_bump_changelog_promotes_body(self):
        changelog = "## [Unreleased]\n\n- 新加了一条\n\n## [1.0.0] - 2026-10-31\n\nold\n"
        out = release.bump_changelog(changelog, "1.0.1", "2026-11-01")
        self.assertIn("## [1.0.1] - 2026-11-01", out)
        self.assertIn("- 新加了一条", out)
        self.assertIn("## [Unreleased]\n\n## [1.0.1]", out, "应当留下空的 Unreleased")
        self.assertNotIn("## [Unreleased]\n\n- 新加了一条", out)

    def test_bump_readme_updates_badge_and_links(self):
        text = "![v](https://img.shields.io/badge/version-1.0.0-blue) 见 releases/tag/v1.0.0"
        out = release.bump_readme(text, "1.0.0", "1.0.1")
        self.assertIn("version-1.0.1-blue", out)
        self.assertIn("releases/tag/v1.0.1", out)

    def test_bump_skill_updates_metadata_only(self):
        text = 'metadata:\n  version: "1.0.0"\n'
        out = release.bump_skill(text, "1.0.0", "1.0.1")
        self.assertIn('version: "1.0.1"', out)

    def test_semver_rejects_bad_versions(self):
        for bad in ("v1.0.1", "1.0", "1.0.1-beta", "abc"):
            self.assertIsNone(release.SEMVER_RE.match(bad), bad)
        self.assertIsNotNone(release.SEMVER_RE.match("1.0.1"))

    def test_unreachable_remote_gives_friendly_error(self):
        """发版的人多半不看代码：连不上远端时，脚本必须友好报错退出而非抛堆栈。

        这里用 mock 模拟「git ls-remote 失败」，而不是真的去断网——
        真断网在 CI / 某些网络环境下不可复现，会让测试时绿时红。
        """
        fake = subprocess.CompletedProcess(
            args=["git", "ls-remote"], returncode=128, stdout="", stderr=""
        )
        with mock.patch.object(release, "sh", return_value=fake):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                with self.assertRaises(SystemExit) as cm:
                    release.remote_tag_exists("v9.9.9")
        self.assertEqual(cm.exception.code, 1)
        out = buf.getvalue()
        self.assertNotIn("Traceback", out, "不该把 Python 堆栈丢给不看代码的人")
        self.assertNotIn("CalledProcessError", out)
        self.assertIn("git remote -v", out, "要给出可执行的下一步")

    def test_remote_tag_exists_parses_stdout(self):
        """远端可达时，按 ls-remote 的真实输出判定 tag 是否存在（两个分支都要测）。"""
        present = subprocess.CompletedProcess(
            args=["git", "ls-remote"], returncode=0,
            stdout="abc123refs/tags/v1.1.0\n", stderr="",
        )
        absent = subprocess.CompletedProcess(
            args=["git", "ls-remote"], returncode=0, stdout="", stderr=""
        )
        with mock.patch.object(release, "sh", return_value=present):
            self.assertTrue(release.remote_tag_exists("v1.1.0"))
        with mock.patch.object(release, "sh", return_value=absent):
            self.assertFalse(release.remote_tag_exists("v1.1.0"))


class TestSyncSnapshots(unittest.TestCase):
    def test_linkify_keeps_chinese_readable(self):
        """务必保留中文原文：%E5%8D%8F... 这种编码人读不懂，也就没法核对。"""
        out = sync_snapshots.linkify_outside_code(
            "见 [01-foo](references/01-foo.md)", "1.0.1"
        )
        self.assertIn("blob/v1.0.1/references/01-foo.md", out)
        self.assertNotIn("%", out)

    def test_linkify_applies_prefix_for_english_package(self):
        out = sync_snapshots.linkify_outside_code(
            "见 [01-foo](references/01-foo.md)", "1.0.1", "docs/"
        )
        self.assertIn("blob/v1.0.1/docs/references/01-foo.md", out)

    def test_linkify_leaves_code_fences_alone(self):
        text = "```\n[01-foo](references/01-foo.md)\n```\n"
        self.assertEqual(sync_snapshots.linkify_outside_code(text, "1.0.1"), text)

    def test_linkify_skips_non_md_targets(self):
        """`docs/` 这类目录引用转成绝对 URL 会变成死链，必须跳过。"""
        out = sync_snapshots.linkify_outside_code(
            "见 [`docs/references/`](docs/references/)", "1.0.1"
        )
        self.assertIn("(docs/references/)", out)

    def test_normalize_ref_labels_shortens(self):
        out = sync_snapshots.normalize_ref_labels(
            "[`references/01-foo.md`](references/01-foo.md)"
        )
        self.assertEqual(out, "[01-foo](references/01-foo.md)")

    def test_frontmatter_keeps_author(self):
        src = '---\nname: spn\ndescription: d\nlicense: CC-BY-4.0\nmetadata:\n  author: xiaoyu-hue\n  version: "0.0.1"\n---\n\n# T\n'
        out = sync_snapshots.render_frontmatter(src, "spn-en", "1.0.1")
        self.assertIn("author: xiaoyu-hue", out)
        self.assertIn('version: "1.0.1"', out)
        self.assertIn("name: spn-en", out)

    def test_generation_is_idempotent(self):
        """连续两次生成必须完全一样，否则 --check 会把自己难住。"""
        for pkg in sync_snapshots.PACKAGES:
            first = sync_snapshots.build_skill(pkg["skill_src"], pkg, "1.0.1")
            second = sync_snapshots.build_skill(pkg["skill_src"], pkg, "1.0.1")
            self.assertEqual(first, second, pkg["name"])

    def test_missing_anchor_raises_instead_of_silent_skip(self):
        """锚点找不到就报错——静默跳过等于又一次留下不同步的副本。"""
        bad = {"title_from": "## X", "blockquote_from": "> Y", "tail_from": "Z"}
        with self.assertRaises(ValueError):
            sync_snapshots.apply_section_overrides("完全没有这些句子", bad)


class TestValidateSkills(unittest.TestCase):
    """重点是负例：一个只会输出 OK 的校验器毫无价值，必须证明它真的会拦。"""

    def make_pkg(self, tmpdir: str, dirname: str, **fields) -> str:
        pkg = os.path.join(tmpdir, dirname)
        os.makedirs(pkg, exist_ok=True)
        body = fields.pop("body", "正文内容需要足够长才会被认为是有用的技能，这里补足远远超过下限的字符数以保证它不会被空壳检查命中。" * 5)
        lines = ["---"]
        for k, v in fields.items():
            lines.append(f"{k}: {v}")
        lines += ["---", "", body]
        with open(os.path.join(pkg, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return pkg

    def check(self, tmpdir: str, dirname: str, **fields) -> list:
        pkg = self.make_pkg(tmpdir, dirname, **fields)
        return validate_skills.check_package(pkg, os.path.join(pkg, "SKILL.md"))

    def test_valid_package_passes(self):
        with tempfile.TemporaryDirectory() as d:
            problems = self.check(d, "good-one", name="good-one", description="当用户 X 时使用：做 Y")
            self.assertEqual(problems, [], problems)

    def test_reserved_word_caught(self):
        """name 含 claude / anthropic 会被官方上传校验拒绝——这是最容易踩的一条。"""
        with tempfile.TemporaryDirectory() as d:
            problems = self.check(d, "helper", name="claude-helper", description="x")
            self.assertTrue(any("保留词" in p for p in problems))

    def test_name_must_match_directory(self):
        with tempfile.TemporaryDirectory() as d:
            problems = self.check(d, "dir-a", name="different", description="x")
            self.assertTrue(any("不一致" in p for p in problems))

    def test_uppercase_name_caught(self):
        with tempfile.TemporaryDirectory() as d:
            problems = self.check(d, "BadCase", name="BadCase", description="x")
            self.assertTrue(any("小写" in p for p in problems))

    def test_description_limit_enforced(self):
        with tempfile.TemporaryDirectory() as d:
            problems = self.check(d, "long", name="long", description="A" * 1100)
            self.assertTrue(any("超出" in p for p in problems))

    def test_missing_description_caught(self):
        """description 决定 Agent 会不会加载它，缺了等于这个技能不存在。"""
        with tempfile.TemporaryDirectory() as d:
            problems = self.check(d, "nodesc", name="nodesc")
            self.assertTrue(any("description" in p for p in problems))

    def test_missing_frontmatter_caught(self):
        with tempfile.TemporaryDirectory() as d:
            pkg = os.path.join(d, "nofm")
            os.makedirs(pkg)
            path = os.path.join(pkg, "SKILL.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write("# 没有 frontmatter\n\n正文就是这里，没有任何元数据可言。")
            problems = validate_skills.check_package(pkg, path)
            self.assertTrue(any("frontmatter" in p for p in problems))

    def test_thin_body_caught(self):
        with tempfile.TemporaryDirectory() as d:
            problems = self.check(d, "thin", name="thin", description="x", body="太短了")
            self.assertTrue(any("太短" in p for p in problems))

    def test_skeleton_directory_is_exempt_from_name_match(self):
        """骨架目录下的 name 是占位符，本来就不该与目录同名。"""
        with tempfile.TemporaryDirectory() as d:
            problems = self.check(d, "_skeleton", name="your-skill-name", description="x")
            self.assertFalse(any("不一致" in p for p in problems))

    def test_repo_packages_are_valid(self):
        """真实包必须一直合规——这条挂了说明有人改坏了。"""
        pkgs = validate_skills.find_packages(["templates/skills", "skills"])
        self.assertGreaterEqual(len(pkgs), 6)
        problems = []
        for pkg, skill in pkgs:
            problems.extend(validate_skills.check_package(pkg, skill))
        self.assertEqual(problems, [], problems)


class TestCheckFacts(unittest.TestCase):
    def test_parses_all_registered_facts(self):
        rows = check_facts.parse_rows()
        self.assertGreaterEqual(len(rows), 10)
        for fact, value, date, source, period in rows:
            self.assertIsInstance(date, datetime.date)
            self.assertGreaterEqual(period, 1)

    def test_stale_detection_triggers_after_period(self):
        today = datetime.date(2027, 6, 1)
        self.assertEqual(len(check_facts.stale_rows(today)), len(check_facts.parse_rows()))

    def test_no_stale_rows_today(self):
        """当前登记表应当全部在复核周期内（FACTS.md 要保持更新）。"""
        self.assertEqual(check_facts.stale_rows(datetime.date.today()), [])


class TestScenarioGrader(unittest.TestCase):
    SCENARIOS = os.path.join(ROOT, "tests", "scenario-tests", "scenarios.json")
    TRANSCRIPTS = os.path.join(ROOT, "tests", "scenario-tests", "transcripts")

    def _grade(self, filename: str) -> dict:
        sc = run_scenarios.load_scenarios(self.SCENARIOS)
        sid = run_scenarios.stem_to_sid(os.path.splitext(filename)[0])
        scenario = run_scenarios.scenario_by_id(sc, sid)
        with open(os.path.join(self.TRANSCRIPTS, filename), encoding="utf-8") as f:
            return run_scenarios.grade(scenario, f.read())

    def test_compliant_answer_has_no_avoid_hits(self):
        """守规则的回答不应命中任何反面标记（评分器不能误杀）。"""
        r = self._grade("S01_compliant.md")
        self.assertEqual(r["avoid_hit"], [])

    def test_violation_answer_flags_avoid_hits(self):
        """违规回答必须被反面标记抓到（评分器不能当橡皮图章）。"""
        r = self._grade("S01_violation.md")
        self.assertGreater(len(r["avoid_hit"]), 0)

    def test_grader_matches_scenario_by_id_prefix(self):
        """文件名 S01_compliant 应匹配到场景 S01-附和（前缀匹配）。"""
        sc = run_scenarios.load_scenarios(self.SCENARIOS)
        self.assertIsNotNone(run_scenarios.scenario_by_id(sc, "S01"))


if __name__ == "__main__":
    verbosity = 2 if "-v" in sys.argv else 1
    result = unittest.main(exit=False, verbosity=verbosity).result
    print()
    if result.wasSuccessful():
        print(f"✓ 全部通过：{result.testsRun} 项")
        sys.exit(0)
    print(f"✗ 失败 {len(result.failures)} / 错误 {len(result.errors)}（共 {result.testsRun} 项）")
    sys.exit(1)
