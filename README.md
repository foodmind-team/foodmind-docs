# FoodMind Documentation

FoodMind Documentation is the restricted system-level source of truth for the FoodMind AD Project. It coordinates product scope, architecture, contracts, data design, delivery evidence, and cross-repository integration without exposing unrelated implementation code to every contributor.

> **Current status:** the formal Proposal and presentation are frozen reference
> baselines. The canonical guide and repository documentation are being aligned
> to the latest recommendation-first UX: a two-mode home, Groups as a core
> shared workspace, and a permission-safe Explore destination. Many planned
> ERD, OpenAPI, ADR, UAT, security, and operations artifacts remain incomplete.

## Repository Role

This repository owns:

- Canonical product scope and terminology
- Cross-system architecture
- Architecture Decision Records
- ERD and data dictionary
- Public and private contract copies/examples used for coordination
- Model-package contract coordination
- Product backlog, Sprint status, and traceability
- UAT and security evidence
- Integration and deployment runbooks
- Presentation, script, and demonstration material

It does not own implementation details that belong inside Backend, Web, Android, Intelligence, or ML.

## Confirmed Repository Topology

FoodMind uses six separate private repositories:

| Repository | Responsibility |
| --- | --- |
| `foodmind-backend` | Public Spring Boot API, security boundary, persistence, business rules, orchestration, and analytics |
| `foodmind-web` | React browser client |
| `foodmind-android` | Native Kotlin/Compose client |
| `foodmind-intelligence` | Private Agent service and runtime inference service |
| `foodmind-ml` | Offline data, training, evaluation, and immutable model release |
| `foodmind-docs` | Restricted cross-system documentation and evidence |

`foodmind-ml` produces a versioned model package. `foodmind-intelligence` validates and consumes that package; it does not own offline training.

## Current ML Data Sources

The current offline ML dataset plan uses:

- **Food.com Recipes and Interactions (Kaggle)** for recipe metadata and
  historical user-recipe ratings.
- **NEA Licensed Eating Establishments (data.gov.sg)** for Singapore licensed
  eating-establishment reference data.
- **Self-collected menu data** for selected restaurant menu items, prices,
  categories, source URLs, and collection dates.

Food.com recipes, FoodMind interactions, and Singapore menu items are connected
through the normalised `dish_id`. NEA data supports establishment context, but
menu prices and dish availability must come from the self-collected menu data.

## Current Top-Level Documents

- `FoodMind_AI_Project_Context_and_Tutoring_Guide.md`: canonical implementation
  and tutoring guide derived from the formal Proposal and presentation, plus
  approved implementation-level clarifications that do not expand their MVP.

- `Team5_AD_Project_Proposal.docx`: formal project Proposal and primary scope
  baseline. Do not edit it during routine documentation alignment.

- `FoodMind_Presentation_Proposal.pptx`: formal presentation and primary
  narrative/architecture baseline. Do not edit it during routine documentation
  alignment.

- `planning/team-work-allocation.md`: seven-person workload and repository
  ownership plan aligned to the recommendation-first UX.

- `planning/cooking-plan-agent-fullstack-plan/README.md`: proposed phased
  delivery plan for the Cooking Plan v2 path across Web, Backend, and the
  Intelligence Agent, including contract freeze, async orchestration,
  production hardening, rollout, and v1 retirement.

- `architecture/recommendation-document-inventory.md`: audited inventory of
  the formal, canonical, Backend, Intelligence, ML, and client documentation
  related to recommendation algorithms and Agents, including discrepancies
  against the current repository implementations.

- `architecture/recommendation-system-implementation-design.md`: proposed
  end-to-end design for the Backend recommendation function, UserCF, ItemCF,
  logistic-regression ranking, model package, private inference service,
  dedicated Recommendation Agent, feedback loop, security, and rollout.

- `planning/recommendation-system-delivery-plan.md`: phased cross-repository
  implementation plan, acceptance gates, responsibility matrix, test strategy,
  and Git/PR sequence for delivering the recommendation system.

- `planning/status/FoodMind_Prioritisation_Strategy_and_Project_Status_Report.xlsx`:
  formula-driven feature prioritisation, business-process, technology and
  evidence-based delivery status report derived from the formal baselines and
  current repository state.

- `operations/production-demo/aws-media-deployment-checklist.md`: AWS-ready
  private S3, ECS Task Role, CORS, environment, smoke-test, and rollback
  checklist for enabling Food/Drink Record image delivery.


## Latest Product-Experience Clarification

The formal sources remain authoritative. The current implementation expresses
their scope through these UX decisions:

- The home header switches between **Eat out & delivery** and **Cooking**.
- **Eat out & delivery** is the default and presents the most prominent
  Generate Recommendation action.
