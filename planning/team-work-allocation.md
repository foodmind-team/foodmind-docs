# FoodMind 七人小组分工计划

**Status:** Proposed
**Owner:** 项目负责人
**Last updated:** 28 July 2026
**Related repositories:** `foodmind-backend`, `foodmind-web`, `foodmind-android`, `foodmind-intelligence`, `foodmind-ml`, `foodmind-docs`
**Related scope:** UC-01 至 UC-09、四周 MVP 交付计划
**Open questions:** 以成员 A、B、C、D 暂代尚未提供姓名的四位成员；执行前替换为真实姓名

## 1. 分工目标

这套安排遵循三个原则：

1. 项目负责人承担架构风险最高、跨仓库依赖最多的工作，包括后端、Web、系统集成和必要重工。
2. H 与 W 是第二梯队的功能负责人，工作量低于项目负责人，但明显高于其余成员。
3. 其余四位成员只承担边界清楚、容易验收、出现问题时可快速支援的工作，不要求他们独立处理复杂架构或跨服务问题。

建议将相对工作量控制为：

| 成员 | 相对负荷 | 定位 |
| --- | ---: | --- |
| 项目负责人（你） | 100% | 技术负责人、后端/Web 主力、集成与重工兜底 |
| H | 75%–80% | Cooking Planner 功能负责人 |
| W | 70%–75% | ML 功能负责人，在明确规范和代码审查下使用 AI 开发 |
| 成员 A | 40%–45% | Android 常规页面与 API 接入 |
| 成员 B | 35%–40% | 测试、UAT 与缺陷复现 |
| 成员 C | 35%–40% | 数据与项目文档维护 |
| 成员 D | 30%–35% | 演示、素材、验收证据与发布协助 |

百分比表示相对投入强度，不等同于工时承诺。若课程规定每位成员必须有可识别贡献，可以使用提交记录、测试记录、文档署名和演示材料作为证据。

## 2. 角色与具体职责

### 2.1 项目负责人（你）：技术负责人及主力开发

**主责范围**

- `foodmind-backend`
  - Spring Boot 项目结构、数据库模型与迁移
  - 身份认证、JWT、权限和群组可见性规则
  - UC-01 至 UC-05、UC-09 所需的核心 API 与业务逻辑
  - 推荐、Cooking Planner、Chatbot 的公共 API 边界
  - Dashboard/weekly recap 的统一指标计算
  - OpenAPI、异常格式、服务间超时与 fallback
- `foodmind-web`
  - React 应用框架、鉴权、API client 和路由
  - Web 端所有 MVP 主流程及 Android/Web parity
  - 推荐、反馈、Cooking Planner、Chatbot 和 Dashboard 的 Web 集成
- 高难度与重工
  - 跨仓库架构、接口冻结、数据库和权限问题
  - `foodmind-intelligence` 的公共骨架、Backend 调用适配与服务集成
  - Runtime inference 的部署接线与 fallback
  - CI/CD、Docker、staging、最终端到端联调
  - 其他成员无法解决的阻塞、返工和高风险代码审查

**不应继续追加的工作**

- 不负责逐页整理截图、手工填写全部 UAT、制作全部演示文稿。
- 不替其他成员完成已经明确分配且风险较低的常规任务。

**主要交付物**

- 可部署的 Backend 与 Web
- 冻结的公共 OpenAPI 和关键私有契约
- 至少一条完整推荐垂直链路，以及全系统集成版本
- 高风险 PR 的最终审查结果

### 2.2 H：Cooking Planner 功能负责人

H 继续负责已经开始的 Cooking Planner，按一条完整功能链路交付，而不是只提交零散页面或 prompt。

**主责范围**

- `foodmind-intelligence` 中的 Cooking Planner Agent
- 受控 recipe catalogue、ingredient matching、时间/预算/饮食限制校验
- 结构化 ingredients、ordered steps、warnings、source recipe ID 输出
- Cooking Planner 的 schema、单元测试和固定测试样例
- 与成员 A 配合完成 Android Cooking Planner 页面
- 与项目负责人对接 Backend/Web；公共 API 和 Web 页面仍由项目负责人主责

