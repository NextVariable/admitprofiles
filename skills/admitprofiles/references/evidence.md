# 研究与证据规则

## 来源等级是逐项的

官网可以确认其明确记载的学生身份、学校、经历，不自动确认未写出的 GPA 或确切年份。本人网站、公开简历和 LinkedIn 是本人公开披露；论坛账号自报保留自报属性；中介和社区汇总保留二手属性。不存在一个“官网来源”标签能给全行未知事实背书。

每项主张记录 value、status、source_ids 和 evidence（每项含 source_id、locator）。来源内的段落定位必须针对该字段，不以来源整体标题代替。status 使用 documented（正文明确记载）、self_reported（本人自述）、secondary（二手）、calculated（日期计算）、inferred（分析）、unknown（未公开／证据不足）、conflicting（来源冲突）。官网访谈若仅转述本人经历，保留这一性质；documented 表示来源记载而非独立审计真实性。

来源记录 id、url、title、publisher、source_type、accessed_on、published_on（不明为 null）、access_state 和 locator。locator 可用标题／段落和极短摘录帮助核查，不复制全文或完整文书。正文受限时，引用摘要仅能支持其确实显示的有限内容，状态保留 snippet_only，身份和复杂时间线不得以此升级为完整核实。

搜索工具返回的长篇缓存也保留snippet_only，不因篇幅长而改称打开正文。为这些线索在检索日志中记录具体查询、取证日期、目标URL、直接打开结果和与主张有关的短片段；无法保留原始输出时明确这一复核限制。线索放在检索日志中，不用未知身份填充cases或画像计数。姓名拼写差异保留原始变体和定位；同页图注与正文对应可说明连接理由，跨来源仍须独立核实。

冲突并列保留两个值及各自出处，解释为何采用某个值或暂时不采用。不要用“整体置信度 90%”掩盖关键字段缺证据。

## 可复用检索方式

使用当前工具支持的检索语法，按项目实际情况调整：

- 项目全称／简称＋student profile／alumni／class of／admitted／申请总结／录取案例。
- 项目全称＋site:linkedin.com/in、site:reddit.com、site:1point3acres.com 或其他相关站点。
- 姓名＋学校／项目＋resume／CV／本科／experience／SOP。
- 项目旧名称、具体轨道、校区、申请年分别搜索，结果独立记录。

先发现再核实；论坛和社交平台的讨论可以用于了解项目体验，不能因为有人讨论项目就当他被录取。跨站转载与相同学校公关稿计作同一证据来源。

## 日期与年限

日期按 YYYY-MM-DD、YYYY-MM 或 YYYY 保留精度。不要将 YYYY 自动当成 1 月 1 日。目标硕士的 expected_graduation 与 completed_graduation 分开；文章说“将于 2025 年毕业”，即使现在已到 2026 年也不能自动写“已毕业”。

有完整月级工作区间时，先保留原始日期及结束月份含义，再标准化为半开区间取并集计算。来源明确表示最后一个在职月份时结束月包含该月；未说明时同时输出包含／不包含结束月的范围，不把月份表述自动当作月初；来源写“至今”时不能把访问日以前的全部工作都算到申请前。申请时点未知，年限的截止边界必须明确写成入学前近似。只有年份时优先给范围或原始区间，不出小数点精确年限。

计算值保留输入区间、来源、截止边界和计算方法，可复核。课程项目和硕士必修实习属于就读经历，不属于之前的申请背景。

## 抽样边界

只观察到 admitted／enrolled／graduated 且可公开发现的人，不等于观察到全部申请者。不得用这种样本反推 P(录取|背景)。拒录自报可以帮助提出问题，但没有共同分母和完整材料时仍不计算录取率。

研究方向、线上模式和毕业年代可能改变路径；研究者不能为了得到更多案例合并不同招生对象。身份确认但轨道未知者可以呈现，不能加入具体轨道的分布统计。

## 月级计算器输入

`work_months.py` 输入为 JSON 对象，含 cutoff（YYYY-MM，截断到该月月初）及 intervals 数组，每项为 start、end（YYYY-MM；持续至 cutoff 为 null）、end_inclusive（true／false；含义不明确为 null）。只传已核实的相关工作区间。截止日精确到日或只有年份时不要强行使用这个月级工具。输出并集月数范围，不是录取优势评分；不能判定区间是否全职或属于申请前。

## 申请前背景还原

每个案例记录本科学校、专业、教育地区／类型、本科入学和毕业日期、目标硕士入学日期和毕业状态、申请前正式工作及实习、科研／项目、公开 GPA 及原始量表、公开申请路线或文书材料。

“studied finance”“某校graduate”只能确认学习经历，不能自动确认本科层级、完成学位或正式专业。层级不明时把已知学校与学科保存在待核实教育经历，本科字段保留未知；pre-med等预备课程也不等于授予学位专业。迎新、注册、开课、录取和学位授予是不同事件，迎新报道只能确认其当时入学／参与迎新的观察，不把迎新日当精确入学日。

只将能够证明在申请前发生的经历作为申请背景。若申请时间未知，以入学前为近似边界并明确标记“入学前，未确认是否早于递交申请”；期间不明的经历保留待核实。学校标注的 '25 等届别不等于实际毕业确认，更不等于入学年。

工作年限区分正式全职、兼职、自雇、实习和研究助理；精确日期可核实时，将相关正式工作区间取并集后计算，重叠不重复累计。注明计算截止日期和是否以入学代替申请时点。仅年份给范围；只说“多年”就保留原意；来源直接说 3.5 年时记录“来源明示”，不要伪造起止日期。未公开不等于零，应届身份也不能仅靠缺少工作记录确定。

