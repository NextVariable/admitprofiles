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

可以先阅读 [Berkeley 最近三届研究](research/berkeley-mdeveng/2026-10-05-cohort-review/report.md)，或通过 [研究索引](research/README.md)查看四个项目的最新版本。本轮已执行2024、2025、2026入学范围的三类渠道检索与停止条件：Berkeley核实10个有入学年份的公开人物，CMU补出2025与2026明确入学记录；Brown与Northwestern个人入学年份仍缺正文证据。检索工作完成不代表全班覆盖。

例如，官网届别不能倒推入学日期，迎新观察日不能当个人开学日；“财经与管理基础”不能升级为正式本科专业。新版保留这些区别、访问限制与未知，旧稿完整保留供复核。

## 验证与边界

辅助工具仅依赖 Python 3.11 或更新版本的标准库：

```sh
python3 -m unittest discover -s tests -v
python3 tests/check_records.py
python3 tests/check_source_audit.py
```

当前 72 项回归测试覆盖结构、引用、日期、独立安装和包内资源，批量检查包含 752 种嵌套输入变异、5,000 组随机工作区间、25,350 组跨年区间穷举及 200 组既有对照。穷举同时核对调换顺序与重复区间不会增加年限。GitHub Actions 在 Python 3.11、3.12、3.13、3.14 上运行回归与记录检查。最近运行证据见 [第六轮验证](docs/history/第六轮完成验证-2026-10-05.md)。批量测试数量不是实际录取研究数量，也不是模型输出正确率。

`validate_cases.py` 检查记录结构与引用一致性；`work_months.py` 计算已提供月级日期区间的并集。两者均不验证网页真实性、正文支持性或模型研究质量。全部旧记录已完成 [703条来源审计](evals/source-audits/2026-10-05/README.md)，309条有支持、17条过度主张、33条当前无法复核、344条保留未知，计数含历史版本重复。新版本已应用修正，历史原件哈希也进入持续检查。人工来源复查与独立研究试运行的证据见 [评估说明](evals/README.md)和 [历史验证记录](docs/history/README.md)。旧版 1.0 记录保留并明确跳过新版结构检查；独立初稿保留供审计，不应作为最终报告引用。

直接检查自己的记录时，可在仓库根目录运行 `python3 skills/admission-intelligence/scripts/validate_cases.py <cases.json>`；该命令只报告结构和引用结果。维护者规范与项目架构见 [贡献指南](CONTRIBUTING.md)和 [架构说明](docs/architecture.md)。

## 仓库结构

可安装的技能与辅助脚本位于 [skills/admission-intelligence](skills/admission-intelligence/SKILL.md)，研究材料位于 [research](research/README.md)，可执行自动回归位于 [tests](tests)，独立评估及历史日志位于 [evals](evals/README.md)，设计与历次修正记录位于 [docs/history](docs/history/README.md)。运行时不依赖研究存档或测试日志。