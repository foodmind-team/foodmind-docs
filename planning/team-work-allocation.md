# FoodMind 七人编码分工计划

**Status:** Proposed
**Owner:** 项目负责人
**Last updated:** 28 July 2026
**Related repositories:** `foodmind-backend`, `foodmind-web`, `foodmind-android`, `foodmind-intelligence`, `foodmind-ml`, `foodmind-docs`
**Related scope:** UC-01 至 UC-09、四周 MVP 交付计划
**Open questions:** 以成员 A、B、C、D 暂代尚未提供姓名的四位成员；执行前替换为真实姓名

## 1. 分工原则

本计划要求七位成员都有可运行、可提交、可说明的编码成果，不设置专职测试、文档或演示岗位。

整体安排如下：

1. 项目负责人承担工作量最大、跨仓库依赖最多的 Backend、Web、系统集成和重工。
2. H 与 W 是第二梯队负责人，工作量略低于项目负责人，但明显高于其余四人。
3. 其余四位成员按业务功能拆分 Android，实现范围清楚，主要完成页面、状态管理和已冻结 API 的接入，不要求独立处理复杂后端或架构问题。
4. 测试、README、截图和演示说明属于每个编码任务的 Definition of Done，由功能开发者随代码一起完成。

建议的相对负荷为：

| 成员 | 相对负荷 | 核心编码范围 |
| --- | ---: | --- |
| 项目负责人（你） | 100% | Backend、Web、Intelligence 公共骨架、集成与重工 |
| H | 80%–85% | Cooking Planner 完整功能链 |
| W | 75%–80% | 离线 ML pipeline、评估与模型包 |
| 成员 A | 45%–50% | Android 基础框架、账户与偏好 |
| 成员 B | 45%–50% | Android 食物记录与群组 |
| 成员 C | 45%–50% | Android 推荐、反馈与 Dashboard |
| 成员 D | 45%–50% | Android Cooking Planner 与 Chatbot |

百分比表示相对投入强度，不等同于精确工时。成员 A 至 D 的功能虽然不同，但应控制在相近的页面数量和 story points。

## 2. 七人具体分工

### 2.1 项目负责人（你）：技术负责人、Backend/Web 主力与重工兜底

**主要编码职责**

- `foodmind-backend`
  - Spring Boot 工程结构、数据库实体与 migration
  - 身份认证、JWT、权限和群组可见性
  - UC-01 至 UC-05、UC-09 的业务 API
  - Recommendation、Cooking Planner 和 Chatbot 的公共 API
  - Dashboard/weekly recap 的统一指标计算
  - OpenAPI、异常响应、超时、重试和 fallback
- `foodmind-web`
  - React 工程框架、鉴权、路由、API client 和共享组件
  - UC-01 至 UC-09 的 Web 端 MVP 页面
  - loading、empty、error、permission denied 等状态
- `foodmind-intelligence` 与系统集成
  - FastAPI 公共骨架、服务认证和 private contract
  - Recommendation 与 Chatbot 的核心编排
  - Runtime inference 接线与模型包加载
  - Backend 到 Intelligence 的 client、timeout 和 fallback
- 重工与交付
  - 跨仓库接口调整、复杂权限问题和数据库返工
  - Docker、CI/CD、staging 和端到端联调
  - 高风险 PR 审查和最终合并把关

**主要交付物**

- 可部署的 Backend、Web 和 Intelligence 集成版本
- 冻结的公共 OpenAPI 与关键私有契约
- Web/Android 使用同一 Backend 的完整 MVP
- 推荐、Cooking Planner、Chatbot 三条独立调用链

**负荷保护**

- 不接手成员 A 至 D 的常规 Android 页面。
- 不替 H/W 完成其已拆分且没有架构阻塞的日常代码。
- 只兜底跨仓库、权限、部署、契约和持续阻塞的问题。

### 2.2 H：Cooking Planner 功能负责人

H 继续负责已经开始的 Cooking Planner，并交付一条完整功能链，而不是只完成 prompt 或单个页面。

**主要编码职责**

- `foodmind-intelligence`
  - Cooking Planner Agent
  - 受控 recipe catalogue 读取
  - ingredient matching
  - 时间、预算、dietary restrictions 校验
  - ingredients、ordered steps、warnings、source recipe ID 的结构化输出
  - 无匹配和限制冲突的可预测 fallback
- 与项目负责人对接 Backend private contract
- 为成员 D 提供稳定的 request/response fixtures
- 协助定位 Android Cooking Planner 接入问题，但不代替成员 D 编写全部 UI