**边界**

- 不负责推荐排序或 Chatbot。
- 不自行修改公共 API；需要变更时先提交契约变更说明。
- 不生成无来源的食品安全结论。

**主要交付物**

- UC-06 可运行链路
- 至少 10 个受控 recipe fixtures
- 正常、无匹配、限制冲突三类测试
- 一份简短的集成说明和演示脚本

### 2.3 W：ML 功能负责人

W 负责 `foodmind-ml` 的离线训练与评估。考虑到其代码能力有限但会合理使用 AI，任务必须拆成可验证的小步骤，所有生成代码都需要测试和审查。

**主责范围**

- 数据清洗、特征生成和可重复训练脚本
- Popularity/rule baseline
- 简单 cosine-similarity UserCF 与 ItemCF
- Logistic Regression 排序模型
- Precision@K、Recall@K、NDCG@K、coverage、diversity 等评估
- 版本化模型包、feature schema、训练配置与 model card
- 固定随机种子、依赖锁定和一条命令复现实验

**AI 使用规则**

- 每次只处理一个小 issue，例如“生成 UserCF 相似度测试”，避免一次生成整个 ML 系统。
- AI 生成的代码必须能说明输入、输出和失败条件。
- 合并前必须通过 lint、单元测试和小数据集 smoke test。
- 模型指标、数据规模和实验结论不得由 AI 猜测，必须来自实际运行结果。
- 项目负责人只审查接口、可复现性和上线风险，不接管 W 的常规实现。

**边界**

- W 不负责在线推理服务、Backend 接线或生产部署。
- 深度学习、矩阵分解、复杂 MLOps 不进入四周 MVP。

**主要交付物**

- 可重复执行的训练/评估 pipeline
- baseline、CF 和 LR 的对比结果
- 带版本号的模型包与 model card
- 供 `foodmind-intelligence` 消费的 contract fixture

### 2.4 成员 A：Android 常规功能开发

**主责范围**

- 按冻结的 OpenAPI 完成 Compose 页面和 Retrofit 接入
- 登录/注册、记录列表与表单、群组 feed、推荐卡片、反馈、Dashboard 等常规 UI
- 与 H 配合接入 Cooking Planner 页面
- 处理 loading、empty、error 三种基础状态

**减压边界**

- 不设计 Backend、数据库、权限或 Agent 架构。
- 不要求自行解决 API 不一致；记录请求/响应后交给项目负责人。
- 优先使用统一组件和现有样例，不追求复杂动画或过度定制。

**主要交付物**

- Android MVP 页面清单
- Android smoke test 记录
- Android/Web parity 检查结果

### 2.5 成员 B：测试与 UAT

**主责范围**

- 将 UC-01 至 UC-09 转成可执行验收步骤
- 在 Web 和 Android 上执行 happy path、权限拒绝、空数据和错误状态测试
- 记录缺陷的环境、步骤、预期、实际结果和截图
- 每轮集成后执行回归测试
- 维护 UAT traceability 和缺陷关闭状态

**减压边界**

- 不要求编写复杂自动化测试框架。
- 不直接修复架构类缺陷；只需提供稳定复现步骤。
- 自动化仅限团队已经提供模板的简单 API collection 或 UI smoke test。

**主要交付物**

- UC-01 至 UC-09 UAT 表
- Android/Web parity 测试证据
- 缺陷清单和最终回归结果

### 2.6 成员 C：数据与文档维护

**主责范围**

- 根据 Backend 已确认实现更新 ERD 和 data dictionary
- 整理 recipe、meal、place 和测试用户所需的非敏感样例数据
- 维护 backlog、Sprint 状态、会议决定和跨仓库 action list
- 将已冻结的 OpenAPI、模型包和私有契约版本登记到 docs
- 检查 proposal、presentation 与 canonical guide 的术语一致性

