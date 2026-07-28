# FoodMind 七人编码分工计划

**Status:** Proposed

**Owner:** Chen Yaqi

**Last updated:** 28 July 2026

**Formal baselines:** `Team5_AD_Project_Proposal.docx`,
`FoodMind_Presentation_Proposal.pptx`

**Related repositories:** `foodmind-backend`, `foodmind-web`,
`foodmind-android`, `foodmind-intelligence`, `foodmind-ml`,
`foodmind-docs`

**Open question:** 成员 A、B、C、D 仍是占位名称，确认真实姓名后只替换姓名，
不改变主要分工。

## 1. 核心分工

| 成员 | 核心编码范围 |
| --- | :--- |
| Chen Yaqi | Backend、Web and the rest |
| Huang Qijun | Cooking Planner 完整功能链 |
| Wu Aomo | 离线 ML pipeline、评估与模型包 |
| 成员 A | Android 基础框架、账户与偏好 |
| 成员 B | Android 食物记录与群组 |
| 成员 C | Android 推荐、反馈与 Dashboard |
| 成员 D | Android Cooking Planner 与 Chatbot |

这张表是主要分工的固定边界。最新 UX 构想只调整各范围内的实现重点：

- 推荐模式是 Android/Web 首页默认模式。
- Cooking 是同一首页顶层的第二个模式，但仍使用独立 Agent 链路。
- Groups 是核心共享功能。
- Explore 由现有群组可见内容和受控内容组成，不扩展为公开社交平台。
- Dashboard 仍在 MVP 内，但不再占据首页最强视觉优先级。

## 2. 分工原则

1. 七位成员都必须提交可构建、可运行、可解释的编码成果。
2. Chen Yaqi 承担跨仓库依赖最多的 Backend、Web、公共集成、DevOps、
   文档协调和重工。
3. Huang Qijun 与 Wu Aomo 分别对 Cooking Planner 和离线 ML 形成完整、
   可验收的纵向责任。
4. 成员 A 至 D 按 Android feature 切分，避免多人同时修改同一页面目录。
5. 测试、README、截图、fixture 和演示说明属于各功能的 Definition of
   Done，不单独形成“只写文档、不写代码”的岗位。
6. 公共 OpenAPI、权限规则、指标口径和 AI structured output 由对应仓库
   owner 冻结后供客户端消费，Android 不自行发明业务规则。

## 3. 具体责任

### 3.1 Chen Yaqi：Backend、Web and the rest

#### Backend

- Spring Boot 工程、数据库实体、Flyway migration 和公共 `/api/v1`
  OpenAPI。
- JWT、资源 ownership、群组 membership、`Private`/`Group` visibility。
- 账户、偏好、记录、历史、群组、`Want to Try`、推荐、反馈、Cooking、
  Chatbot、Dashboard 和 weekly recap 的业务 API。
- 推荐上下文聚合：个人历史、授权群组证据、预算、距离/区域、时间和
  dietary restrictions。
- 最多三个有差异的 ordered candidates；第一项为客户端 lead result。
- Explore 所需的 permission-aware group feed、authorised search 和 curated
  catalogue 组合，不引入公开 feed。

#### Web

- React/TypeScript 工程框架、鉴权、路由、API client 和共享组件。
- 顶层 **Eat out & delivery / Cooking** 模式切换。
- 默认推荐首页和醒目的 **Generate recommendation** 主按钮。
- lead recommendation、`try another`、feedback 和 share-to-group。
- Groups 核心共享页面。
- Xiaohongshu 风格但 permission-safe 的 Explore 帖子流。
- Saved、Me、Dashboard、weekly recap、Cooking 和 Chatbot 页面。
- responsive、keyboard、loading、empty、error、forbidden 和 fallback
  状态。

#### Intelligence、集成和交付

- `foodmind-intelligence` 公共 FastAPI 骨架、服务认证、Recommendation
  和 Chatbot 编排。
- Backend 到 Agent/inference 的 private client、timeout、validation 和
  fallback。
- Runtime model package 加载接线；不替代 Wu Aomo 的离线训练职责。
- Docker、CI/CD、staging、cloud、跨仓库 UAT 和高风险 PR 审查。
- 正式 Proposal/PPT 保持只读；其余系统文档、contract 和实现状态保持
  一致。

#### 边界

- 不接手成员 A 至 D 的常规 Android 页面。
- 不替 Huang Qijun 或 Wu Aomo 完成其已拆分且没有架构阻塞的日常代码。
- 只兜底跨仓库 contract、权限、数据库、部署和持续阻塞问题。