**主要交付物**

- UC-06 可运行链路
- 至少 10 个 recipe fixtures
- 正常、无匹配、限制冲突三类可运行样例
- Cooking Planner schema、实现代码和自动化检查

**边界**

- 不负责 Recommendation 排序或 Chatbot。
- 不直接修改公共 API；需要变更时先与项目负责人确认。
- 不生成无来源或无法验证的食品安全结论。

### 2.3 W：ML 功能负责人

W 主责 `foodmind-ml`。考虑到 W 的手写代码能力有限但会合理使用 AI，工作按小 issue 拆分，并以实际运行结果验收。

**主要编码职责**

- 数据读取、清洗、feature generation 和 train/evaluate CLI
- Popularity/rule baseline
- cosine-similarity UserCF 与 ItemCF
- Logistic Regression 排序模型
- Precision@K、Recall@K、NDCG@K、coverage、diversity 计算
- 版本化模型包、feature schema 和训练配置
- 固定随机种子、依赖锁定和可重复运行脚本

**AI 辅助开发规则**

- 每次只让 AI 处理一个可验证的小任务，例如一个 transformer、metric 或 test fixture。
- AI 代码必须能说明输入、输出、异常条件和数据 shape。
- 合并前必须实际运行 pipeline，不能只依赖 AI 对代码的解释。
- 模型指标和实验结论必须来自真实输出，禁止让 AI 补写不存在的结果。
- 项目负责人审查 contract、可复现性和上线风险，不接管 W 的普通实现。

**主要交付物**

- 一条命令可执行的训练与评估 pipeline
- baseline、UserCF、ItemCF、LR 的实际对比结果
- 可被 Intelligence 验证和加载的版本化模型包
- model card 与最小 consumer fixture

**边界**

- W 不负责在线服务部署或 Backend 接线。
- 矩阵分解、深度学习和复杂 MLOps 不进入四周 MVP。

### 2.4 成员 A：Android 基础框架、账户与偏好

成员 A 负责 Android 的公共基础和 UC-01，给其他 Android 成员提供稳定的开发入口。

**主要编码职责**

- Compose Navigation 和页面框架
- Retrofit/OkHttp API client 的基础配置
- token 保存、登录状态和 logout
- 注册、登录、个人资料和 dietary preference 页面
- 通用 loading、empty、error UI 组件
- 基础主题和可复用表单组件

**主要交付物**

- 可运行的注册—登录—资料修改链路
- 其他 Android 功能可以复用的导航、网络和状态组件
- 账户模块的基础 ViewModel 与代码级检查

**减压边界**

- 不设计认证协议或 Backend 权限模型。
- API 不一致时提供请求、响应和日志，由项目负责人修改 contract 或 Backend。
- 不做复杂动画和非 MVP 设计系统。

### 2.5 成员 B：Android 食物记录与群组

成员 B 负责 UC-02 和 UC-03，基于成员 A 的公共组件实现常规 CRUD 与列表功能。

**主要编码职责**

- Food/drink record 的列表、详情、创建、编辑和删除
- 基础搜索与筛选
- 群组创建、加入、成员列表和 group feed
- `Want to Try` 保存与列表
- 私有、群组可见等状态的 UI 展示

**主要交付物**

- 可运行的记录 CRUD
- 可运行的群组 feed 与 `Want to Try`
- 对 loading、empty、error、permission denied 的页面处理

**减压边界**

- 不实现数据库、群组权限算法或搜索后端。
- 图片上传若影响主流程，可先使用 URL/placeholder，再由项目负责人决定是否纳入。
- 只消费冻结的 OpenAPI，不自行发明 response fields。

### 2.6 成员 C：Android 推荐、反馈与 Dashboard

成员 C 负责 UC-04、UC-05 和 UC-09 的 Android 展示层。计算和推荐逻辑全部由 Backend/Intelligence 提供。

**主要编码职责**

- 三张推荐卡片及 explanation/reason code 展示
- accept、reject、re-recommend 和 post-meal rating
- recommendation session 状态恢复
- Dashboard summary cards
- 使用 Vico 渲染后端返回的基础图表数据
- weekly recap 页面

**主要交付物**

- 可运行的“生成推荐—反馈—重新推荐”链路
- Dashboard 与至少两种基础图表
- 无推荐、fallback 和服务暂不可用状态

**减压边界**

- 不实现推荐算法或在 Android 本地重复计算指标。
- 不设计新的图表统计口径。
- 图表样式以清晰可读为目标，不做复杂交互。

### 2.7 成员 D：Android Cooking Planner 与 Chatbot

