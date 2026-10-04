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
  "schema_version": "1.0",
  "researched_on": "YYYY-MM-DD",
  "scope": {"institution": "...", "program": "...", "tracks": [], "years": []},
  "sources": [{"id": "S1", "url": "...", "title": "...", "source_type": "official_profile", "accessed_on": "YYYY-MM-DD", "published_on": null, "access_state": "full_text", "locator": "..."}],
  "cases": [{
    "id": "C1", "public_name_or_handle": "...",
    "identity_link": {"basis": "...", "source_ids": ["S1"]},
    "fields": {
      "enrollment_status": {"value": null, "status": "unknown", "source_ids": []},
      "track": {"value": null, "status": "unknown", "source_ids": []},
      "undergraduate_school": {"value": null, "status": "unknown", "source_ids": []},
      "undergraduate_major": {"value": null, "status": "unknown", "source_ids": []},
      "undergraduate_start": {"value": null, "status": "unknown", "source_ids": []},
      "undergraduate_end": {"value": null, "status": "unknown", "source_ids": []},
      "masters_start": {"value": null, "status": "unknown", "source_ids": []},
      "masters_graduation": {"value": null, "status": "unknown", "source_ids": []},
      "work_duration_before_application": {"value": null, "status": "unknown", "source_ids": [], "cutoff": null, "calculation": null},
      "application_narrative": {"value": null, "status": "unknown", "source_ids": []}
    },
    "experiences": [], "primary_archetype": null, "tags": [], "conflicts": []
  }],
  "archetypes": [{"label": "...", "status": "inferred", "case_ids": [], "source_ids": [], "scope": "...", "limitations": "..."}]
}
```

experiences 每项保存类型（full_time／part_time／internship／research／project）、单位／岗位、原始起止日期、相对申请时间（before_application／before_enrollment_only／during_program／after_program／unknown）、status 与 source_ids。可附公开 GPA 原始量表和教育地区等相关字段，使用同样证据结构。

所有 source_ids 必须存在；推断画像必须指向实际 case_ids；unknown 的值用 null，而不是 0、无工作或自动估算。冲突值保存各来源，不能丢弃冲突后输出已确认。
