# 维护与验证

修改技能时保持默认任务为项目公开录取画像研究。新增规则应针对已观察到的失败或明确用户要求，不将单次案例固化成全局流程。通用流程保留在 SKILL.md，条件细节放入 references 并注明读取时机。

Python 运行时只依赖标准库，Ruff 是维护工具。使用 Python 3.11+，在自己的虚拟环境中安装 `requirements-dev.txt` 后运行：

```sh
ruff check .
ruff format --check .
python3 -m unittest discover -s tests -v
python3 tests/check_records.py
python3 tests/check_source_audit.py
```

提交前核对差异、包内引用和从独立目录执行的行为；校验器结构通过不代表网页支持结论。新增研究保留报告、证据和检索记录，修正版使用独立目录，并更新 research/README.md。禁止覆盖独立初稿或旧研究以掩盖修正。

自动测试代码放在 tests，人工／模型评估与原始日志放在 evals，设计历史放在 docs/history。评估应明确输入、执行条件、实际产物、失败与修正；不把未执行的验收计划列为通过。项目没有宣布开源许可证，贡献规范不授予再分发权限。

架构依据与本次整理的范围见 [架构说明](docs/architecture.md)。
