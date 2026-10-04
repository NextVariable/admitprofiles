# 第五轮交付与来源复核（2026-10-05）

本轮由当前主审执行，已读历史结论，不是独立盲测；不将它计算成模型正确率、隐式触发准确率或全渠道新增研究。原始目标仍为项目公开录取背景研究，个人定位仅在用户要求且有真实履历时补充。没有新增概率评分、自动SOP或生成履历功能。

## 实际来源检查

直接打开五个官方URL并阅读正文，核查13项判断，再核对一个历史摘要记录的身份依据，共14项。以下判断均为本轮实际执行；正文缺失不补猜。

Brown [官方FAQ](https://prime.brown.edu/faqs)：主要面向STEM不是唯一本科门槛，官网明确有经济／商科／工业设计毕业者；2027开放申请与deadline小节的2028／summer 2025起始存在矛盾。这三项与旧报告的有限结论一致，不输出确定申请日期。

Berkeley [Who Should Apply](https://developmentengineering.berkeley.edu/programs/deveng-master/who-should-apply/)：技术准备必需且举例两门连续课程；本科后职业经验不是必需；多数1—3年是官网概括，不是硬上限或案例分布。这三项未发现需改写旧报告的问题。

Northwestern [Austin](https://sps.northwestern.edu/stories/news-stories/msis-austin-olson.html)：线上MSIS有直接文字；pre-med就读不能证明已完成本科；2013—2021军旅区间不证明申请前全职年限。这三项与保留未知的记录一致。

Northwestern [Swetha](https://sps.northwestern.edu/stories/news-stories/msis-swetha-popuri.html)：图注支持毕业身份；CommonSpirit fellowship明确毕业后开始。这两项不应被转写为申请前背景。

Northwestern [Nancy](https://sps.northwestern.edu/stories/news-stories/information-systems-nancy-dandridge.html)：正文说明线上就读；2016稿的正在学习状态不能随当前年份升级成已毕业。这两项与现有记录一致。

第14项来自历史JSON而非本次网页读取：Northwestern C4 的唯一身份来源 S6 标为 snippet_only。旧版仍把它放入 cases，与技能“线索保存在检索日志”要求不一致。新版本只保留三个正文身份案例；C4完整记录转存新的search-log.md，原目录不改动，旧来源状态不升级。没有再次访问其论坛原帖，不声称否定其自报或证明未录取。

## 自动回归

新增6个测试方法包含有效／损坏URL、空占位值、冲突备选值、过深JSON正常失败，以及25,350个跨年区间组合。合成域穷举核对月集合与区间合并算法，并对每组再次检查区间倒序及重复不改变结果。初次运行实际发现13个失败子情形；修正后再跑完整套件，原始失败日志保留在results。既有随机5000组、752种嵌套变异和200组对照仍继续运行。

修改过程中完整套件捕获了对非字符串status使用集合查询造成的类型异常，随后改为无需哈希的查询，再跑全套验证。这个中间失败说明不能以新增测试局部通过作为交付条件。交付检查还发现评估索引先引用了尚未写出的机器结果文件，链接测试拒绝通过；结果保存后重新运行，不把这次失败覆盖掉。所有结果以第五轮机器记录与GitHub本次提交的Actions为准。

## 范围与保留

未执行新的三个项目全渠道三届研究、重复模型盲测或平台隐式触发测试。五个官方页面的13项支持判断及一项记录归类核查不等于整个历史库逐字段通过。运行包保持独立安装；历史文档、初稿、报告与原始日志保留，不堆入安装包。仓库仍为私有，未声明开源许可证。

新增失败日志归档仅裁剪行尾空格，保留断言、错误输出与退出结果；旧轮次日志未调整。