成员 D 负责 UC-06、UC-07 和 UC-08 的 Android 展示层，输入输出均使用项目负责人/H 提供的固定 contract。

**主要编码职责**

- Cooking Planner 请求表单
- ingredients、ordered steps、warnings 的结果页面
- Chatbot conversation list 与 message UI
- 发送消息、查看 source references、打开共享内容
- Chatbot search、summary、comparison 结果的基础展示

**主要交付物**

- Android Cooking Planner 请求—结果链路
- Android Chatbot 发送—回复—来源查看链路
- Cooking 与 Chatbot 两个独立入口

**减压边界**

- 不编写 Agent、prompt、搜索算法或 summary 逻辑。
- 不支持复杂富文本编辑、语音聊天或 streaming。
- Contract 或 Agent 结果异常时保存完整响应并交由 H/项目负责人处理。

## 3. 仓库与模块主责矩阵

| 仓库/模块 | 编码主责 | 代码协作 | 最终把关 |
| --- | --- | --- | --- |
| `foodmind-backend` | 项目负责人 | 各成员提供所需 contract 反馈 | 项目负责人 |
| `foodmind-web` | 项目负责人 | H/W 提供 fixture | 项目负责人 |
| Android foundation、UC-01 | 成员 A | C/D 复用公共组件 | 项目负责人审查高风险部分 |
| Android UC-02、UC-03 | 成员 B | A 提供网络/导航组件 | 项目负责人审查 contract |
| Android UC-04、UC-05、UC-09 | 成员 C | A 提供公共组件，W 提供 fixture | 项目负责人审查 contract |
| Android UC-06、UC-07、UC-08 | 成员 D | A 提供公共组件，H 提供 Cooking fixture | 项目负责人审查 contract |
| Intelligence 公共骨架、Recommendation、Chatbot | 项目负责人 | W 提供模型包 | 项目负责人 |
| Intelligence Cooking Planner | H | 项目负责人负责服务接线 | 项目负责人 |
| `foodmind-ml` | W | 项目负责人确认 consumer contract | 项目负责人 |

四位 Android 成员使用 feature-based packages，避免多人同时修改同一个页面目录：

```text
feature/
├── account/          # A
├── records/          # B
├── groups/           # B
├── recommendation/   # C
├── dashboard/        # C
├── cooking/          # D
└── chatbot/          # D
```

成员 A 负责的 `core/network`、`core/navigation` 和通用 UI 需要尽早冻结接口。其他成员若需要修改公共组件，应先说明使用场景，避免四人并行时产生频繁冲突。

## 4. 四周编码安排

### Sprint 1：骨架与第一条请求

- 项目负责人：Backend/Web/Intelligence 骨架、数据库初版、认证最小链路和 OpenAPI v0。
- H：Cooking Planner schema、recipe fixtures 和 agent 最小实现。
- W：ML 环境、数据 schema、baseline 和 CLI 骨架。
- A：Android 导航、网络、登录状态和登录页面。
- B：records/groups feature package、列表页面和 mock ViewModel。
- C：recommendation/dashboard feature package、推荐卡片 mock UI。
- D：cooking/chatbot feature package、表单和 message mock UI。

**退出条件：** 七个人均有可运行的代码提交；Android 四个功能区可以独立打开；关键 contract 已有版本。

### Sprint 2：核心功能链

- 项目负责人：记录、群组、推荐 fallback、Web 核心流程和 Android 所需 API。
- H：Cooking Planner 正常路径和结构化输出。
- W：UserCF、ItemCF 和 feature pipeline。
- A：注册、登录、profile、preference 与 token handling。
- B：记录 CRUD、筛选、群组和 `Want to Try`。
- C：推荐、accept/reject 和 re-recommend。
- D：Cooking Planner Android 接入和 Chatbot conversation UI。

**退出条件：** Android/Web 均能完成“登录—记录—推荐—反馈”的基础链路；Cooking Planner 有首个端到端结果。

### Sprint 3：Agents、ML 与完整接入

- 项目负责人：Chatbot、runtime inference、Web 全功能与服务间集成。
- H：Cooking Planner fallback、限制校验和 UC-06 联调。
- W：LR、评估、模型包和 consumer fixture。
- A：公共组件稳定、认证异常状态和 session 恢复。
- B：群组可见性状态与 records/groups 缺陷修复。
- C：Dashboard、Vico 图表、weekly recap 和 fallback UI。
- D：Chatbot 搜索/summary/comparison、source references 和错误状态。

