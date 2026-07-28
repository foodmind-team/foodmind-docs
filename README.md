# FoodMind Documentation

FoodMind Documentation is the restricted system-level source of truth for the FoodMind AD Project. It coordinates product scope, architecture, contracts, data design, delivery evidence, and cross-repository integration without exposing unrelated implementation code to every contributor.

> **Current status:** the project proposal, presentation, and canonical AI context guide exist. The directory framework and repository-specific documentation are established, but many planned ERD, OpenAPI, ADR, UAT, security, and operations artifacts are not yet complete.

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

## Current Top-Level Documents

- `FoodMind_AI_Project_Context_and_Tutoring_Guide.md`: canonical project context, confirmed decisions, scope, architecture, and implementation guidance.

- `Team5_AD_Project_Proposal.docx`: formal project proposal. It may lag behind later canonical decisions and must be synchronised before final submission.

- `FoodMind_Presentation_Proposal.pptx`: presentation deck. Slide content and diagrams must be checked against the canonical guide before final use.

- `planning/team-work-allocation.md`: proposed seven-person workload and repository ownership plan for the four-week MVP.

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

1. Explicit decision made by the project owner after the latest document date
2. Accepted ADR
3. Current canonical AI context guide
4. Versioned public/private contracts
5. ERD and data dictionary
6. Proposal and presentation
7. Historical planning notes

The conflict must still be fixed; precedence is not permission to leave final artifacts inconsistent.

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