国家／地区的本科分类按学校和校区，不凭姓名推断国籍、族裔或身份。GPA 不擅自换算不同量表。不要记录无关联系方式和敏感个人信息。

“包装路线”只在本人公开 SOP、申请复盘或明确访谈时描述其自述表达方式。事后访谈的选择动机不等于申请文书内容。履历能支持经历路径，不能支持文书故事或录取原因；模型提出的叙事解释标为推断。

---

# Research and evidence rules — English

This section translates the Chinese rules above; it is not a second set of requirements.

## Evidence grades are claim-specific

Official pages support explicitly stated identity, education or experience, not unstated GPA or exact dates. Personal sites, public résumés and LinkedIn are public self-disclosures; forum claims retain self-reported status; agency/community summaries retain secondary status. An official-source label does not validate every unknown field.

Every claim records `value`, `status`, `source_ids` and `evidence` with `source_id` and field-specific `locator`. A page title alone is insufficient. Status values are `documented` (explicitly stated), `self_reported`, `secondary`, `calculated`, `inferred`, `unknown` and `conflicting`. An official interview quoting a person's history retains that nature; documented means source-stated, not independently audited truth.

Source records contain `id`, `url`, `title`, `publisher`, `source_type`, `accessed_on`, `published_on` (null when unknown), `access_state` and `locator`. Use headings/paragraphs and very short excerpts, not full pages or essays. Restricted-page snippets support only displayed content and remain `snippet_only`; do not use them to claim full identity/timeline verification.

Long search-tool caches remain snippet-only regardless of length. Log query, evidence date, target URL, direct-open result and a short supporting fragment. Disclose when raw output cannot be retained. Keep leads in search logs rather than filling cases or group counts with unverified identities. Preserve name variants and locators. Captions and body text on the same page may support a connection with an explicit basis; cross-source identity links still require separate verification.

Retain conflicting values and their sources together, explaining any resolution or decision to withhold a value. Do not hide missing key evidence behind an overall confidence percentage.

## Search patterns

Adapt syntax to current tools and the program: full/short program name with student profile, alumni, class of, admitted, application retrospective or admission case; program name with `site:linkedin.com/in`, `site:reddit.com`, `site:1point3acres.com` or relevant sites; name with school/program and résumé, CV, undergraduate, experience or SOP; and separate searches for former names, tracks, campuses and application years.

Discover first, verify second. Discussion may describe program experience but does not establish the participant's admission. Reposts and the same school press release count as one evidence source.

## Dates and duration

Preserve precision as YYYY-MM-DD, YYYY-MM or YYYY. A year is not January 1. Keep expected and completed master's graduation separate: a statement of expected graduation in 2025 does not prove completion merely because the current year is 2026.

For complete month-level work intervals, retain raw dates and end-month meaning before normalizing to half-open intervals and computing their union. Include the last month if the source explicitly says it was worked; otherwise report inclusive/exclusive bounds rather than assuming month-start. “Present” does not make all work before access pre-application. If application timing is unknown, explicitly identify a pre-enrollment approximation. With year-only evidence report ranges or raw intervals, not decimal precision.

Retain inputs, sources, cutoff and calculation method for review. Required master's internships and course projects belong to study, not earlier application background.

## Sampling boundaries

Publicly discoverable admitted/enrolled/graduated people are not all applicants. Do not infer P(admission|background) from this sample. Rejection self-reports may prompt questions, but without a common denominator and complete material do not calculate admission rates.

Tracks, delivery modes and eras can change paths. Do not combine different applicant populations to enlarge a sample. Confirmed identities with unknown tracks may be shown but excluded from track-specific distributions.

## Month calculator input

`work_months.py` accepts a JSON object with `cutoff` (YYYY-MM, truncated at that month's start) and `intervals` containing `start`, `end` (YYYY-MM; null for ongoing until cutoff) and `end_inclusive` (true/false/null when unclear). Supply only verified relevant work intervals. Do not force day-precision or year-only cutoffs into this tool. Output is a union-month range, not an admission-advantage score; it cannot determine full-time status or pre-application relevance.

## Reconstruct prior backgrounds

Record undergraduate school, major, education region/type, undergraduate start/end, target master's start and graduation status, prior employment/internships, research/projects, public GPA with its original scale, and public application accounts or essays.

“Studied finance” or “graduate of a school” establishes education, not automatically undergraduate level, completed degree or formal major. Store known school/subject as education pending verification and leave undergraduate fields unknown. Pre-med preparation is not an awarded major. Orientation, registration, classes, admission and degree award are different events. Orientation reports establish an enrollment/participation observation, not an exact personal start date.

Only proven pre-application experiences count as application background. If application dates are unknown, use an explicitly labeled pre-enrollment approximation: not confirmed before submission. Undated experiences remain pending. Class labels such as ’25 establish neither actual graduation nor entry year.

Separate full-time, part-time, self-employed, internships and research-assistant work. For verified dates, compute the union of relevant employment intervals without double-counting overlap. State cutoff and whether enrollment substitutes for application. Give ranges for year-only evidence, preserve “many years” as stated, and record source-stated 3.5 years without inventing start/end dates. Undisclosed does not mean zero; missing work records do not establish new-graduate status.

Classify undergraduate regions by institution and campus, not name-based nationality, ethnicity or identity guesses. Do not silently convert GPA scales. Do not collect irrelevant contact details or sensitive personal information.

Describe application presentation only from public SOPs, application retrospectives or explicit interviews as self-described expression. Post-admission motivation interviews are not evidence of essay content. Résumés support experience paths, not application stories or admission causes. Label model-proposed narrative interpretations as inference.
