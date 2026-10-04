# Admission Intelligence · 录取画像研究

[![验证状态](https://github.com/NextVariable/admission-intelligence/actions/workflows/validate.yml/badge.svg)](https://github.com/NextVariable/admission-intelligence/actions/workflows/validate.yml)

一个用于 Codex 的研究技能：从公开录取与入学案例中还原申请前背景，归纳有出处的经历路径。输入学校和项目即可开始；用户提供真实履历并要求匹配时，再补充个人定位。

它将学校、专业、工作与实习、时间线和申请表达逐项连接到来源，保留未知、冲突及访问限制。公开案例能说明某条路径曾经出现，不能用于推算录取概率或解释录取原因。

## 开始使用

先将仓库克隆到固定位置：

```sh
git clone https://github.com/NextVariable/admission-intelligence.git
cd admission-intelligence
```

私有仓库需要具有访问权限的 GitHub 账号。按 [Codex 官方安装目录说明](https://learn.chatgpt.com/docs/build-skills)，在 macOS／Linux 上，将技能链接到 Codex 的个人技能目录；目标已存在时，先保留原版本，避免覆盖：

```sh
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/skills/admission-intelligence" "$HOME/.agents/skills/admission-intelligence"
```

也可将 `skills/admission-intelligence` 整个目录复制到自己的技能目录（已有 `~/.codex/skills` 安装可以继续使用，避免重复安装同名技能），无需复制研究与测试资料。移动仓库后需更新链接；新会话中确认技能已被发现。

```text
使用 $admission-intelligence 研究 Northwestern MSIS。
先确认具体项目，给出画像分类、代表案例和逐项来源。
未公开的不要猜，说明年份和渠道覆盖的缺口。
```

## 交付内容

完整研究保存 `report.md`、`cases.json` 和 `search-log.md`：报告说明观察到的背景路径与结论边界，证据记录保存逐字段出处，检索记录说明渠道覆盖与停止原因。有限研究会明确缺失年份、渠道和字段，不把小样本描述为完整画像。

可以先阅读 [Northwestern MSIS 修正版报告](research/northwestern-msis/2026-10-05-delivery-review/report.md)，或通过 [研究索引](research/README.md)选择其他案例。现有报告均为有限验证产物，尚未完成最近三个入学年级的全面覆盖。

例如，Northwestern 的官方历史人物稿可以确认 Austin Olson 在线攻读 MSIS，却不能将其 pre-med 学习经历补写为已完成的本科专业，也不能将 2013—2021 的军旅区间算成八年申请前全职工作。修正版保留三个正文身份案例，把仅摘要的论坛自报放进检索线索；这体现了本技能对“查到了什么”的实际约束。

## 验证与边界

辅助工具仅依赖 Python 3.11 或更新版本的标准库：

```sh
python3 -m unittest discover -s tests -v
python3 tests/check_records.py
```

当前 67 项回归测试覆盖结构、引用、日期、独立安装和包内资源，批量检查包含 752 种嵌套输入变异、5,000 组随机工作区间、25,350 组跨年区间穷举及 200 组既有对照。穷举同时核对调换顺序与重复区间不会增加年限。GitHub Actions 在 Python 3.11、3.12、3.13、3.14 上运行回归与记录检查。实际运行证据见 [第五轮验证](docs/history/第五轮交付复核-2026-10-05.md)。批量测试数量不是实际录取研究数量，也不是模型输出正确率。

`validate_cases.py` 检查记录结构与引用一致性；`work_months.py` 计算已提供月级日期区间的并集。两者均不验证网页真实性、正文支持性或模型研究质量。人工来源复查与独立研究试运行的证据见 [评估说明](evals/README.md)和 [历史验证记录](docs/history/README.md)。旧版 1.0 记录保留并明确跳过新版结构检查；独立初稿保留供审计，不应作为最终报告引用。

直接检查自己的记录时，可在仓库根目录运行 `python3 skills/admission-intelligence/scripts/validate_cases.py <cases.json>`；该命令只报告结构和引用结果。维护者规范与项目架构见 [贡献指南](CONTRIBUTING.md)和 [架构说明](docs/architecture.md)。

## 仓库结构

可安装的技能与辅助脚本位于 [skills/admission-intelligence](skills/admission-intelligence/SKILL.md)，研究材料位于 [research](research/README.md)，可执行自动回归位于 [tests](tests)，独立评估及历史日志位于 [evals](evals/README.md)，设计与历次修正记录位于 [docs/history](docs/history/README.md)。运行时不依赖研究存档或测试日志。