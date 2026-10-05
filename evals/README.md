# 模型评估

[固定判断题包](decision-benchmark/2026-10-05/README.md)保存32道证据边界题、运行清单、原始回答和评分。四个独立会话与两次同上下文重复均匹配参考标准；实际模型部署型号无法独立核验，不能据此进行模型排名。

执行 `python3 tests/check_decisions.py evals/decision-benchmark/2026-10-05` 可重评分。缺失运行、重复题号、错误答案或题包哈希变化会返回失败。持续验证运行同一命令，避免只展示历史通过记录。

这些合成判断不测联网检索、隐式触发或长报告质量。真实查询示例见[研究索引](../research/README.md)，历史评估与来源审计见[档案](../archive/README.md)。

---

# Model evaluations

The [fixed decision packet](decision-benchmark/2026-10-05/README.md) includes 32 evidence-boundary questions, an execution manifest, raw answers and grading results. Four independent sessions and two same-context repetitions matched the reference answers. Actual deployed model identities could not be independently verified, so these results do not support a model ranking.

Run `python3 tests/check_decisions.py evals/decision-benchmark/2026-10-05` to regrade. Missing runs, duplicate question IDs, wrong answers or packet-hash changes produce failure. Continuous validation runs the same command rather than relying only on historical pass records.

Synthetic decisions do not test web search, implicit invocation or long-report quality. See [research examples](../research/README.md) for actual queries and the [archive](../archive/README.md) for historical evaluations and source audits.
