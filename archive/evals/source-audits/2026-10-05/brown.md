# Brown PRIME 既有版本逐字段来源审计（2026-10-05）

清单基准提交 `7c0e6f071a455418267a20ff7ef2b468862bbf86`；共 170 个不可合并的版本/主张单位，已输出 170 行逐条判定。结果：{'supported': 84, 'inaccessible': 13, 'unknown_preserved': 72, 'overstated': 1}。审计 JSON 每行保留原 unit_id、原主张、判定、核过的 URL 与具体定位；同一来源只重开一次，但各版本的字段仍逐条映射。当前 agent 只能确认 GPT-6 家族，运行环境未提供精确部署型号；没有调用外部第二模型。

重开了库存中的 10 个不同 URL：9 个 Brown 官方页面可读；Reddit 原帖 `1saytir` 直接打开返回 cache miss，old.reddit 版本不可访问，.json 版本亦 cache miss。搜索结果仍可见 2026-04-03 日期和 Brown PRIME accepted 摘要，但无法独立复核作者名和完整上下文。故 Reddit 原帖的旧 `full_text` 记录标为 inaccessible，而非断言历史访问是假的。仅索引日期的 `snippet_only` 元数据可作为有限二手线索。

最明确的超证据是独立初稿将 Joseph D. 的 `wanted in-resident` 记为实际 `track=residential`；官网人物页第40-41行只证明偏好，后续最终稿改为 `track=unknown`、另存 `format_preference`，这一修正成立。Chinmay S. 的 `Class of '22` 联合 alumnus 只能说明届别及现在为校友；旧记录以 `cohort_label=2022`、`exact_completion=null` 明确保留授位日期未知，所以该行判 supported。Megan 的2019本科与2022已有硕士、海军2019-05起任职和本科CWEP均有官网第37-44行；没有申请日期便不能推精确申请前年限。Lily 本科末年镜片原型在入学前，Haunani/NASA/黑客松在读期间，不得回填申请背景。

前测最终稿及独立初稿都明确不是三届完整研究，这一范围自限得到文件文本支持。最终稿有关“重开 Reddit 原帖”的过程主张今天不可重演；本次审计无法把当前拒绝访问倒推为旧报告未曾访问。范围测试中 Marco 是2019历史人物，Chinmay为'22届，Lily为'26届新毕业生，三人都没有被证实为2024、2025、2026某个个人入学年度。官网 FAQ 第33及82-100行、Format 页第113-121行存在内部年份矛盾，旧版记录冲突而未替个人补日期的做法成立。官方FAQ第130-131行用“primarily”描述STEM背景并举经济、商科、工业设计完成者，不能改写成只录STEM。

库存中 unknown/null 的字段逐项以 `unknown_preserved` 保存。它们不是零工作、未录取或某届缺席的证据。人物页和报告的事实大多能直接定位，但这组旧版本没有覆盖三年逐年正式入学样本；新盲搜亦未找到可打开正文同时给出个人入学年的人物，因此不能计算逐届分布。
