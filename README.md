# AdmitProfiles · 录取画像研究 / Admission Profile Research

[![验证状态 / Validation](https://github.com/NextVariable/admitprofiles/actions/workflows/validate.yml/badge.svg)](https://github.com/NextVariable/admitprofiles/actions/workflows/validate.yml)

**输入一个留学项目，跨渠道研究真实录取与入学案例，归纳背景画像，帮助你判断项目匹配与申请定位。**
**Research real admission and enrollment cases across sources, identify background patterns, and use the evidence to inform program fit and applicant positioning.**

AdmitProfiles 是一个用于 Codex 的录取画像研究技能。从官网、LinkedIn、本人公开履历和申请社区等渠道寻找案例，先回答“这个项目出现过哪些背景路径”，再给出具体人物的学校、专业、入学与毕业时间、申请前工作年限、实习经历及公开申请路线。每个关键事实和画像判断都附可核查的依据，未公开的信息明确保留。

AdmitProfiles is a research skill for Codex. It searches official pages, LinkedIn, public résumés and applicant communities to identify observed background paths, then presents representative cases with education, dates, pre-application work experience, internships and publicly shared application approaches. Key facts and interpretations carry reviewable sources; missing information stays explicit.

结合你提供的真实经历，可以进一步分析你与已有路径的联系、需要补足的证据，以及有依据的差异化表达，帮助你理解该申请什么项目、应该突出哪些经历。个人匹配与定位能力仍在完善，不保证每个项目都能找到充分案例或得出明确分类。

With your actual experience, it can also examine connections to observed paths, evidence gaps and credible ways to differentiate your application. Personal fit and positioning are still being refined; sufficient cases or clear categories are not guaranteed for every program.

## 这样问 / Example

```text
使用 $admitprofiles 研究 Berkeley MDevEng 最近三届的录取画像。
结论先行，归纳有证据的背景路径，给代表案例的学校、专业、
入学毕业时间、申请前工作年限、实习和公开申请路线，逐项附来源。
样本不足时不要强行分类。

Use $admitprofiles to research admission profiles for the three most recent
entering cohorts of Berkeley MDevEng. Lead with findings, identify evidenced
background paths, and provide representative cases with education, dates,
pre-application work, internships and public application approaches.
Cite each finding; do not force categories when evidence is insufficient.
```

也可以问：“有没有非理工背景的录取案例？”或提供自己的履历后问：“我的经历与哪些路径相近？有什么证据缺口，哪些经历值得突出？”

You can also ask: “Are there admitted applicants from non-STEM backgrounds?” With your résumé: “Which observed paths relate to my experience, what evidence is missing, and what should I emphasize?”

你会得到有出处的背景路径、代表案例、背景对照和信息缺口。现有[研究示例 / Research example →](research/berkeley-mdeveng/2026-10-05-cohort-review/report.md)展示了案例核查与未知项处理；该项目样本尚不足以支持稳定画像分类，也未演示完整个人定位。

Outputs include sourced background paths, representative cases, comparisons and information gaps. Existing reports are in Chinese. The linked example demonstrates case verification and explicit unknowns; it does not establish stable profile categories or demonstrate complete personal positioning.

公开案例不代表全体录取者，背景路径不是招生公式，也不能直接推算你的录取概率。公开申请复盘与实际文书分开；没有文书证据时，不猜测某个人如何包装自己或为何被录取。

Public cases do not represent all admitted applicants. Observed paths are not admission rules or individual admission probabilities. Public retrospectives are distinguished from actual application essays; missing essays do not justify invented narratives or admission causes.

## 安装 / Installation

需要 Codex 和联网检索能力；记录检查工具需要 Python 3.11+。克隆仓库，再将技能链接到个人技能目录。

Requires Codex and web research tools; record validation requires Python 3.11+. Clone the repository and link the skill to your personal skills directory.

```sh
git clone https://github.com/NextVariable/admitprofiles.git
cd admitprofiles
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/skills/admitprofiles" "$HOME/.agents/skills/admitprofiles"
```

若已有同名安装，请先保留旧版本。安装后在新会话中使用。
Preserve any existing installation with the same name. Use the skill in a new session after installation.

[更多查询示例 / More examples](research/README.md) · [维护与测试 / Maintenance and tests](CONTRIBUTING.md)

项目原创代码与文档采用 [MIT 许可证 / MIT License](LICENSE)。引用的第三方材料保留原权利归属。
Original code and documentation are MIT licensed. Third-party quoted material retains its original rights.
