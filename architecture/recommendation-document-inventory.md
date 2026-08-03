# Recommendation and Agent Documentation Inventory

- **Status:** Proposed
- **Owner:** Chen Yaqi / recommendation workstream
- **Last updated:** 3 August 2026
- **Related repositories:** `foodmind-docs`, `foodmind-backend`, `foodmind-intelligence`, `foodmind-ml`, `foodmind-web`, `foodmind-android`
- **Related contract/ADR:** `recommendation-agent-v1`, `recommendation-features-v1`; v2 contracts proposed in [Recommendation System Implementation Design](recommendation-system-implementation-design.md)
- **Open questions:** Dataset approval and licence; model-key rotation owner; minimum launch data; final v2 contract acceptance

## Purpose and audit basis

This inventory locates the documents that define, constrain, implement, or consume FoodMind's machine-learning recommendation flow and associated Recommendation Agent. It also records discrepancies found by comparing those documents with the repositories as they existed on 3 August 2026.

The audit used these fetched remote revisions:

| Repository | Audited remote revision | Relevant implementation state |
| --- | --- | --- |
| `foodmind-docs` | `origin/main` at `5e658cc` | Formal baselines, canonical guide, governance, and planning artifacts exist |
| `foodmind-backend` | `origin/master` at `19fe13a` | Recommendation orchestration, fallback, Agent adapter, feedback, and training export exist |
| `foodmind-intelligence` | `origin/main` at `87e1d76` | Shared runtime and Cooking Agent exist; Recommendation Agent/inference directories remain placeholders |
| `foodmind-ml` | `origin/main` at `062ba13` | Repository and release workflow scaffolding exist; no recommender training code exists |

The Backend code inspection used the clean code at local revision `7ea2b90`. The twelve newer remote commits are Cooking-path changes; the recommendation implementation described here is unchanged by that delta. The formal DOCX, all twelve presentation slides, and all four workbook sheets were inspected, not only their filenames.

## Authority order

When sources disagree, apply the repository's documented order:

1. Formal Proposal for scope and requirements.
2. Formal presentation for the approved narrative and architecture summary.
3. Explicit owner clarification that does not expand the formal MVP.
4. Accepted ADR.
5. Canonical AI context guide.
6. Versioned contracts.
7. ERD and data dictionary.
8. Historical plans and status reports.

The frozen Proposal and presentation are not edited to hide contradictions. A current design must identify and resolve them explicitly.

## Primary product and architecture sources

| Repository and path | Role | Recommendation/Agent content | Audit conclusion |
| --- | --- | --- | --- |
| `foodmind-docs/Team5_AD_Project_Proposal.docx` | Frozen primary scope baseline | Defines hybrid UserCF + ItemCF + logistic-regression ranking, cold-start preference/context features, acceptance prediction, and explanation through an Agent | Authoritative MVP algorithm. Preserve unchanged. |
| `foodmind-docs/FoodMind_Presentation_Proposal.pptx` | Frozen presentation baseline | Slides 8-10 show hard rules, UserCF, ItemCF, context, logistic regression, a five-Agent concept, an ML service, and Yelp Open Dataset as a starting dataset | Useful architecture summary. Dataset use still needs approval, provenance, licence review, and a documented proxy-label mapping. |
| `foodmind-docs/FoodMind_AI_Project_Context_and_Tutoring_Guide.md` | Canonical implementation guide | Reconciles product scope, hybrid ranking, three result types, dedicated Recommendation Agent, logical Agent/inference services, training ownership, contracts, feedback, evaluation, and fallback | Most complete current design source. This design adopts it where the frozen visual material is ambiguous. |
| `foodmind-docs/README.md` | Governance and topology index | Defines six repository boundaries, source-of-truth order, latest recommendation UX, contract ownership, required evidence, and change workflow | Governs placement and ownership of the new artifacts. |
| `foodmind-docs/architecture/decisions/document-governance.md` | Accepted governance decision | Defines owners and propagation rules for Agent, inference, model-feature, database, and public API changes | Requires coordinated v2 contract changes in Backend, Intelligence, ML, and Docs. |
| `foodmind-docs/planning/team-work-allocation.md` | Delivery ownership | Assigns the recommendation, Intelligence, ML, data, quality, and documentation work across the team | Planning input, not an implementation-status source. |
| `foodmind-docs/planning/status/FoodMind_Prioritisation_Strategy_and_Project_Status_Report.xlsx` | Prioritisation and status snapshot | Features, process, technology, and project-status sheets identify recommendation and AI/ML work | Dated 28 July 2026. Its claim that fallback, feedback, and export were not implemented is now stale relative to Backend code. |

## Backend implementation sources