**减压边界**

- 不自行决定数据模型或产品范围。
- 发现冲突时列出差异，由项目负责人决定后再更新。
- 不处理生产数据或真实用户隐私信息。

**主要交付物**

- 最新 ERD/data dictionary
- 可合法使用的 seed/fixture 数据清单
- 每周状态页和决策记录

### 2.7 成员 D：演示与交付证据

**主责范围**

- 维护最终演示流程、讲稿、备用演示路径和时间控制
- 按统一命名规则整理工作功能截图和短视频
- 收集 CI、依赖扫描、secret scan、container scan、ZAP 与部署证据
- 编制功能—证据—提交版本索引
- 组织至少两次完整 demo rehearsal，并记录问题

**减压边界**

- 不负责搭建 CI/CD 或修复安全扫描问题；项目负责人提供运行入口和修复。
- 不要求解释模型算法或系统架构细节；相关内容由对应负责人提供。
- 不使用尚未运行成功的截图或虚构结果。

**主要交付物**

- 可在限定时间内完成的 demo script
- evidence index 和最终截图集
- rehearsal 问题清单与备用方案

## 3. 仓库主责矩阵

| 仓库 | 主责 | 协作 | 合并把关 |
| --- | --- | --- | --- |
| `foodmind-backend` | 项目负责人 | B 测试、C 文档 | 项目负责人 |
| `foodmind-web` | 项目负责人 | B 测试、D 演示证据 | 项目负责人 |
| `foodmind-android` | 成员 A | H 负责 Cooking Planner 页面协作、B 测试 | 项目负责人审查契约与高风险变更 |
| `foodmind-intelligence` | 项目负责人负责骨架/集成，H 负责 Cooking Planner | W 提供模型包 fixture、B 测试 | 项目负责人 |
| `foodmind-ml` | W | C 整理数据来源与文档 | 项目负责人审查契约和可复现性 |
| `foodmind-docs` | C | B、D 提供证据，所有负责人确认内容 | 项目负责人 |

主责人不等于独自完成全部工作。主责人负责拆 issue、说明验收条件、跟进阻塞和确认交付，项目负责人只在高风险或跨仓库问题上兜底。

## 4. 四周执行安排

### Sprint 1：冻结边界与建立可工作骨架

- 项目负责人：Backend/Web 骨架、认证最小链路、OpenAPI v0、数据库初版、Intelligence 接口骨架。
- H：冻结 Cooking Planner 输入输出 schema，准备 recipe fixtures 和 agent 最小实现。
- W：建立 ML 环境、数据 schema、baseline 和可重复运行命令。
- A：Android 骨架、登录和 API client。
- B：完成 UC-01 至 UC-09 验收用例初稿。
- C：完成 ERD 初稿、data dictionary 和 Sprint board。
- D：建立 evidence index、截图命名规则和 demo 大纲。

**退出条件：** 六个仓库均能执行基本检查；公共/私有契约有版本；每位成员至少有一个可验收 issue。

### Sprint 2：完成核心产品闭环

- 项目负责人：记录、群组、推荐 fallback、Web 主流程和基础 Dashboard。
- H：完成 Cooking Planner 正常路径和结构化输出测试。
- W：完成 UserCF、ItemCF 和特征 pipeline。
- A：完成记录、群组、推荐与反馈的 Android 常规页面。
- B：执行核心流程测试并提交可复现缺陷。
- C：更新 ERD/data dictionary，准备非敏感 seed data。
- D：收集可工作的核心流程证据并完善演示顺序。

**退出条件：** 至少能通过 Web 和 Android 各完成一条“登录—记录—推荐—反馈”链路。

### Sprint 3：Agents、ML 与完整功能接入

