# 维护与验证

运行时仅依赖 Python 3.11+ 标准库。安装维护工具后，在仓库根目录执行：

```sh
python3 -m pip install -r requirements-dev.txt
ruff check .
ruff format --check .
python3 -m unittest discover -s tests -v
python3 tests/check_records.py
python3 tests/check_decisions.py evals/decision-benchmark/2026-10-05
```

日常检查覆盖技能工具、当前研究与固定模型输出。历史证据独立检查：

```sh
python3 tests/check_records.py --root archive/research
python3 tests/check_source_audit.py archive/evals/source-audits/2026-10-05 --records-root archive
```

结构检查不证明来源真实，固定输出重评分也不等于重新运行模型。变更证据规则时，应增加针对实际错误的回归，并做真实查询复核。

技能规则留在 `skills/`，当前示例留在 `research/`，过时版本移入 `archive/`，原内容保留。更新示例后同步研究索引，不把独立初稿当正式结果。历史文件中的原始相对路径按归档前目录解释；审计清单保留原路径与哈希。

[架构说明](docs/architecture.md) · [评估范围](evals/README.md) · [历史档案](archive/README.md)

仓库尚未声明开源许可证；源码可访问不代表获得再分发授权。
