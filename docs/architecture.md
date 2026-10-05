# 架构

这是单一查询技能，安装单元是 `skills/admitprofiles`。它包含入口、按需读取的证据规则和两个标准库辅助脚本；无需安装整个研究档案。

| 目录 | 用途 |
| --- | --- |
| `skills/` | 可安装的技能、规则与辅助脚本 |
| `research/` | 当前查询示例，每个项目一个最新版本 |
| `tests/` | 回归测试与维护检查工具 |
| `evals/` | 可重跑的模型判断题包与输出 |
| `archive/` | 历史研究、初稿、审计与开发日志 |
| `.github/workflows/` | 持续验证 |

记录校验器先检查结构，再检查来源与案例关系；月级计算器只合并已有时间区间。二者不负责搜索网页或裁定网页是否支持结论。保留独立CLI，避免为少量共同代码引入安装依赖。

日常回归使用小型自包含输入，历史审计单独运行。审计检查器接受目录和证据根目录，不依赖固定日期或项目名；模型评分器读取运行清单，缺失输出或错误答案均返回失败。

详细开发过程保存在[历史索引](../archive/README.md)。

---

# Architecture

This is a single research skill. Its installation unit is `skills/admitprofiles`, containing an entrypoint, references loaded when needed and two standard-library helpers. Installing the research archive is unnecessary.

| Directory | Purpose |
| --- | --- |
| `skills/` | Installable skill, rules and helpers |
| `research/` | Current examples, one latest version per program |
| `tests/` | Regression tests and maintenance checkers |
| `evals/` | Repeatable decision packets and recorded model outputs |
| `archive/` | Historical research, drafts, audits and development logs |
| `.github/workflows/` | Continuous validation |

The record validator checks structure before source and case relationships. The month calculator merges supplied intervals. Neither searches the web or decides whether a page supports a claim. Both remain standalone CLIs rather than adding installation dependencies for a small amount of shared code.

Routine regression tests use small, self-contained inputs; historical audits run separately. The audit checker accepts audit and evidence-root directories without depending on a fixed date or program. The model grader reads the execution manifest and fails on missing outputs or incorrect answers.

Development history is available in the [archive index](../archive/README.md).
