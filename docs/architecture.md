# Skill 架构与维护约定

本项目按可独立安装的 Agent Skills 目录组织，采用简洁入口、按需参考和确定性辅助工具。没有客观的“最强 Skill 架构”排名；本次对照官方实现，选择适合单一研究技能的部分，没有复制大型插件、依赖管理或多技能路由框架。

## 对照依据

2026-10-05 检查以下原始规范与 GitHub 文件，作为设计依据而非质量排名：

| 来源 | 本项目采用的做法 |
| --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | 目录名与 name 一致，SKILL.md 有元信息，脚本与参考文件使用相对包路径 |
| [OpenAI skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) | 简洁入口、条件细节按需读取，agents/openai.yaml 提供 Codex 元数据 |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | 实际请求驱动迭代，保存评估材料，区分自动检查与研究行为质量 |
| [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills) | 新安装使用个人 .agents/skills 目录，可链接技能目录，避免同名重复安装 |

Agent Skills 规范支持 compatibility 元信息，但当前本机官方辅助校验器的允许字段列表未包含它。本项目将环境要求写在入口正文，避免为一个可选字段修改上游工具或造成旧校验器误报。

## 内容归属

```text
admission-intelligence/
├── README.md                     用户入口、安装与能力边界
├── CONTRIBUTING.md               维护与验证方式
├── pyproject.toml                Python 格式与静态检查约定
├── requirements-dev.txt          固定版本的维护工具
├── skills/admission-intelligence/  独立安装单元
│   ├── SKILL.md                  范围、核心约束、读取时机
│   ├── agents/openai.yaml        Codex 展示与调用配置
│   ├── references/               检索、证据与输出细节
│   └── scripts/                  记录校验与月级区间计算
├── tests/                        自动回归与独立安装检查
├── evals/                        人工／模型评估、原始结果与日志
├── research/                     按项目与运行日期保存证据
├── docs/                         架构说明及不可覆盖的历史记录
└── .github/workflows/validate.yml 持续验证
```

技能不依赖仓库外部目录；README、评估、研究历史及维护工具均不随技能安装。未实际需要的 assets、插件清单、发布脚本和第三方框架不创建空目录。

SKILL.md 保留默认目的、重要证据边界和资源读取时机。完整研究读取 workflow；字段核实读取 evidence；准备交付或保存记录读取 output。详细规则由参考文件维护，不在入口逐条重复，历史版本仍可通过 Git 追溯。

## 校验器责任

validate_cases.py 的公开接口仍为 validate(data) 与原 CLI。先检查输入结构、日期和数值，之后核对来源与案例的连接关系；分两阶段是为了保证坏输入返回错误而非触发异常，并非运行两套互相替代的规则。结构检查按来源、案例、冲突、画像拆成命名方法。

两项 CLI 都拒绝重复键、NaN、Infinity 及指数溢出数字。成员来源连接只接受直接记载、自报或二手字段／经历，不能只靠未知字段通过；计算年限的 calculation 要有非空方法文字。JSON 结构通过仍不表示学校网页支持结论。

重复的几行严格 JSON 读取钩子在两个独立 CLI 中保留，避免为微小共用代码引入模块加载与安装路径耦合。后续如有更多工具需要共同读取逻辑，再按实际依赖拆分模块。

## 本次复审与验证

上一轮主要整理了人类阅读入口，未深入检查字段规则。独立只读复审新增发现三项实质问题：空白／布尔计算方法通过、嵌套指数溢出未被拒绝、画像能只引用未知成员字段来源。新回归先复现失败，再修复；可安装包检查还捕获了迁移参考内容后的相对路径错误。

历史评估文件从 tests 移到 evals，原始日志和初稿未删除或改写。历史文档里的旧 tests 路径作为当时记录保留，现路径见 evals/README.md。现有研究版本与人数未调整，不将架构整理声称为新的完整研究验收。

格式与静态检查、独立安装测试、记录检查均进入持续验证。只有真实运行才更新通过状态；已有有限研究和近期年级覆盖缺口仍按研究索引说明。