- 项目负责人：完成推荐/Chatbot 集成、模型推理接线、Web Cooking Planner 与 Chatbot 页面。
- H：完成 UC-06 边界场景，并协助 A 接入 Android Cooking Planner。
- W：完成 LR、评估对比、版本化模型包和 model card。
- A：完成 Cooking Planner、Chatbot、Dashboard Android 页面接入。
- B：覆盖 UC-04 至 UC-09、权限和 fallback 场景。
- C：登记契约版本，补齐 cross-repository action list。
- D：组织第一次完整 rehearsal，记录失败点和备用路径。

**退出条件：** UC-01 至 UC-09 均有可演示实现或明确缺陷；模型包可被 runtime consumer 验证。

### Sprint 4：集成、重工与提交

- 项目负责人：集中处理重工、权限、安全、跨仓库集成、staging 和最终发布。
- H：修复 Cooking Planner 缺陷，冻结 fixtures 与说明。
- W：复现实验、冻结模型版本，不再临时扩展算法。
- A：只修复 P0/P1 Android 缺陷和 parity 差异。
- B：完整回归并关闭 UAT。
- C：冻结 ERD、状态、traceability 和版本索引。
- D：完成最终演示材料、第二次 rehearsal 和证据归档。

**退出条件：** 演示路径在干净环境中跑通；关键证据带日期、环境和 commit；无未说明的 P0/P1 缺陷。

## 5. 协作与升级规则

### 日常协作

- 每个任务控制在半天至两天内可验收，避免出现“一人负责整个 App”这种不可追踪任务。
- Issue 必须包含负责人、输入、输出、验收条件、依赖和截止 Sprint。
- 每日异步更新只写三项：已完成、下一步、阻塞。
- 每周两次 20 分钟集成检查，只讨论跨仓库阻塞和即将到期的交付。

### 阻塞升级

1. 成员先用 30–45 分钟根据文档和现有测试定位问题。
2. 仍无法解决时，提交最小复现、日志和已尝试方法。
3. H 先处理 Cooking Planner 范围，W 先处理 ML 范围。
4. 只有契约、权限、部署、跨服务或持续阻塞的问题升级给项目负责人。

这能让项目负责人集中处理真正的重工，同时避免其他成员因复杂问题长期停滞。

### 变更控制

- Sprint 1 后冻结 MVP 范围；新增功能默认进入 backlog。
- Backend OpenAPI 由项目负责人维护，A/H/W 不直接做破坏性修改。
- ML 模型包由 W 产出，Intelligence 只按已登记的 contract 消费。
- Cooking Planner、Recommendation 和 Chatbot 保持三个独立入口。
- 所有宣称“已完成”的功能必须有运行证据，不以代码生成或页面截图代替集成结果。

## 6. 验收与个人贡献证据

每位成员至少保留以下三类证据：

1. **可追踪工作：** 自己负责的 issue、PR 或文档提交。
2. **可运行结果：** 测试记录、截图、评估输出或演示片段。
3. **个人说明：** 能用两分钟解释负责范围、关键选择和一个实际问题。

推荐的最终个人展示：

| 成员 | 最适合展示的内容 |
| --- | --- |
| 项目负责人 | 端到端架构、Backend/Web、权限与集成重工 |
| H | Cooking Planner 从请求到结构化结果 |
| W | ML pipeline、模型对比与可复现评估 |
| A | Android 主流程与跨客户端 parity |
| B | UAT 设计、缺陷复现和回归结果 |
| C | ERD、数据字典和版本/范围一致性 |
| D | 演示流程、证据索引和发布准备 |

## 7. 需要团队确认的事项

执行前只需要做三项确认：

1. 将成员 A、B、C、D 替换为真实姓名。
2. 确认 H 现有 Cooking Planner 代码所在仓库和当前完成度。
3. 确认每位成员每周实际可投入时间；若有人明显不足，优先缩减其页面数量或证据范围，不把其核心任务转嫁给 H 或 W。

除非 MVP 范围发生变化，这份计划不需要改变整体角色结构。
