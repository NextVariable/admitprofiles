# 维护与验证

辅助脚本仅依赖 Python 3.11+ 标准库。安装维护工具后，在仓库根目录执行：

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

项目原创代码、技能规则与文档采用 [MIT 许可证](LICENSE)。第三方网页摘录与其他引用材料不因收录而获得重新授权，保留原权利归属与来源。

---

# Maintenance and validation

Helper scripts use only the Python 3.11+ standard library. Install maintenance tools and run the commands in the Chinese section from the repository root. Routine checks cover skill helpers, current research and recorded model outputs. Run historical record and source-audit checks separately using the archive commands above.

Structural validation does not establish source truth. Regrading recorded outputs is not a fresh model run. When evidence rules change, add regressions for demonstrated errors and verify behavior through an actual research query.

Keep installable rules in `skills/`, current examples in `research/`, and superseded versions in `archive/`. Update the research index when examples change. Independent drafts are not final reports. Interpret historical relative paths against the original directory layout; audit inventories retain original paths and hashes.

[Architecture](docs/architecture.md) · [Evaluation scope](evals/README.md) · [Archive](archive/README.md)

Original code, skill rules and documentation are covered by the [MIT License](LICENSE). Inclusion does not relicense third-party excerpts or other quoted material; retain original rights and sources.

---

## MIT 许可证中文说明 / MIT License explained in Chinese

MIT 允许使用、复制、修改、合并、发布、分发、再授权及销售项目原创代码与文档，包含商业用途。复制或分发全部或重要部分时，须保留版权声明与许可声明；不要求修改后的代码继续开源。软件按现状提供，不作保证。正式条款以 [LICENSE](LICENSE) 中的英文原文为准；本段仅作中文说明。第三方引用材料不在项目重新授权范围内。

MIT permits use, copying, modification, merging, publication, distribution, sublicensing and sale of original project code and documentation, including commercial use. Retain the copyright and permission notices in copies or substantial portions. Modified code need not be open sourced. The software is provided as is, without warranty. The English text in [LICENSE](LICENSE) contains the formal terms; the Chinese paragraph is explanatory. Third-party quoted material is not relicensed by this project.
