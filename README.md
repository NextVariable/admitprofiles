# AdmitProfiles · 录取背景查询 / Admitted Applicant Background Research

[![验证状态 / Validation](https://github.com/NextVariable/admitprofiles/actions/workflows/validate.yml/badge.svg)](https://github.com/NextVariable/admitprofiles/actions/workflows/validate.yml)

**输入学校和项目，查真实录取者的学校、专业、工作与实习背景。**
**Enter a school and program to research admitted applicants’ education, work and internship backgrounds.**

一个用于 Codex 的查询技能。检索官网、个人履历和申请社区，整理案例并附来源；也可结合你的真实经历，分析与已观察路径的联系和差异。

A research skill for Codex. Search official pages, public profiles and applicant communities for sourced cases. With your actual background, it can also compare your experience with observed paths.

## 这样问 / Example

```text
使用 $admitprofiles 查 Berkeley MDevEng 最近三届录取者的背景。
重点看本科学校和专业、工作年限、实习经历，附上每项来源。

Use $admitprofiles to research the three most recent entering cohorts of Berkeley MDevEng.
Focus on undergraduate institutions and majors, work experience and internships. Cite each finding.
```

也可以问：“有没有非理工背景的录取案例？”或“有三年以上工作经验的人走了什么申请路径？”

You can also ask: “Are there admitted applicants from non-STEM backgrounds?” or “What application paths have people with over three years of work experience taken?”

你会得到有出处的案例、背景对照和仍未查到的信息。[查看查询结果 / View an example →](research/berkeley-mdeveng/2026-10-05-cohort-review/report.md)

Receive sourced cases, background comparisons and explicit information gaps. Existing research reports are in Chinese.

公开案例不代表全体录取者，也不能直接推算你的录取概率。
Public cases do not represent all admitted applicants or establish your admission probability.

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
