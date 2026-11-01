# PR 说明

## 改了什么
<!-- 一句话概括 -->

## 为什么
<!-- 对应哪类真实问题 / 哪个 issue -->

## 落在哪一层
- [ ] 通用层（`AGENTS.md` / `SKILL.md` / `references/`）
- [ ] 英文镜像（`docs/`）
- [ ] 技能包（`skills/`）
- [ ] 个人层（`personal/`）
- [ ] 仓库治理（许可证 / CI / 脚本 / 模板）

## 同步自检（改了规则就必须过）
> 根目录是唯一规范源，`docs/` 与 `skills/` 是会自动生成的发布副本，不要直接编辑。

- [ ] 我只改了规范源，没有直接编辑发布副本
- [ ] 改了 `AGENTS.md` / `SKILL.md` → 已跑 `python3 scripts/sync_snapshots.py --apply`
- [ ] 改了中文 `references/` → 英文版（如需要）已同步

```bash
python3 scripts/run_tests.py
python3 scripts/sync_snapshots.py --check
python3 scripts/doc_lint.py
python3 scripts/check_links.py
python3 scripts/check_facts.py
```

## 内容自检
- [ ] 没有把同一段内容重复写多遍（去重约定）
- [ ] 时效性数据（调研数字 / 额度 / 价格）已登记进 `FACTS.md`，没有散落在文档里
- [ ] 改动了 `scripts/` 就补了对应的测试
- [ ] 如涉及安全红线，已先开 issue 对齐

## 验证证据
<!-- 按 AGENTS.md 的交付格式：跑了哪条命令，输出是什么 -->
