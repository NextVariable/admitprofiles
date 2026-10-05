# AdmitProfiles · 录取背景查询

[![验证状态](https://github.com/NextVariable/admitprofiles/actions/workflows/validate.yml/badge.svg)](https://github.com/NextVariable/admitprofiles/actions/workflows/validate.yml)

**输入学校和项目，查真实录取者的学校、专业、工作与实习背景。**

一个用于 Codex 的查询技能。按你的问题检索官网、个人履历和申请社区，整理具体案例并附上来源；也可以结合你的真实经历，分析与已观察路径的联系和差异。

## 这样问

```text
使用 $admitprofiles 查 Berkeley MDevEng 最近三届录取者的背景。
重点看本科学校和专业、工作年限、实习经历，附上每项来源。
```

也可以问：“这个项目有没有非理工背景的录取案例？”或“帮我查有三年以上工作经验的人走了什么申请路径。”

你会得到有出处的案例、背景对照和仍未查到的信息。[查看一份查询结果 →](research/berkeley-mdeveng/2026-10-05-cohort-review/report.md)

公开案例不代表全体录取者，也不能直接推算你的录取概率。

## 安装

需要 Codex 和联网检索能力；记录检查工具需要 Python 3.11+。先克隆仓库，再将技能链接到个人技能目录：

```sh
git clone https://github.com/NextVariable/admitprofiles.git
cd admitprofiles
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/skills/admitprofiles" "$HOME/.agents/skills/admitprofiles"
```

若已有同名安装，请先保留旧版本。安装后在新会话中使用。

[更多查询示例](research/README.md) · [维护与测试](CONTRIBUTING.md)

项目原创代码与文档采用 [MIT 许可证](LICENSE)。引用的第三方材料保留原权利归属。
