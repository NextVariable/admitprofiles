# 架构

这是单一查询技能，安装单元是 `skills/admission-intelligence`。它包含入口、按需读取的证据规则和两个标准库辅助脚本；无需安装整个研究档案。

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

结构采用 [Agent Skills规范](https://agentskills.io/specification)和[OpenAI skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md)中的简洁入口、按需参考和可独立安装原则。没有加入当前用不到的插件框架或空目录。

详细开发过程保存在[历史索引](../archive/README.md)。
