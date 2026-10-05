# 同题重复会话验证

先冻结32道合成证据判断题及参考标准，再向四个新会话分发同一packet，不提供oracle或其他输出。调度时分别请求gpt-6-astra/high与gpt-6-sol/high，各两次，fork_turns=none；另保存继承模型同一上下文两次重复作补充。四个独立会话128判断、两次同上下文64判断，均与冻结标准一致。主审抽读每份T02/T09/T25/T29/T31理由，核对入学日期、区间并集、准入分母、停止条件及申请边界。

工具接受了型号请求，但执行端未暴露可独立核验的实际部署型号；这些只能称“按两种型号请求执行的重复会话测试”，不能称已证实两种实际模型完成对照，不能作模型排名。调用条件、请求型号与这项限制记录于execution.json；原输出逐份保留。

题包是显式使用skill的合成判断，不包含真实网页检索、隐式触发、自由生成长报告或完全背景还原。题目有明显规则边界，32/32不能推广为实际研究100%正确，更不能称skill完美。三份真实盲搜和CMU主审研究在research；冻结后仍发现本科专业错误，正说明合成题成绩不能替代来源审阅。

运行python3 tests/check_decisions.py evals/decision-benchmark/2026-10-05重现results.json；脚本检查输入哈希、题号集合、重复遗漏和yes/no一致性，不自动裁定理由的全部语义。

维护更新：评分入口移至tests，按execution.json要求全部运行输出存在。错误答案与缺失输出均返回失败；原汇总脚本保留archive。

---

# Repeated-session validation on a fixed packet

Freeze 32 synthetic evidence decisions and reference answers before distributing the same packet to four fresh sessions, without the oracle or other outputs. Dispatch requested `gpt-6-astra/high` and `gpt-6-sol/high` twice each with `fork_turns=none`; two same-context repetitions using the inherited model were also retained. All 128 independent-session decisions and 64 same-context decisions matched the frozen reference. The reviewer sampled reasons for T02/T09/T25/T29/T31 in each output, checking enrollment dates, interval unions, admission denominators, stopping conditions and pre-application boundaries.

The tool accepted model requests, but the execution environment did not expose independently verifiable deployed model identities. These are repeated sessions requested under two model labels, not a verified comparison of two deployed models or a model ranking. `execution.json` records conditions, requested models and this limitation; original outputs are retained.

The packet explicitly invokes the skill and uses synthetic decisions. It does not test real web retrieval, implicit invocation, unrestricted long reports or complete background reconstruction. Obvious rule boundaries mean 32/32 cannot imply 100% real-research accuracy or a perfect skill. Three blind web-search runs and the lead reviewer's CMU research are in `research/`. An undergraduate-major error discovered after freezing illustrates why synthetic scores do not replace source review.

Run `python3 tests/check_decisions.py evals/decision-benchmark/2026-10-05` to reproduce `results.json`. The checker validates input hashes, the question-ID set, duplicates, omissions and yes/no agreement; it does not automatically judge all reasoning semantics.

The grading entrypoint now lives in `tests/` and requires every output listed in `execution.json`. Wrong answers and missing outputs fail. The original summary script remains in the archive.
