# Documentation Governance

**Status:** Accepted
**Owner:** Project lead / core documentation team
**Last updated:** 28 July 2026

## Objective

Keep product, architecture, contracts, implementation guidance, and presentation material consistent across six independently developed repositories.

## Artifact Owners

| Artifact | Canonical owner |
| --- | --- |
| Product scope and terminology | `foodmind-docs` |
| Public OpenAPI | `foodmind-backend` |
| Backend database migrations | `foodmind-backend` |
| Cross-system ERD/data dictionary | `foodmind-docs`, reconciled with Backend |
| Agent/inference runtime schemas | `foodmind-intelligence` |
| Model-package producer schema | `foodmind-ml` |
| Model-package consumer fixtures | `foodmind-intelligence` |
| Web implementation notes | `foodmind-web` |
| Android implementation notes | `foodmind-android` |
| UAT and security evidence index | `foodmind-docs` |

Coordination copies must link to or record the canonical version.

## Decision Types

Use an ADR for a decision that:

- Changes a service or repository boundary
- Changes public/private contract ownership
- Changes persistence authority
- Changes security or visibility rules
- Adds infrastructure
- Changes model-package compatibility
- Moves an item into or out of the frozen MVP

Small editorial corrections do not require an ADR.

## ADR Fields

Every ADR should include:

- ID and title
- Status
- Date
- Decision owner
- Context
- Decision
- Alternatives considered
- Consequences
- Affected repositories
- Migration or follow-up actions
- Superseded ADR, if any

## Change Propagation Matrix

### Public API change

Update:

- Backend OpenAPI and tests
- Web client issue/fixtures
- Android client issue/fixtures
- Docs coordination examples
- UAT traceability

### Database/domain change

Update:

- Backend migration and model
- ERD/data dictionary
- API contract if exposed
- Analytics definitions if affected
- ML feature contract if affected

### Agent/inference contract change

Update:

- Intelligence schemas/tests
- Backend client DTO/contract tests
- Docs private-contract reference
- Timeout/fallback test cases

### Model feature/package change

Update:

- ML feature schema, evaluation, model card, and package
- Intelligence consumer schema/fixtures
- Compatibility matrix
- Runtime deployment record
- Backend only if the private inference contract changes

### Scope change

Update:

- Canonical guide
- Backlog and acceptance criteria
- Proposal
- Presentation
- Architecture/use-case diagrams
- Demo plan

## Review Checklist

- Is the artifact status explicit?
- Is the owner clear?
- Are confirmed decisions separated from recommendations?
- Does it match the six-repository topology?
- Does it preserve Spring Boot as the only public boundary?
- Does it separate offline ML training from runtime inference?
- Are Recommendation, Cooking, and Chatbot separate entry points?
- Are privacy and group visibility rules preserved?
- Are unsupported food-safety or model-accuracy claims absent?
- Are affected repositories listed?
- Are dates, versions, and links current?

## Superseding Material

Do not delete useful historical rationale. Mark the old artifact `Superseded`, point to the replacement, and ensure final submission material uses only the accepted version.

Binary Proposal and PowerPoint files cannot be safely reconciled through line diffs alone. Their Pull Requests should include:

- Change summary
- Sections/slides affected
- Exported visual review evidence
- Confirmation that canonical terminology was checked
