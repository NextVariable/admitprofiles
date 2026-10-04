# 录取画像研究

第一版是可在 Codex 中使用的 `admission-intelligence` skill，源码位于 `skills/admission-intelligence/`。输入具体项目，研究公开录取／入学案例，归纳背景路径，并为学校专业、时间线、工作实习及申请表达提供出处。个人匹配只在用户要求且提供真实背景后执行。

调用示例：`使用 $admission-intelligence 研究 Northwestern MSIS，先确认具体项目，结论先行，给画像分类、代表案例和逐项来源，未公开的不要猜。`

源文件保存在本项目并由 Git 管理。本机安装位置为 `~/.codex/skills/admission-intelligence`，指向本项目 skill 目录；移动项目后需要更新链接。Codex 是否已在现有聊天刷新 skill 列表需另确认，新聊天可尝试名称调用，也可直接提供 SKILL.md 完整路径。

`research/cmu-miips/2026-10-05-pilot/` 是三个官方人物介绍的小样本人工核查。它验证的是规则应用示例，尚未完成全网项目研究，也没有证明不同 Agent 或不同项目的稳定效果。