# Local Integration Workspace

**Status:** Proposed
**Owner:** Core integrator
**Last updated:** 28 July 2026

## Purpose

Define a safe local arrangement for running authorised FoodMind repositories together without turning them into a monorepo.

## Workspace Layout

```text
FoodMind/
├── foodmind-backend/
├── foodmind-web/
├── foodmind-android/
├── foodmind-intelligence/
├── foodmind-ml/
└── foodmind-docs/
```

Each child directory remains an independent Git repository with its own:

- Branches
- Pull Requests
- CI
- Secrets
- Releases
- Access rules

The parent directory is not a Git repository.

## Runtime Components

For normal end-to-end development:

```text
PostgreSQL
Spring Boot Backend
Intelligence inference service
Intelligence Agent service
Web client and/or Android client
```

`foodmind-ml` is not a normal runtime dependency. It produces an immutable model package before runtime integration.

## Startup Order

1. Configure approved local secrets outside Git.
2. Start PostgreSQL.
3. Apply Backend migrations and start Backend.
4. Validate/load a local test model package in inference service.
5. Start Agent service.
6. Start Web or Android.
7. Execute the selected UAT scenario.

Backend CRUD should remain usable if Agent/inference services are unavailable.

## Environment Ownership

| Value | Owner | Consumers |
| --- | --- | --- |
| Public Backend URL | Backend/integration | Web, Android |
| Database credentials | Backend | Backend only |
| Agent service URL/token | Backend | Backend only |
| Inference service URL/token | Backend/Intelligence | Backend or Agent as defined by private contract |
| Model artifact URI/checksum | ML release/Intelligence deployment | Inference service only |
| LLM credential | Intelligence | Agent service only |

No shared plaintext environment file should be distributed to the entire team.

## Contract-First Integration

When another service is unavailable:

- Use versioned fixtures.
- Record the owning contract commit.
- Cover success and failure responses.
- Do not create a second unofficial schema.
- Replace the mock with a real contract test before declaring integration complete.

## UAT Record

Every cross-system test record should include:

- Use-case ID
- Date/time
- Tester
- Environment
- Repository commits
- API/contract versions
- Model version, when applicable
- Steps
- Expected result
- Actual result
- Evidence link
- Defect/Issue link

## Prohibited Practices

- Copying implementation code between repositories
- Committing a parent-level orchestration file containing secrets
- Giving client developers database or private-service credentials
- Pointing Android/Web directly to Agent or inference
- Using a mutable unversioned model artifact
- Testing group visibility with real personal accounts or unrestricted data

## Troubleshooting Sequence

Trace one request at a time:

1. Client correlation ID
2. Backend authentication/validation
3. Backend permission scope
4. Backend database operation
5. Agent route/tool call, when applicable
6. Inference request/model version, when applicable
7. Backend response/fallback
8. Client rendering

Do not bypass the failing layer to make the demonstration appear successful.
