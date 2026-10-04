本次独立试运行只能给出有限研究：已确认 Brown PRIME 为工程学院的 Innovation Management and Entrepreneurship 理学硕士 ScM，有 residential 与 fully online 两种模式。四个已记录身份中，三人有官方 PRIME 身份与本科学校专业，另一人是搜索缓存所指 2026 申请季的论坛 offer 自报。个人确切入学年份全部未核实，因此没有完成 2024、2025、2026 最近三个已入学年级的分层研究，也不能称三届录取画像。三位官网人物只作为届别明确、入学年未知的历史补充。GPA、本科入学时间、精确申请前工作年限和文书原文均缺失；未形成稳定分类或比例。[项目官网](https://prime.brown.edu/)

已观察到的路径包括 UCF 电气工程本科及同校已有硕士、产业在职后继续学习；UC Davis 管理经济学本科进入创业方向；West Point 系统工程本科通过 Technical Scholar Program 获得申请研究生的机会。这些是单人路径，不是招生偏好。官网访谈中的项目选择动机也不是 SOP 内容。

[Megan D. 的官方访谈](https://prime.brown.edu/people/megan-d)明确记载 UCF 电气工程学士 2019 年、硕士 2022 年，在本科期间参与 Lockheed Martin 的兼职 CWEP，并自述从 2019 年 5 月起全职任职美国海军。她在访谈时已参加 PRIME 第二学期，网页标 Class of '25；它没有直接提供入学年或授予 PRIME 学位的确认，不能把当前日期或届别补成已经毕业。任职起点虽明确，申请日期和硕士入学日期缺失，故未计算申请前工作年限，也未推断线上轨道。她本科期间创办国防咨询企业的叙述可作为创业线索，但有限时间内未追加该经历的时间字段。

[Joseph D. 官方访谈](https://prime.brown.edu/people/joseph-d)记载 UC Davis 的 Managerial Economics 本科学位，并表示希望选择一年制、住校项目。网页标 Class of '24，介绍其实际 PRIME 体验；可以记录曾在读，尚未找到明确毕业授位文字、确切入学年、GPA或申请前雇佣经历。

[Jacob F. 官方访谈](https://prime.brown.edu/people/jacob-f)记载 West Point Systems Engineering 本科及 Regional Studies-Europe 辅修、Class of '24，以及 Technical Scholar Program 的申请机会。官网把其列入校友 spotlight，访谈讨论 PRIME，但具体访谈日期和入学日期未公开；保留曾在读状态，未直接认定已毕业或零工作经验。他期待参与 PRIME@Work，并不能据此把项目内实习记为申请前背景。

[Reddit 原帖](https://www.reddit.com/r/gradadmissions/comments/1saytir/2025_grad_struggling_to_find_a_job_already/)作者 Plenty-Initiative-49 自报 Brown PRIME accepted；搜索缓存显示帖期2026年4月3日，正文仅显示相对时间，精确发布日期未经正文核实；在 UTD PhD 结果下表示自己在那里读本科，标题称 2025 年毕业。本科专业未明确，不能从其申请 CS 硕士/博士反推。该记录属于 offer 自报，未确认接受 offer 或入学，独立于已入学样本，也没有联系匿名账号与任何实名人物。

官网范围也有需要保留的矛盾：[Format 页面](https://prime.brown.edu/format-resources)的 Class of 2028 标题写 summer 2026，但表格写 summer 2027；[FAQ](https://prime.brown.edu/faqs)的 Class of 2027 / September 2026、Class of 2028 / summer 2025 标注又不一致。此次未解决这些官网日期矛盾，因此没有把其中任何一项作为确定入学日期。官网 Class of 2022、2023、2024 的合并本科统计属于旧届官方汇总，不能替代最近三届的人物背景分母。

实际覆盖了官网、本人履历检索、申请论坛三个渠道；本人 LinkedIn 三页直接打开返回 429/999，因此只能保存检索线索，未把缓存长摘要升格为全文证据。LUMS 校友年刊提供 Huzaifa Rashid 线索，但直接打开失败；同名 LinkedIn 的学校也不一致，未合并。Brown B-Lab 新闻中 Milidu Jayaweera 是 Biomedical engineering and entrepreneurship 的本科成员，邻近 ChopChop 三人另标 PRIME 硕士；先检索摘要时存在误读风险，正文核查后排除 Milidu。时间限制而非检索饱和结束，接下来应查 2024、2025、2026 入学迎新新闻与可打开履历，补齐时间线及轨道。

机器结构检查只验证 JSON 结构和出处关联。网页支持性逐项人工检查仍有限，四条记录也不能作为成熟内容验收。规则难点主要是届别、旧校友身份与入学年的分离，以及如何保留失败访问产生的本人线索；本次宁可不把这些线索写成案例，也没有为最近三届凑数。

实际首次验证失败：文档描述经历相对申请时间，但结构例没有给该字段名；我采用 relative_to_application，验证器要求 relative_timing。已改成验证器字段后复验。该修正只解决格式，不补证据。

主审补核：重开三篇官网人物访谈与Reddit原帖，确认核心学历与offer自报。Joseph表述是想选择住校一年制，未明确实际轨道，因此track改为unknown，愿望另存format_preference。Reddit精确日期只见搜索缓存，已另设snippet_only来源S8，正文来源published_on保留null，2026申请季改为带索引限制的inferred字段。独立初稿仍在independent-draft/，不把修正版称首次无误通过。
