# 诱导场景测试（SPN 的「证明自己有效」机制）

所有 AGENTS.md 类项目都面临同一个质疑：**都说自己有效，没人能证明。** 这个目录就是 SPN 的回答——把核心规则变成可以跑的「诱惑性对话」，看 AI 守没守规则。

## 为什么只有人适合做这件事

判卷不需要懂代码，只需要读对话、判断「该问的问了没、该说的风险说了没」。这恰恰是零基础作者比工程师占优的地方：你不会被「技术上能实现」带偏，而会盯住「该不该这么做」。

## 怎么用

```bash
# 1. 看看有哪些场景
python3 run_scenarios.py scenarios.json

# 2. 挑一个场景，把它的 user_prompt 丢给任意 AI，把完整回答存成 transcripts/S01_compliant.md
#    （文件名带场景 id 即可：S01_xxx.md 只对照场景 S01，避免串场）

# 3. 跑评分器看观测结果
python3 run_scenarios.py scenarios.json transcripts/S01_compliant.md
python3 run_scenarios.py scenarios.json transcripts/        # 一次评全部
```

## 评分器只观测，不定罪

- `expect` 标记 = 守规则时大概率出现的词；`avoid` 标记 = 违反时大概率出现的词。
- 输出只是「命中了哪些标记」，最终是否守规则由**你读对话**判定。
- 脚本永远 exit 0，**不会**因为它觉得没守住就阻塞 CI——避免 LLM 判定的不确定性反噬整个流程。

## 当前覆盖

10 条核心规则：一味附和 / 服务端权限 / 不可逆确认 / 不编造 / 三视角 / 调试三步 / 不写死数字 / 边界声明归人 / 交付诚实 / 术语翻译。

> 想扩充：在 `scenarios.json` 的 `scenarios` 数组里加一条，字段照抄现有即可。`transcripts/` 下补一份对应回答就能加入回归。
