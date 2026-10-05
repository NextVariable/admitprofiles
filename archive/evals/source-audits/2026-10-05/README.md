# 全历史来源审计

基线为7c0e6f071a455418267a20ff7ef2b468862bbf86，库存固定了11份cases及对应报告，共703条：来源元数据、身份、所有字段（含未知）、经历、冲突备选、画像、项目冲突与整份报告。inventory.json记录原文件SHA256；旧材料未改写。审计是逐条人工/模型网页核查，不是程序证明来源真值。

| 项目 | 单元 | 有支持 | 过度主张 | 当前无法复核 | 未知保留 |
| --- | ---: | ---: | ---: | ---: | ---: |
| [Berkeley](berkeley.json) | 237 | 96 | 10 | 6 | 125 |
| [Brown](brown.json) | 170 | 84 | 1 | 13 | 72 |
| [CMU](cmu.json) | 139 | 78 | 3 | 2 | 56 |
| [Northwestern](northwestern.json) | 157 | 51 | 3 | 12 | 91 |
| 总计 | 703 | 309 | 17 | 33 | 344 |

数字是版本化核查单位，不是独立人物或309个来源网页。四个项目原引用网址分别9、10、8、7，均重新打开或尝试；不可访问不证明旧版当时读取虚假。Berkeley另检查8个库存之外的scope/leads/空画像约定，单列于JSON，不伪称合入703。

发现初稿本科层级、迎新观察日当入学日、申请前年限、希望住校当实际轨道、报告“未公开”越界等问题。修正版本在[研究索引](../../../../research/README.md)，历史原件保留；逐项rationale、checked_urls、evidence_locators与日期在JSON，中文说明在对应.md。

运行python3 tests/check_source_audit.py核对703个ID无遗漏/重复、审计出处及原文件哈希。这个检查只保证记录覆盖与历史完整，不替代证据支持性判断；309 supported也是本次审阅结论，非无误保证。

---

# Historical source audit — English

The original baseline was commit `7c0e6f071a455418267a20ff7ef2b468862bbf86` before privacy-history rewriting. The inventory freezes 11 case files and associated reports, covering 703 units: source metadata, identities, every field including unknowns, experiences, conflict alternatives, groups, program conflicts and complete reports. `inventory.json` records original SHA256 hashes. Frozen research material remains unchanged. This is claim-by-claim human/model page review, not programmatic proof of source truth.

| Program | Units | Supported | Overstated | Currently unverifiable | Unknown retained |
| --- | ---: | ---: | ---: | ---: | ---: |
| [Berkeley](berkeley.json) | 237 | 96 | 10 | 6 | 125 |
| [Brown](brown.json) | 170 | 84 | 1 | 13 | 72 |
| [CMU](cmu.json) | 139 | 78 | 3 | 2 | 56 |
| [Northwestern](northwestern.json) | 157 | 51 | 3 | 12 | 91 |
| Total | 703 | 309 | 17 | 33 | 344 |

Counts refer to versioned review units, not independent people or 309 source pages. The four programs had 9, 10, 8 and 7 original URLs respectively; each was reopened or attempted. Current inaccessibility does not prove historical access was fabricated. Eight additional Berkeley scope/lead/empty-group checks outside the inventory are separate JSON entries, not included in 703.

Review found errors in degree-level assumptions, treating orientation observations as exact entry dates, pre-application durations, inferring actual tracks from housing preferences and overstating “not publicly disclosed.” Current corrected versions are in the [research index](../../../../research/README.md); historical originals remain. JSON records contain per-unit reasons, checked URLs, evidence locators and dates; original explanations remain in Chinese.

Run `python3 tests/check_source_audit.py archive/evals/source-audits/2026-10-05 --records-root archive` from the repository root to check all 703 IDs, completeness, uniqueness, audit citations and frozen hashes. This guarantees record coverage and historical integrity only, not semantic support. The 309 supported units are review judgments, not an error-free guarantee.