### 3.2 Huang Qijun：Cooking Planner 完整功能链

- Cooking Planner Agent、graph/state、tool allow-list 和 Pydantic schema。
- 受控 recipe catalogue、ingredient matching、预算/时间/dietary
  validation。
- 使用手动输入或已授权 pantry context；不实现自动库存识别或采购。
- 输出 ingredients、ordered steps、warnings、source recipe ID 和
  fallback status。
- 正常、有约束冲突、无匹配和服务失败的 fixtures/tests。
- 与 Chen Yaqi 冻结 Backend private contract，并向成员 D 提供稳定
  request/response fixtures。

**边界：** 不负责 Recommendation 排序、Chatbot、Android 页面或公共 API
设计。

### 3.3 Wu Aomo：离线 ML pipeline、评估与模型包

- 数据读取、validation、cleaning、feature generation 和
  train/evaluate CLI。
- Popularity/rule baseline、UserCF、ItemCF 和 Logistic Regression。
- 明确 acceptance/rejection/passive non-selection 的 label semantics。
- 评估 lead candidate 的 Top-1 表现，以及 ordered top-3 的 ranking、
  coverage 和 diversity。
- cold start、fallback、data leakage、reproducibility 和 limitations。
- immutable model package、manifest、checksum、feature schema、model card
  和 consumer fixtures。

**边界：** 不负责在线服务、Backend 接线、Agent graph 或客户端 UI。

### 3.4 成员 A：Android 基础框架、账户与偏好

- Compose 目标架构、Navigation、Retrofit/OkHttp、token/session 和通用
  UI state。
- 登录、注册、profile 和 preferences。
- Home/Groups/Explore/Saved/Me 导航框架。
- 顶层 **Eat out & delivery / Cooking** mode state 和可复用 shell。
- loading、empty、error、forbidden、offline 等基础组件。

**边界：** 不设计认证协议、Backend 权限模型或复杂业务规则。

### 3.5 成员 B：Android 食物记录与群组

- Food/drink record 列表、详情、创建、编辑、删除和历史筛选。
- 群组创建、加入、成员、group feed、active vote 和 share target。
- `Private`/`Group` visibility 与 `Want to Try`。
- Explore 的 Android 数据展示和帖子卡片；数据只能来自已授权 group
  feed/search/curated contracts。

**边界：** 不实现公开 follower feed、公共互联网搜索、数据库权限算法或
后端搜索逻辑。

### 3.6 成员 C：Android 推荐、反馈与 Dashboard

- 推荐模式默认首页、群组上下文、约束摘要和主 Generate 按钮。
- ordered candidate set 的 lead result 展示。
- `try another` 在同一 session 内切换其余 Personal、Exploratory、
  Group-inspired 候选。
- accept、reject、re-recommend、later rating 和 `Would Eat Again`。
- fallback、no-result、service unavailable 和 session recovery。
- Dashboard summary、Vico 图表和 weekly recap。

**边界：** 不在 Android 本地实现推荐算法、reason 推断或统计口径。

### 3.7 成员 D：Android Cooking Planner 与 Chatbot

- Cooking 模式的 pantry/ingredient、servings、time、budget、dietary
  输入。
- ingredients、ordered steps、warnings 和 source recipe 的结果页面。
- Chatbot conversation/message UI、source references、search、summary 和
  comparison 展示。
- Cooking 与 Chatbot 保持两个独立入口；Chatbot 不调用推荐或 Cooking。

**边界：** 不编写 Agent、prompt、搜索算法、summary 逻辑或自动库存
采集。

## 4. 仓库与模块主责矩阵

| 仓库/模块 | 编码主责 | 主要协作 |
| --- | --- | --- |
| `foodmind-backend` | Chen Yaqi | 所有成员提供 contract 反馈 |
| `foodmind-web` | Chen Yaqi | Huang/Wu 提供 fixtures |
| Android foundation、账户与偏好 | 成员 A | C/D 复用公共 shell |
| Android records、groups、Explore | 成员 B | A 提供网络/导航 |
| Android recommendation、feedback、Dashboard | 成员 C | A 提供公共组件，Wu 提供 fixtures |
| Android Cooking、Chatbot | 成员 D | A 提供公共组件，Huang 提供 Cooking fixtures |
| Intelligence 公共骨架、Recommendation、Chatbot | Chen Yaqi | Wu 提供模型包 |
| Intelligence Cooking Planner | Huang Qijun | Chen Yaqi 负责服务接线 |
| `foodmind-ml` | Wu Aomo | Chen Yaqi 确认 consumer contract |
| `foodmind-docs` 与跨仓库交付 | Chen Yaqi | 各成员维护自己功能的证据 |