| Repository and path | What it defines | Current status or limitation |
| --- | --- | --- |
| `foodmind-backend/README.md` | Backend role, module boundaries, integrations, and local execution | Supporting entry point. |
| `foodmind-backend/docs/planning/branches/10-recommendation-fallback.md` | Candidate retrieval, hard filters, session persistence, deterministic fallback, and tests | Implemented substantially. |
| `foodmind-backend/docs/planning/branches/11-recommendation-agent.md` | Agent request/response, timeout, validation, fallback, and reason handling | Implemented for `recommendation-agent-v1`. |
| `foodmind-backend/docs/planning/branches/12-recommendation-feedback.md` | Explicit feedback, re-recommendation, labels, feature snapshots, and export | Implemented substantially, including snapshot export. |
| `foodmind-backend/src/test/resources/contracts/agent/recommendation/contract-notes.md` | Executable v1 Agent contract notes and fixture semantics | Canonical Backend-side v1 consumer evidence. |
| `foodmind-backend/src/test/resources/contracts/agent/recommendation/*.json` | Success, unknown-candidate, and inference-unavailable fixtures | Must remain during a v1/v2 compatibility window. |
| `foodmind-backend/src/test/resources/fixtures/public/recommendation/*` | Public fallback response fixture and manifest | Public response coordination evidence. |
| `foodmind-backend/src/main/resources/openapi/openapi.yaml` | Canonical public recommendation and feedback API | Public contract can remain stable while private v2 contracts are introduced. |
| `foodmind-backend/docs/api/conventions.md` | Public error, idempotency, correlation, pagination, and contract conventions | Applies to recommendation endpoints. |
| `foodmind-backend/docs/architecture/overview.md` | Modular-monolith overview and integration boundary | Its older framework-only status statement is stale for recommendation. |
| `foodmind-backend/docs/architecture/backend-development-plan.md` | Planned backend sequencing and boundaries | Historical planning context; code is stronger evidence. |
| `foodmind-backend/docs/database/postgresql-schema-guide.md` | Database ownership and schema conventions | Governs recommendation migrations and data protection. |
| `foodmind-backend/src/main/resources/db/migration/V7__recommendations.sql` | Recommendation sessions, candidate snapshots, reasons, and feedback schema | Implemented persistence base. Training-export database objects are added by `V10__cross_cutting_and_analytics.sql` on the audited branch. |
| `foodmind-backend/docs/operations/local-development.md` | Local services and verification expectations | Explains PostgreSQL/Testcontainers requirements for integration tests. |
| `foodmind-backend/docs/planning/branches/17-cloud-security-uat.md` | Security and end-to-end evidence expectations | Applies to the private Agent boundary, fallbacks, and release evidence. |

The current implementation is also the decisive source for behavior. The principal code locations are:

- `recommendation/application/GenerateRecommendation.java`
- `recommendation/application/RecommendationTransactionService.java`
- `recommendation/infrastructure/persistence/JdbcRecommendationContextQuery.java`
- `recommendation/domain/filter/*`
- `recommendation/domain/fallback/FallbackSelector.java`
- `recommendation/domain/AgentResultValidator.java`
- `integration/agent/RecommendationAgentHttpAdapter.java`
- `recommendation/application/BuildTrainingSnapshot.java`
- `recommendation/infrastructure/export/*`

## Intelligence runtime sources

| Repository and path | What it defines | Audit conclusion |
| --- | --- | --- |
| `foodmind-intelligence/README.md` | Private Agent and inference service ownership, repository layout, contracts, and workflow separation | Correct target repository; recommendation directories are still placeholders. |
| `foodmind-intelligence/docs/architecture/runtime-architecture.md` | Logical service split, trust boundary, orchestration, model loading, observability, and fallback expectations | Governs the proposed Agent/inference implementation. |
| `foodmind-intelligence/docs/operations/model-consumption.md` | Immutable package validation, readiness, activation, rollback, and no-runtime-training rule | Governs model promotion and consumption. |

Cooking Agent code on current `origin/main` is a useful production pattern for structured state, internal authentication, and observability. It is not a recommendation algorithm and must not become a shared conversation route for recommendations.

## ML repository sources

| Repository and path | What it defines | Audit conclusion |
| --- | --- | --- |
| `foodmind-ml/README.md` | Offline-only repository responsibility, suggested package layout, reproducibility, and separation from runtime | Correct producer boundary; implementation remains empty. |
| `foodmind-ml/docs/experiments/training-workflow.md` | Snapshot ingestion, validation, splitting, baselines, training, evaluation, packaging, and reproducibility | Sound workflow skeleton; this design supplies recommendation-specific details. |
| `foodmind-ml/docs/model-cards/model-release-process.md` | Required metrics, limitations, approvals, manifest, checksums, and release status | Governs acceptance of an immutable recommendation model package. |

