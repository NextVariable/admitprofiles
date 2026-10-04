# 交付与记录格式

## 用户看到的报告

开头结论先行：具体项目／方向、实际观察到的画像或路径、独立案例数和年份、主要信息缺口。接着逐类解释共同背景和代表案例，给来源。不要以统一招生公式表述。

具体案例可按用户需求用表格，列出案例、录取／在读／毕业状态、项目版本、本科学校专业及入学毕业年、硕士入学年与毕业状态、申请前工作年限及计算边界、实习科研项目、申请路线／文书证据、出处。缺失写未公开，冲突写有冲突并展开。表格过宽时分成学历时间线与工作／申请路径，不能为了简洁省掉用户要求的字段。

随后说明项目官方要求与课程背景，研究覆盖和局限。如果用户要求个人匹配，放在研究结论之后，并保持个人事实与分析分开。

## 保存记录

默认路径为 research/<项目标识>/<YYYY-MM-DD>/。已存在目录使用不同运行后缀，或在明确更新任务中保留旧版本。research 不包含自动安装器、虚构示例或生成身份。

report.md 是中文可读结论；search-log.md 记录查询、渠道、访问情况、新增独立案例数和停止原因；cases.json 用于未来复核与复用。简短回答可只保存报告，完整项目研究需保存三者。

cases.json 结构示例（字段值下方仅为结构说明，实际文件不得用占位符充数）：

```json
{
  "schema_version": "1.1",
  "researched_on": "YYYY-MM-DD",
  "scope": {"institution": "...", "program": "...", "tracks": [], "years": []},
  "sources": [{"id": "S1", "url": "...", "title": "...", "source_type": "official_profile", "accessed_on": "YYYY-MM-DD", "published_on": null, "access_state": "full_text", "locator": "..."}],
  "cases": [{
    "id": "C1", "public_name_or_handle": "...",
    "identity_link": {"basis": "...", "source_ids": ["S1"], "evidence": [{"source_id": "S1", "locator": "..."}]},
    "fields": {
      "enrollment_status": {"value": null, "status": "unknown", "source_ids": [], "evidence": []},
      "track": {"value": null, "status": "unknown", "source_ids": [], "evidence": []},
      "undergraduate_school": {"value": null, "status": "unknown", "source_ids": [], "evidence": []},
      "undergraduate_major": {"value": null, "status": "unknown", "source_ids": [], "evidence": []},
      "undergraduate_start": {"value": null, "status": "unknown", "source_ids": [], "evidence": []},
      "undergraduate_end": {"value": null, "status": "unknown", "source_ids": [], "evidence": []},
      "masters_start": {"value": null, "status": "unknown", "source_ids": [], "evidence": []},
      "masters_graduation": {"value": null, "status": "unknown", "source_ids": [], "evidence": []},
      "work_duration_before_application": {"value": null, "status": "unknown", "source_ids": [], "cutoff": null, "calculation": null, "evidence": []},
      "application_narrative": {"value": null, "status": "unknown", "source_ids": [], "evidence": []}
    },
    "experiences": [], "primary_archetype": null, "tags": [], "conflicts": []
  }],
  "archetypes": [{"label": "...", "status": "inferred", "case_ids": [], "source_ids": [], "evidence": [], "scope": "...", "limitations": "..."}]
}
```

experiences 每项保存类型（full_time／part_time／internship／research／project）、单位／岗位、原始起止日期、相对申请时间（before_application／before_enrollment_only／during_program／after_program／unknown）、status 与 source_ids。可附公开 GPA 原始量表和教育地区等相关字段，使用同样证据结构。

经历的相对时间键名必须为relative_timing；不要使用relative_to_application等同义键替代。完整键形为 `{type, organization, role, start, end, relative_timing, status, source_ids, evidence}`；单位、岗位或日期未公开可用null，source_ids和evidence仍按证据约定填写。申请时点未知的既往职业年限单列在经历中，申请前年限字段保留unknown，或按已明确入学边界给近似并附说明，不把附注中的不确定性藏在已确认数字之后。

## 机器检查约定

新记录使用 schema_version 1.1；历史 1.0 记录保留原样，不伪称通过新检查。每个非 unknown 字段的 source_ids 至少一个，evidence 至少一项并为每个 source_id 提供 `{source_id, locator}`。未知字段 value 为 null。字段层冲突需在 case.conflicts 中保存 `{field, values: [{value, source_ids, evidence}]}`，保留两种以上不同值。

access_state 为 full_text／partial_text／snippet_only／blocked／failed；阻止访问或失败的来源不得支持字段，摘要单列有限证据，不许升级 documentary 事实。来源 id、案例 id 唯一；来源 URL 为 http 或 https。experiences 使用 full_time／part_time／self_employed／internship／research／project／employment_unspecified。经历同样提供 evidence 定位。

画像 case_ids 必须非空，不能包括拒录、候补、未知准入状态，不能混入明确排除的项目版本；轨道未知案例只能组成注明轨道未确认的路径，不加入已确认轨道的比例。

所有 source_ids 必须存在；推断画像必须指向实际 case_ids；unknown 的值用 null，而不是 0、无工作或自动估算。冲突值保存各来源，不能丢弃冲突后输出已确认。

字段 status 使用 documented／self_reported／secondary／calculated／inferred／unknown／conflicting。enrollment_status.value 使用 offer_self_reported／offer_documented／enrolled／graduated／waitlisted／rejected；无准入证据时使用 null、status unknown。预计入学与毕业在附注或日期对象中标 planned／expected，不当作完成。计算年限必须附 cutoff 与 calculation。

身份连接 identity_link 必须含非空 basis 与对应 source_ids、evidence。画像准入状态必须直接记载或自报，不能靠 inferred／calculated／conflicting 字段入组；每个成员至少有一个字段来源被画像引用。这个连接只检查出处关系，仍需人工核实这些来源是否支持分类。来源与研究访问日期使用有效 YYYY-MM-DD。JSON不允许重复键或NaN／Infinity。未知字段若保留来源，同样需要字段定位。

画像也可引用成员experiences中的直接记载、自报或二手经历出处，不强迫将工作经历复制到学历字段才能通过检查；unknown、inferred或calculated经历不能单独充当成员来源连接。经历是否确实属于该人且是否支持申请前分类，仍须按身份与时间边界复核。

官方项目资料存在内部冲突时，可增加 program_conflicts 数组，每项含 field、两种以上不同的原始文字 alternatives、resolution（未解决也明确写出）、source_ids 与 evidence。它与人物字段冲突分开，不把官网矛盾塞进某个人的履历。

同一人物的同一冲突字段只保存一条冲突记录，将所有不同值及出处归入其 values。已知文字值不可留空；同一字段不重复保存相同 source_id 与 locator。来源访问日期不得晚于本次 researched_on；后续补查时更新研究日期并保留旧版。计算年限的 cutoff 使用有效的 YYYY、YYYY-MM 或 YYYY-MM-DD，保持来源精度；月级计算器仍只接受 YYYY-MM。两项工具都拒绝重复 JSON 键及非有限数字。

学历层级未确认的已知学校／学科，可保存为fields.prior_education的value，注明degree_level未确认，使用相同的status、source_ids与evidence；undergraduate字段保持unknown。观察日期可另存fields.enrollment_observation，value含事件类型与日期，不把它当作实际开学日。自定义顶层扩展（如leads）不在验证器保证范围内；未核实线索默认记录于search-log.md，不凭一次结构通过宣称扩展已验证。数字形式年限不得为负数、布尔值或非有限数，单位仍需在value对象或附注里明确。
