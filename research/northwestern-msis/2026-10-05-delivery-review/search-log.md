# 检索日志

2026-10-05；范围：Northwestern SPS Master of Science in Information Systems，当前各版本分开，优先搜索2023—2025、历史案例单列。工具：web搜索及打开，未使用登录权限。

第一轮实际查询：`site.northwestern.edu MSIS master information systems student alumni`；`Northwestern MSIS alumni resume education work`；`Northwestern MSIS admission 一亩三分地 录取`。发现官网Austin、Swetha、Nancy及LinkedIn线索；排除其他学位、学校职业简历模板、Northwestern Mutual公司和未录取的讨论者。

核查：打开MSIS官方主页面，确认part-time远程与accelerated full-time不同；打开Austin官网正文，点击主页面Swetha、Nancy、compare页面并读取。得到3个独立官方历史案例。三人的本科学校专业与申请前年限大多缺失；新增的是身份、版本与经历时间边界，而非完整画像。

LinkedIn Swetha个人页：搜索索引有教育区间；直接open返回Internal Error。来源保留snippet_only，不声称全文访问，不据其索引把人物完整拼接。Reddit `experiences_with_onlineparttime_msis_degree`：open成功，开帖者在考虑申请，排除。

第二轮实际查询：`"Northwestern" "MSIS" "2024" "admitted"`；`"Northwestern" "MSIS" "2025" "resume"`；`site.1point3acres.com "Northwestern" "MSIS"`。得到一个2020年匿名AD自报的原帖搜索提取，新增1个录取线索；正文open失败（Cache miss）。提取中的隐去本科字段没有尝试绕过；它没有确定版本或入学证明。

检索覆盖：官网正文可读；个人履历渠道仅摘要；论坛Reddit可读及一亩三分地仅摘要。没有定向执行GradCafe、知乎、微信、小红书或其他社交平台。最近2023—2025入学案例未还原，不代表不存在。

停止：有限forward-test范围结束。第二轮仍新增录取线索，不满足“连续两轮无新增案例或关键字段”的饱和条件。未把测试结束伪写为自然检索终点。

第四轮来源支持审查：独立重开对应官方URL与定向find，核查记录见evals/forward-evaluations/round4-source-audit.md；修正已知发布日期及正文/JSON对齐，不添加研究案例，不声称新增年份覆盖。

## 第五轮本次执行

本次仅做交付来源复核，未重新执行上面的历史查询。直接打开 Austin Olson、Swetha Popuri、Nancy Dandridge 三篇官网正文，全部可读。核对 Austin 线上就读、pre-med不代表完成本科学位、军旅年份不代表申请前全职年限；Swetha毕业状态与毕业后fellowship；Nancy2016年在读与线上版本。未重新打开一亩三分地原帖或LinkedIn，不升级其旧摘要状态。新增人物为0；已核实案例数组从4条收敛为3条，摘要线索移到本日志；既有原目录完整保留。

## 未核实摘要线索（原 C4 完整保留）

下面是旧版取证记录的保留副本，仅供后续检索，不代表本次核实，也不纳入案例与录取计数。

```json
{
  "id": "C4",
  "public_name_or_handle": "wujx1998",
  "identity_link": {
    "basis": "single original source explicitly names Northwestern MSIS person or anonymous author; no name-only cross-site merge",
    "source_ids": [
      "S6"
    ],
    "evidence": [
      {
        "source_id": "S6",
        "locator": "named MSIS profile or original post header"
      }
    ]
  },
  "fields": {
    "work_duration_before_application": {
      "value": null,
      "status": "unknown",
      "source_ids": [],
      "evidence": []
    },
    "track": {
      "value": null,
      "status": "unknown",
      "source_ids": [],
      "evidence": []
    },
    "undergraduate_end": {
      "value": null,
      "status": "unknown",
      "source_ids": [],
      "evidence": []
    },
    "masters_graduation": {
      "value": null,
      "status": "unknown",
      "source_ids": [],
      "evidence": []
    },
    "undergraduate_school": {
      "value": null,
      "status": "unknown",
      "source_ids": [],
      "evidence": []
    },
    "application_narrative": {
      "value": null,
      "status": "unknown",
      "source_ids": [],
      "evidence": []
    },
    "masters_start": {
      "value": {
        "date": "2020",
        "state": "planned",
        "term": "Fall"
      },
      "status": "self_reported",
      "source_ids": [
        "S6"
      ],
      "evidence": [
        {
          "source_id": "S6",
          "locator": "入学年度2020 / Fall is planned offer year, not attendance proof"
        }
      ]
    },
    "enrollment_status": {
      "value": "offer_self_reported",
      "status": "self_reported",
      "source_ids": [
        "S6"
      ],
      "evidence": [
        {
          "source_id": "S6",
          "locator": "search extract: 申请结果 AD无奖; notification 2020-02-21"
        }
      ]
    },
    "undergraduate_major": {
      "value": null,
      "status": "unknown",
      "source_ids": [],
      "evidence": []
    },
    "undergraduate_start": {
      "value": null,
      "status": "unknown",
      "source_ids": [],
      "evidence": []
    }
  },
  "experiences": [],
  "conflicts": [],
  "tags": [
    "track_unknown",
    "anonymous_self_report",
    "historical"
  ]
}
```