## Client and integration consumers

These documents contain recommendation behavior or contracts but do not define the algorithm:

| Repository | Related documents | Relevance |
| --- | --- | --- |
| `foodmind-web` | `README.md`, `docs/architecture/frontend-architecture.md`, `docs/planning/backend-api-integration-plan.md`, `docs/planning/web-frontend-development-plan.md`, `docs/ux/README.md`, `contracts/backend-openapi-v1.yaml`, local/testing delivery plans | Consume the ordered set, display one lead result, support “try another,” and submit feedback. The copied OpenAPI must record its Backend source revision. |
| `foodmind-android` | `README.md`, `docs/architecture/android-architecture.md`, `docs/ux/README.md`, `docs/operations/local-development.md` | Consume the same public contract and preserve Web/Android parity. |
| `foodmind-docs/operations/local/integration-workspace.md` | Six-repository local integration setup | Supports end-to-end verification without creating a monorepo. |

## Adjacent workflow boundary documents

The Cooking Agent delivery-plan set under `foodmind-docs/planning/cooking-plan-agent-fullstack-plan/` and Backend branch plans for Cooking and Chat are relevant only because they enforce three separate entry points:

- Recommendation: bounded candidate ranking and grounded reasons.
- Cooking: structured recipe/plan generation.
- Chatbot: search and summary over authorised references.

They must not share a user-visible conversation or silently route a recommendation through Chat.

## Reconciled decisions and discrepancies

| Finding | Evidence | Resolution in the implementation design |
| --- | --- | --- |
| Presentation use-case visual can be read as asking the chatbot for a recommendation | Presentation slide 6 versus Proposal prose and canonical guide | Follow the higher-detail sources: recommendation remains a dedicated endpoint and Recommendation Agent workflow. Record the frozen-slide inconsistency; do not silently edit it. |
| Presentation combines “five Agents” and “hybrid ML” at a high level | Slides 9-10 and canonical guide | Treat them as five logical workflows with two private logical services: Agent orchestration and inference. Offline training remains in `foodmind-ml`. |
| Yelp is named as a starting dataset | Presentation slide 8 | Allow only a documented bootstrap experiment. FoodMind explicit feedback is the production training source. Dataset licence, provenance, mapping, and domain mismatch must appear in the model card. |
| Status workbook says recommendation backend capabilities are missing | Workbook dated 28 July 2026 versus Backend code and history | Mark the workbook status as stale; do not reclassify implemented Backend work as missing. |
| Backend overview says framework only | Overview text versus implemented recommendation package | Update that overview in a Backend-owned follow-up. The cross-system design records the actual state. |
| Documented candidate sources include user/group history and seed catalog | Canonical guide versus `JdbcRecommendationContextQuery` | Current query ranks active curated `place_meal` offerings and uses personal/group history as evidence. Phase 1 must either register historical offerings in that catalog or implement an authorised catalog union explicitly. |
| “Missing evidence is not proof of safety” | Canonical guide versus permissive missing allergen evidence | Make allergen/dietary evidence completeness explicit and fail closed where the user has a safety constraint. |
| UserCF and ItemCF reasons are supported by proxy counters | `AgentResultValidator` and fallback renderer | v2 requires distinct CF score/availability/evidence fields; group counts cannot substantiate “similar users.” |
| `recommendation-features-v1` lacks CF and several context features | Backend feature snapshot/export | Add a versioned v2 schema; keep v1 readable for rollback and reproducibility. |
| Integration tests fail on this workstation | Test reports | Pure unit/adapter tests pass; database-backed tests require a working Docker/Testcontainers environment and must run in CI or a prepared local environment. |

## Documents to create or update during delivery

The following artifacts do not yet exist as accepted contracts and are required before implementation crosses repository boundaries:

- Accepted ADR for recommendation v2 contracts, model keys, and compatibility policy.
- `recommendation-agent-v2` schema and examples owned by `foodmind-intelligence`.
- `recommendation-inference-v1` schema and examples owned by `foodmind-intelligence`.
- `recommendation-features-v2` schema owned jointly through producer/consumer contract tests.
- Model-package manifest schema and example release.
- Compatibility matrix covering Backend Agent contract, inference contract, feature schema, key version, and model package.
- Recommendation sequence, trust-boundary, and training-to-release diagrams.
- Model card and reproducibility report for every promoted package.
- UAT traceability for normal, cold-start, no-candidate, timeout, invalid-response, fallback, feedback, and “try another” paths.

The architecture and execution details are in [Recommendation System Implementation Design](recommendation-system-implementation-design.md) and [Recommendation System Delivery Plan](../planning/recommendation-system-delivery-plan.md).