**退出条件：** UC-01 至 UC-09 均可从至少一个客户端运行；Android 功能接近 parity；模型包可被 Intelligence 验证。

### Sprint 4：联调、重工与冻结

- 项目负责人：集中处理跨仓库重工、权限、安全、staging、部署和最终合并。
- H：修复 Cooking Planner 缺陷并冻结 schema/fixtures。
- W：复现实验并冻结模型版本，不再增加新算法。
- A：修复账户和公共组件问题，协助解决 Android merge conflicts。
- B：修复 records/groups 的 P0/P1 问题。
- C：修复 recommendation/dashboard 的 P0/P1 问题。
- D：修复 cooking/chatbot Android 的 P0/P1 问题。

**退出条件：** 干净环境可构建；演示主路径可运行；每个人负责的模块都有代码、基本检查和个人讲解材料。

## 5. 每个编码任务的完成标准

测试和交付工作不单独分配给某个人，而是随功能一起完成。一个 issue 只有同时满足以下条件才算完成：

- 功能代码已提交并通过仓库现有 lint/build。
- 至少覆盖一个正常场景和一个错误/空数据场景。
- API 调用使用已登记的 contract，没有硬编码 secret 或生产地址。
- 复杂逻辑有最小自动化检查；纯 UI 至少有可复现的手动检查步骤。
- PR 说明包含功能范围、运行方法、截图或实际输出。
- 开发者可以解释自己的主要类、数据流和一个遇到的问题。

测试工作的落点如下：

| 功能 | 谁写代码 | 谁完成该功能的基本检查 |
| --- | --- | --- |
| Backend/Web/集成 | 项目负责人 | 项目负责人 |
| Cooking Planner Agent | H | H |
| ML pipeline | W | W |
| Android 账户与公共组件 | A | A |
| Android 记录与群组 | B | B |
| Android 推荐与 Dashboard | C | C |
| Android Cooking 与 Chatbot | D | D |

最终联调时可以互相做一次交叉 smoke check，但这不构成独立岗位，也不替代开发者对自己代码的责任。

## 6. 协作与减压规则

### 小任务拆分

- 每个 issue 应控制在半天至两天可交付。
- 每个 issue 写清输入、输出、依赖和验收条件。
- A 至 D 优先做页面、ViewModel、API mapping 和状态处理，不把复杂服务逻辑下放到客户端。
- H/W 的工作也拆为 schema、fixture、单个组件、集成四类 issue，避免一次生成整套系统。

### 阻塞升级

1. 成员先根据 contract、fixture 和日志定位 30–45 分钟。
2. 无法解决时提交最小复现、请求/响应和已尝试方法。
3. Cooking Planner 问题先找 H，ML 问题先找 W。
4. Contract、权限、部署、数据库和跨服务问题直接升级给项目负责人。

### 变更控制

- Sprint 1 后冻结 MVP，新增功能默认进入 backlog。
- 公共 OpenAPI 由项目负责人维护。
- Android 不自行实现业务规则、推荐算法或统计口径。
- Cooking Planner、Recommendation 和 Chatbot 保持三个独立入口。
- “代码已生成”不等于完成，必须能够构建和运行。

## 7. 个人贡献验收

每位成员最终都应具备以下贡献证据：

1. 至少一个自己主责的 feature package、service 或 pipeline。
2. 连续、可解释的代码提交和对应 issue。
3. 可运行页面、API 输出或模型评估结果。
4. 自己负责功能的基本检查记录。
5. 两分钟个人说明：负责了什么、数据如何流动、解决了什么问题。

推荐的个人展示内容：

| 成员 | 个人编码展示 |
| --- | --- |
| 项目负责人 | Backend/Web、权限、服务集成和重工 |
| H | Cooking Planner 的 schema、Agent 和结构化结果 |
| W | ML pipeline、模型对比和可复现模型包 |
| A | Android 登录、profile 和公共网络/导航组件 |
| B | Android 记录 CRUD、群组和 `Want to Try` |
| C | Android 推荐反馈、Dashboard 和图表 |
| D | Android Cooking Planner、Chatbot 和来源展示 |

## 8. 执行前确认

开始执行前只需确认：

1. 将成员 A、B、C、D 替换为真实姓名。
2. 检查四位 Android 成员的 Kotlin/Compose 基础；若差距较大，只调整各自页面数量，不改变“每个人都编码”的原则。
3. 确认 H 当前 Cooking Planner 代码所在仓库和已完成部分。
4. 确认 W 能在本地运行 Python 环境和最小数据集。

除非 MVP 范围或成员可用时间发生明显变化，整体角色结构无需调整。