Android feature packages：

```text
feature/
├── account/          # A
├── records/          # B
├── groups/           # B
├── explore/          # B
├── recommendation/   # C
├── dashboard/        # C
├── cooking/          # D
└── chatbot/          # D
```

成员 A 应尽早冻结 `core/network`、`core/navigation`、app shell 和通用 UI
接口。公共组件变更必须说明使用场景并由受影响成员 review。

## 5. 四周安排

### Sprint 1：骨架与 contract

- Chen Yaqi：Backend/Web/Intelligence 骨架、数据库、认证、OpenAPI v0 和
  两模式 Web shell。
- Huang Qijun：Cooking schema、recipe fixtures 和最小 Agent。
- Wu Aomo：ML 环境、数据 schema、baseline 和 CLI 骨架。
- A：Android 网络、导航、session 和两模式 shell。
- B：records/groups/explore package 与 mock UI。
- C：recommendation/dashboard package、lead-result mock UI。
- D：cooking/chatbot package 与 mock UI。

### Sprint 2：核心 vertical slice

- Chen Yaqi：记录、群组、permission-safe Explore source、推荐 fallback、
  Web 核心链和 Android API。
- Huang Qijun：Cooking 正常路径和 structured output。
- Wu Aomo：UserCF、ItemCF 和 feature pipeline。
- A：账户/偏好与公共组件。
- B：记录 CRUD、群组、Explore 和 `Want to Try`。
- C：Generate、lead result、accept/reject 和 try-another。
- D：Cooking Android 接入和 Chatbot conversation UI。

### Sprint 3：Agents、ML 与完整接入

- Chen Yaqi：Recommendation/Chatbot、runtime inference、Web 全功能和
  跨服务集成。
- Huang Qijun：Cooking fallback、约束验证和 UC-06 联调。
- Wu Aomo：LR、评估、model package 和 consumer fixture。
- A：session recovery、导航和公共组件稳定。
- B：群组 visibility、Explore 权限状态和缺陷修复。
- C：Dashboard、weekly recap 和推荐 fallback UI。
- D：Chatbot search/summary/comparison、references 和错误状态。

### Sprint 4：联调与冻结

- Chen Yaqi：权限、安全、部署、UAT、跨仓库重工和最终合并。
- Huang Qijun：冻结 Cooking schema/fixtures。
- Wu Aomo：复现实验并冻结模型版本。
- A 至 D：修复各自主责模块 P0/P1 问题并准备个人演示证据。

## 6. Definition of Done

每个成员负责的 issue 必须同时满足：

- 代码通过仓库现有 build/lint/test。
- 至少覆盖一个正常场景和一个错误、空数据或 fallback 场景。
- API 使用登记过的 contract，不硬编码 secret、生产地址或未定义字段。
- PR 说明包含范围、运行方式、截图/实际输出和 contract 版本。
- 功能 owner 可以说明主要类、数据流、权限边界和一个遇到的问题。
- 与正式 Proposal/PPT 的 scope 一致；发现冲突时先停止并升级，不直接改
  正式文件。

## 7. 协作规则

1. Issue 控制在半天至两天内可验收。
2. Contract、权限、数据库、部署和跨服务问题升级给 Chen Yaqi。
3. Cooking 问题先找 Huang Qijun；ML 问题先找 Wu Aomo。
4. Sprint 1 后冻结公共 MVP 范围；新增功能默认进入 backlog。
5. Recommendation、Cooking 和 Chatbot 保持三个独立 AI workflow。
6. Explore 不创建新的 public visibility 或 public-search contract。
7. “代码已生成”不等于完成，必须能够构建、运行和解释。

## 8. 个人贡献验收

| 成员 | 最终个人编码展示 |
| --- | --- |
| Chen Yaqi | Backend/Web、推荐首页、权限、服务集成和部署 |
| Huang Qijun | Cooking Planner schema、Agent、fallback 和 structured result |
| Wu Aomo | ML pipeline、Top-1/Top-3 评估和可复现模型包 |
| 成员 A | Android shell、登录、profile、偏好和公共网络/导航 |
| 成员 B | Android records、groups、Explore 和 `Want to Try` |
| 成员 C | Android recommendation、feedback、Dashboard 和图表 |
| 成员 D | Android Cooking、Chatbot 和 source references |

每人需要保留连续提交、对应 issue/PR、构建或测试结果、运行截图，以及约
两分钟的个人说明。