- Recommendation uses the user's authorised history, trusted-group evidence,
  current context, and the existing hybrid ranking design.
- The backend may return three intentionally different candidates; clients show
  one lead result at a time and expose the remaining candidates through “try
  another”.
- Groups is a core shared decision workspace.
- Explore uses an image-led post layout for authorised group-visible and curated
  content. It is not the public/follower feed excluded by the Proposal.
- Cooking uses manually entered or already authorised pantry context. Automatic
  inventory capture remains outside the MVP.

## Repository Structure

```text
foodmind-docs/
├── architecture/
│   ├── adrs/
│   ├── diagrams/
│   └── decisions/
├── contracts/
│   ├── public/
│   │   ├── openapi/
│   │   └── examples/
│   └── internal/
│       ├── agent/
│       ├── inference/
│       └── model-package/
├── database/
│   ├── erd/
│   └── data-dictionary/
├── evidence/
│   ├── reports/
│   └── screenshots/
├── operations/
│   ├── local/
│   ├── staging/
│   └── production-demo/
├── planning/
│   ├── backlog/
│   ├── sprints/
│   └── status/
├── presentation/
│   ├── slides/
│   ├── scripts/
│   └── demo/
└── testing/
    ├── uat/
    ├── security/
    └── traceability/
```

## Source-of-Truth Order

When artifacts conflict, apply this order:

1. Formal Proposal for product scope and requirements
2. Formal presentation for the approved narrative and architecture summary
3. Explicit project-owner clarification that does not contradict or expand the formal MVP
4. Accepted ADR
5. Current canonical AI context guide
6. Versioned public/private contracts
7. ERD and data dictionary
8. Historical planning notes

The conflict must still be fixed. If a proposed change would contradict or
expand the formal sources, stop and obtain explicit approval before changing
implementation documentation.

## Documentation Status Labels

Every significant design document should identify one status:

- `Draft`
- `Proposed`
- `Accepted`
- `Superseded`
- `Archived`

Also include:

- Owner
- Last updated date
- Related repositories
- Related contract/ADR
- Open questions

Do not describe a proposal as implemented without repository evidence.

## Contract Ownership

### Public API

- Canonical owner: `foodmind-backend`
- Coordination copy/examples: `contracts/public/`
- Consumers: Web and Android

The backend's committed OpenAPI file remains authoritative. This repository should record the version/commit used for cross-system UAT.

### Runtime internal contracts

- Canonical owner: `foodmind-intelligence`
- Matching client DTO/tests: `foodmind-backend`
- Coordination examples: `contracts/internal/agent/` and `contracts/internal/inference/`

### Model-package contract

- Producer: `foodmind-ml`
- Consumer: `foodmind-intelligence`
- Coordination material: `contracts/internal/model-package/`

A contract copy here must identify its owning repository and version to prevent drift.

## Required Architecture Artifacts

- System context diagram
- Container/runtime diagram
- Recommendation sequence
- Cooking-plan sequence
- Chatbot search/summary sequence
- Trust and permission boundaries
- DevSecOps deployment diagram
- ERD
- Model training-to-runtime release flow
- Major ADRs

Diagrams must show direction and trust boundaries, not only disconnected boxes.

## Required Delivery Evidence

- UC-01 through UC-09 UAT results
- Android and Web parity matrix
- Permission and visibility tests
- Recommendation fallback evidence
- Chatbot grounding/source evidence
- ML evaluation and model card
- CI checks
- Dependency/secret/container scans
- OWASP ZAP report
- Cloud HTTPS demonstration
- Working-feature screenshots
- Final demo recording and script

Evidence must identify the commit, environment, date, and tester.

## Sensitive Information

This repository may contain restricted academic and project material. Therefore:

- Keep the repository private.
- Grant least-privilege access.
- Do not add production secrets or real passwords.
- Minimise personal identifiers in new documents.
- Redact test-user credentials and tokens.
- Confirm permission to use screenshots, datasets, and images.
- Do not move restricted proposal/member information into public code repositories.

## Change Workflow

1. Identify the owning artifact.
2. Check whether the change requires an ADR.
3. Update the canonical source first.
4. Update affected diagrams/contracts/tables.
5. List cross-repository actions.
6. Review terminology and scope.
7. Open a documentation Pull Request.
8. Record superseded material instead of silently preserving contradictions.

See [document governance](architecture/decisions/document-governance.md).

## Integration Workflow

For local end-to-end work, authorised repositories may be cloned as sibling directories. Do not create a monorepo or copy source between repositories.

See [integration workspace](operations/local/integration-workspace.md).
