# FoodMind full end-to-end integration test report

**Initial audit date:** 2026-08-11 (Asia/Singapore)<br>
**Repair acceptance date:** 2026-08-12 (Asia/Singapore)<br>
**Overall verdict:** **PASS — repair acceptance complete**<br>
**Mandatory Web/Android parity verdict:** **PASS — 83/83 operations on both clients**<br>
**Live communication verdict:** **PASS — real stack and real clients verified**

The release blockers recorded by the initial audit have been repaired and verified. The historical defect evidence in Sections 3–9 is intentionally preserved; Section 10 is the authoritative post-repair acceptance record. DeepSeek credential rotation is explicitly excluded at the request of the task owner. No credential value was modified, printed, or committed.

## 1. Acceptance verdict

| Requirement | Result | Evidence summary |
|---|---:|---|
| Every interface matches and is connected exactly | **PASS** | Web and Android API gates both resolve all 83 canonical Backend OpenAPI operations with no exemptions or duplicate Retrofit declarations. Generated DTO checks match the corrected recommendation contract. |
| Web and Android expose exactly the same full functions and all pages work | **PASS** | Both clients expose inventory, shopping lists, recipe import, server recipe CRUD, cooking, recommendation, chat, navigation, filters, and empty/error states against the same server-owned data. |
| Stable client → backend → intelligence communication | **PASS** | The rebuilt no-mock Compose stack remained healthy while authenticated Web Playwright and Android emulator clients exercised Backend, Cooking, Recommendation, Chat, and Inference links. |
| Severity-sorted report with targeted Codex solutions | **PASS** | Sections 5–8 preserve the initial defects and solutions; Section 10 records the implemented resolution and verification for every in-scope P0–P3 item. |

**Release decision:** all in-scope repair gates pass. Keep the submitted PRs pending for independent manual review; do not self-merge.

## 2. Tested revisions and workspace state

| Repository | Branch | Tested commit | Initial state |
|---|---|---|---|
| `foodmind-backend` | `master` | `0ed7ca5383180ec2d3972cb368e6f815ac060162` | clean |
| `foodmind-web` | `master` | `2f998da18f251ca39b1ac0fc6e8a8f1be1bce253` | clean |
| `foodmind-android` | `master` | `4c2d6e58ac3f2af60396f058c3142996d93010da` | clean |
| `foodmind-intelligence` | `main` | `f21abc536ad2d23a2f7a51fee76c828bb0678a7e` | clean |
| `foodmind-ml` | `fix/recommendation-runtime-package` | `9c5fbfb4d9b5d2f750699dc2a308d38990e26026` | pre-existing untracked `.tmp/` preserved |
| `foodmind-docs` | `main` | `98f0db4eb024e01868e8053e8d036c8b5edfb857` | clean before this report |

The workspace root is not a Git repository; each child repository was inspected independently.

## 3. Interface and functional-parity census

### 3.1 Operation coverage

| Contract/client | Unique operations | Relationship to backend |
|---|---:|---|
| Backend canonical OpenAPI | 83 | source of truth |
| Web production call sites | 80 | 3 explicit exceptions |
| Android Retrofit declarations | 63 | 20 missing; 64 declarations because one route is duplicated |
| Common to Web and Android | 61 | 73.5% of backend operations |
| Web-only | 19 | mostly server recipes, imports, inventory, and shopping |
| Android-only | 2 | synchronous cooking generation and synchronous decision submission |

The Android endpoint comparison normalised Retrofit paths by adding the OpenAPI leading slash. Correlation ID is not counted as missing because Android adds it globally in the OkHttp interceptor.

### 3.2 Web exceptions

Web's `npm run api:coverage` reports 80 used operations and these 3 explicit exceptions from `contracts/backend-api-coverage.json`:

- `POST /cooking-plans/{planId}/decisions`
- `POST /cooking-plans/generate`
- `GET /inventory/lots/{lotId}`

Under the requested “exactly all interfaces” rule, documented exceptions are still parity failures. Android implements the first two synchronous operations, while neither client implements the single-lot read.

### 3.3 Backend operations absent from Android

Android is missing these exact 20 operations:

1. `POST /cooking-plans/{planId}/decisions-async`
2. `POST /cooking-plans/{planId}/shopping-list`
3. `GET /inventory/lots`
4. `POST /inventory/lots`
5. `GET /inventory/lots/{lotId}`
6. `PUT /inventory/lots/{lotId}`
7. `DELETE /inventory/lots/{lotId}`
8. `GET /shopping-lists`
9. `GET /shopping-lists/{shoppingListId}`
10. `PATCH /shopping-lists/{shoppingListId}/items/{itemId}`
11. `POST /shopping-lists/{shoppingListId}/complete`
12. `POST /recipe-imports`
13. `GET /recipe-imports/{importId}`
14. `POST /recipe-imports/{importId}/answers`
15. `POST /recipe-imports/{importId}/confirm`
16. `GET /recipes`
17. `POST /recipes`
18. `GET /recipes/{id}`
19. `PUT /recipes/{id}`
20. `DELETE /recipes/{id}`

Android's manifest has recipe editor/library and cooking activities, but no inventory, shopping-list, or recipe-import activity. `RecipeDraftStore` explicitly uses account-scoped `SharedPreferences`, seeds three demonstration recipes, and incorrectly states that the backend has no recipe CRUD endpoints. Web routes use the backend recipe, recipe-import, inventory, and shopping APIs.

### 3.4 Shared-operation shape differences

Android omits 8 optional OpenAPI filters:

- Food record list: `cuisineId`, `mealId`, `placeId`, `minRating`, `maxRating`
- Drink record list: `placeId`, `minRating`, `maxRating`

Android also sends an undocumented `{}` request body to `POST /cooking-plans/{planId}/cancel`, whose public OpenAPI operation has no request body.

Four same-named Android DTOs omit 12 OpenAPI fields:

| Android DTO | Missing fields |
|---|---|
| `ApiFieldError` | `code` |
| `GenerateCookingPlanRequest` | `recipeIds`, `region`, `servingAt` |
| `RecommendationResponse` | `modelVersion`, `fallbackVersion`, `createdAt`, `completedAt` |
| `UserPreferencesResponse` | `hardConstraints`, `version`, `createdAt`, `updatedAt` |

The OpenAPI schema `CookingQuestionAnswer` is absent. Android instead has a wire-equivalent `QuestionAnswerRequest(questionId, value)`, while another Retrofit declaration references the nonexistent type and breaks compilation.

Name-based schema coverage found 81 of 122 backend schema names represented in Android. The 41 absent names are listed in Appendix B. Name absence alone is not proof of a defect where a deliberately differently named wire-equivalent model exists, but it identifies the ungenerated/manual-client surface that the parity gate must cover.

### 3.5 Recommendation response contract contradiction

The backend OpenAPI `RecommendationResponse` permits only `FALLBACK_SUCCEEDED` and `NO_VALID_CANDIDATE` for `status`; permits only `SUCCEEDED` and `NO_VALID_CANDIDATE` for `fallbackStatus`; and requires `fallbackVersion`.

The backend's successful agent test asserts the actual response is:

- `status = SUCCEEDED`
- `modelStatus = SUCCEEDED`
- `fallbackStatus = NOT_REQUIRED`
- `modelVersion` present
- `fallbackVersion` absent

Web compensates with a handwritten `RuntimeRecommendation` type and unsafe casts. Therefore, the generated type check is green while the public contract remains false.

## 4. Executed validation and communication results

### 4.1 Build and test results

| Component | Command/test | Result |
|---|---|---:|
| Web API generation | `npm run api:check` | PASS against the Web snapshot |
| Web operation coverage | `npm run api:coverage` | PASS: 80 used, 3 exceptions |
| Web unit/coverage | `npm run test:coverage -- --maxWorkers=1` | PASS: 78/78 tests; 93.21% statements, 81.96% branches, 96.12% functions, 96.78% lines |
| Web production build | `npm run build` | PASS |
| Web Playwright | `npm run test:e2e -- --workers=1` | PASS: 12/12, including primary destinations, core flows, accessibility, and visual checks |
| Backend OpenAPI syntax | `python scripts/validate-openapi.py` | PASS |
| Backend clean test | `mvnw clean test` | FAIL: 193/195 pass; 2 Chat flow failures |
| Backend package | `mvnw -DskipTests package` | PASS |
| Android unit/build/lint | `gradlew testDebugUnitTest assembleDebug lintDebug` | FAIL at Kotlin compilation; no APK, unit result, lint result, or page run |
| Inference service | `uv run pytest -q` | PASS: 3/3 |
| Recommendation agent | `uv run pytest -q` | PASS: 171 passed, 1 skipped |
| Chat agent | `uv run pytest -q` | PASS: 4/4 |
| Cooking agent, working tree | `uv run pytest -q` | FAIL during collection: 13 settings errors |
| Cooking agent, clean Git archive without shared `.env` | current venv with archive on `PYTHONPATH` | PASS: 1,216/1,216; 22 deprecation warnings |

The first heavily parallel Web run had Vitest worker-start failures and two Playwright timeouts. Isolated single-worker reruns passed completely, so those initial failures are classified as resource contention rather than product failures. The first non-clean backend test run also saw a stale compiled Flyway migration in `target/`; `mvnw clean test` removed that noise and exposed the two real Chat failures above.

Web Playwright tests intercept `**/api/v1/**` through `e2e/fixtures/api.ts`; they validate pages and client behavior but are not a live Web → Backend test.

### 4.2 Live communication probes

| Link | Probe | Result |
|---|---|---:|
| Recommendation Agent → Inference | 20 authenticated recommendation fixture calls | PASS 20/20; 20–85 ms, 28 ms average; expected contract/model/feature versions and at least one result |
| Backend-shaped client → Cooking | Compared all 16 `AgentGeneratePlanRequest` snake-case properties with live `GeneratePlanRequest` schema | PASS 16/16 |
| Backend-shaped client → Cooking preprocess | 20 authenticated `POST /internal/v1/agents/cooking-plan/preprocess` calls | PASS 20/20 HTTP/parsed responses; 6–33 ms, 8.5 ms average |
| Cooking health | `/health/live`, `/health/ready`, `/health/load` | PASS; ready checks reported settings validated, graph compiled, and not shutting down |
| Backend → Chat Agent | Backend `ChatFlowTest` reached the already-running live agent | CONNECTED, but caused nondeterministic test semantics (`SUCCEEDED` instead of expected `FALLBACK_SUCCEEDED`) |
| Web → Backend → agents | Authenticated real-stack browser flow | NOT VERIFIED; browser suite uses API interception |
| Android → Backend → agents | Build/emulator flow | BLOCKED by Android compilation |

Recommendation, Inference, and Chat containers were already running and were left untouched. Cooking was started solely for this test, verified healthy, probed, and stopped afterward. A paid external Cooking LLM generation was not invoked; the live probe stopped at the authenticated parsing boundary.

## 5. P0 — release-blocking findings

### P0-01 — Android does not compile, so no Android page is runnable

**Evidence**

- `FoodMindApi.kt:249` references unresolved `CookingQuestionAnswer`.
- `FoodMindApi.kt:245-250` and `:270-275` declare the same `POST /cooking-plans/{planId}/decisions` twice.
- `FoodMindNetwork.kt:269-274` exposes two overloads for those declarations.
- `CookingActivities.kt:280` becomes overload-ambiguous; further inference errors cascade from it.
- `assembleDebug`, unit tests, lint, and instrumentation cannot pass the compile phase.

**Codex-executable targeted solution**

Scope: `foodmind-android` only.

1. Make the OpenAPI `CookingQuestionAnswer` model canonical by renaming or replacing `QuestionAnswerRequest`; keep its exact `questionId` and `value` wire fields.
2. Keep exactly one Retrofit declaration for synchronous decision submission and exactly one `FoodMindNetwork` wrapper. Update all callers to that single type and method.
3. Remove the cascading ambiguous call and add a MockWebServer assertion for the exact JSON list body and `Idempotency-Key`.
4. Run:

   ```powershell
   .\gradlew.bat clean testDebugUnitTest assembleDebug lintDebug
   ```

5. With an emulator available, run:

   ```powershell
   .\gradlew.bat connectedDebugAndroidTest
   ```

Acceptance: zero duplicate Retrofit operations, compilation succeeds, APK exists, unit/lint pass, and the decisions request contract test passes.

### P0-02 — Mandatory Web/Android functional parity is absent

**Evidence**

- Only 61/83 backend operations are common to both clients.
- Android is missing the 20 operations in section 3.3 and has no corresponding inventory, shopping-list, or recipe-import pages.
- Android recipes are seeded device-local drafts; Web recipes are persisted by `/recipes` and used by async Cooking generation.
- Web still excludes 3 backend operations.

**Codex-executable targeted solution**

Scope: `foodmind-android`, `foodmind-web`, and the canonical backend OpenAPI.

1. Add Android server-backed recipe CRUD, recipe-import question/answer/confirm, inventory CRUD, shopping-list list/detail/update/complete, Cooking → shopping-list, and async decision submission.
2. Replace `RecipeDraftStore` as the production source of truth with an authenticated repository backed by `/recipes`. If offline drafts remain, mark them explicitly as unsynced and reconcile them; do not seed demo records into a user's production library.
3. Add Android activities/navigation and usable loading, empty, error, optimistic-lock, and success states for every added capability.
4. Add Web production call sites for sync generate, sync decisions, and single-lot read, or remove those public operations from the canonical API only after both clients migrate. The requested gate does not allow exceptions.
5. Add one checked-in capability manifest generated from OpenAPI and a CI check that fails unless both clients cover the same 83 operations and user-visible capabilities.
6. Add parity tests that create/update/read the same recipe, inventory lot, shopping list, recipe import, and Cooking plan from both clients against one test account.

Acceptance: Web and Android each cover 83/83 operations with no exception, have equivalent user flows, and cross-device reads observe the same server state.

### P0-03 — Public recommendation schema rejects the backend's successful response

**Evidence**

- `foodmind-backend/src/main/resources/openapi/openapi.yaml:1788-1828` excludes runtime `status=SUCCEEDED`, excludes `fallbackStatus=NOT_REQUIRED`, and requires `fallbackVersion`.
- `RecommendationAgentFlowTest.java:75-85` asserts those exact successful runtime values and an absent `fallbackVersion`.
- `foodmind-web/src/routes/HomeRoutes.tsx:15-19,115,244` widens the generated type manually and casts both generate and read responses.

**Codex-executable targeted solution**

Scope: `foodmind-backend`, then regenerate `foodmind-web` and `foodmind-android` models.

1. Derive response enums and conditional nullability from backend persistence constraints and response mappers, including successful, fallback, no-candidate, processing, and failed states that can actually cross the public boundary.
2. Correct `RecommendationResponse.status`, `modelStatus`, and `fallbackStatus`; make `modelVersion`/`fallbackVersion` required or nullable according to the corresponding status rather than requiring absent metadata.
3. Add backend response validation tests that serialise every reachable state and validate it against the committed OpenAPI schema.
4. Refresh both clients from the corrected contract and delete `RuntimeRecommendation` plus its casts.
5. Run backend tests, `npm run api:check`, Web tests/build, and Android tests/build.

Acceptance: successful and fallback backend fixtures validate against OpenAPI, generated clients compile without widening/casts, and both clients render all reachable statuses.

### P0-04 — Cooking's documented direct-run configuration fails and exposed a credential value

**Evidence**

- The shared agent README instructs developers to place `DEEPSEEK_API_KEY` in `agent-service/app/agents/.env`.
- Cooking reads that same file with `env_prefix="COOKING_PLAN_"` and `extra="forbid"` at `settings.py:220-224`.
- Direct `uv run pytest -q` failed during collection with 13 Pydantic settings errors because the shared unprefixed key was considered extra.
- The validation error rendered the credential's input value in terminal output. The value is intentionally not reproduced here. The `.env` file is ignored by Git, but exposure in logs/terminal history still requires rotation.

**Immediate operator action**

Revoke/rotate the exposed DeepSeek credential in the provider console, then update the ignored local `.env`. Do not commit either value.

**Codex-executable targeted solution**

Scope: `foodmind-intelligence/agent-service/app/agents/cooking`.

1. Preserve the documented shared `.env` design and change Cooking settings so unrelated shared-agent keys are ignored, while `COOKING_PLAN_*` remains the only bound prefix. Alternatively, use an explicit settings source that maps only approved keys.
2. Store API keys as secret types and ensure validation/log formatting never includes raw input values.
3. Add a regression test using a temporary shared `.env` containing a sentinel `DEEPSEEK_API_KEY` and unrelated agent variables; assert settings load and captured output never contains the sentinel.
4. Run `uv run pytest -q` from the real working tree, not only a clean archive.

Acceptance: all 1,216 Cooking tests pass with the documented shared `.env`, and a repository-wide search of captured test output finds no sentinel secret.

## 6. P1 — high-priority integration findings

### P1-05 — Android's manual API models and shared-operation shapes have drifted

**Evidence**

- 8 optional filters are unavailable to Android callers.
- 12 fields are absent across four same-named DTOs.
- Cancel sends an undocumented body.
- 41/122 OpenAPI schema names have no same-named Kotlin representation.

**Codex-executable targeted solution**

Scope: `foodmind-android`.

1. Generate Retrofit interfaces/models from the accepted backend OpenAPI, or add an equivalent deterministic generator/check if keeping custom wrappers.
2. Correct the 8 filters, 12 fields, and no-body cancel operation.
3. Keep domain/UI models separate from generated wire DTOs and add explicit mappers; do not weaken required OpenAPI fields into nullable defaults merely to hide drift.
4. Add `apiGenerate`, `apiCheck`, and `apiCoverage` Gradle tasks. `apiCheck` must regenerate to a temporary directory and diff; `apiCoverage` must compare normalised method/path pairs and parameters.

Acceptance: a machine comparison reports 83/83 methods, exact parameters/bodies/headers, zero stale generated files, and no duplicate operation declarations.

### P1-06 — Web's contract provenance gate can report green with a stale lock

**Evidence**

- Backend OpenAPI and Web snapshot are currently byte-identical with SHA-256 `d1bf2c44acee4918a2a0baa12a152890eba2170ca0236882a40b53745778252e`.
- `backend-openapi-v1.lock.json` instead records `backendCommit=WORKTREE-uncommitted` and SHA-256 `70a83c8cbd3c8e4d3d7414844b3f11672747e0c9b17b04937617fe3986def6eb`.
- `scripts/check-api.mjs` checks only generated TypeScript against the local Web snapshot; it never validates the lock or source repository.

**Codex-executable targeted solution**

Scope: `foodmind-web`.

1. Update the lock to the exact committed backend revision and snapshot hash.
2. Extend `api:check` to hash the snapshot, compare it with the lock, reject `WORKTREE-*`, and, when the sibling backend is present, verify its committed OpenAPI blob and commit.
3. Add a CI input/artifact path so the same check works without a sibling checkout.
4. Correct `docs/operations/local-development.md`, which currently says there are no coverage exceptions despite the three checked-in exceptions.

Acceptance: changing the snapshot, lock hash, backend commit, or generated file independently makes `npm run api:check` fail with a specific message.

### P1-07 — Backend Chat flow tests depend on whichever service occupies port 8004

**Evidence**

- `ChatFlowTest` overrides only the internal service token.
- Default application configuration enables Chat and targets `http://127.0.0.1:8004`.
- With a live Chat Agent present, two tests expected `FALLBACK_SUCCEEDED` but received `SUCCEEDED`, leaving `mvnw clean test` at 193/195.

**Codex-executable targeted solution**

Scope: `foodmind-backend`.

1. Make `ChatFlowTest` deterministic by disabling the external Chat Agent for fallback scenarios or injecting a controlled `ChatAgentPort` stub.
2. Keep adapter contract tests on a private ephemeral mock server.
3. Move real Chat integration into an explicit profile/tag such as `live-agent-integration`; require a provided base URL/token and skip clearly when absent.
4. Run the ordinary suite once with port 8004 closed and once with a real agent on that port; results must be identical.

Acceptance: `mvnw clean test` passes 195/195 regardless of local agent processes, while the opt-in live test independently verifies `SUCCEEDED`.

### P1-08 — There is no real-stack cross-repository E2E release gate

**Evidence**

- Web's 12 Playwright tests mock every `/api/v1` request.
- Android has only `MainActivitySmokeTest.kt` with two instrumentation tests; the `e2e` and `fixtures` directories contain only `.gitkeep`.
- No executed test covered authenticated Web → Backend → Intelligence → Inference with a real database.
- Android → Backend could not start because Android does not compile.

**Codex-executable targeted solution**

Scope: all runtime repositories; place orchestration in a clearly owned integration-test directory and CI workflow.

1. Provide an isolated Compose stack for Postgres, Backend, Recommendation, Inference, Cooking, Chat, and the built Web application, with health-based dependencies and test-only credentials.
2. Add deterministic seed/setup through public APIs, not direct production-table mutation.
3. Add a no-route-interception Playwright project that covers registration/login/refresh, records, groups/privacy, recommendation and fallback, recipes/import, Cooking async/decision/cancel, inventory/shopping, Chat, dashboard/recap, and logout.
4. Add Android emulator tests for the same capability manifest and account, including cross-client state visibility.
5. Propagate and assert one correlation ID across client request, Backend log, and each called intelligence service. Include retry/timeout/unavailable tests.
6. Tear down only test-owned resources and publish logs/results as CI artifacts.

Acceptance: one CI command brings up the clean stack, passes both client suites with zero mocked public API routes, verifies cross-device state, and tears down successfully.

## 7. P2 — medium-priority inconsistencies

### P2-09 — Android release builds silently default to a placeholder API host

**Evidence**

`foodmind-android/app/build.gradle.kts:11-13` falls back to `https://api.foodmind.example/api/v1/`. A release APK can therefore compile while being unable to reach a real Backend.

**Codex-executable targeted solution**

Scope: `foodmind-android`.

1. Require `FOODMIND_API_BASE_URL` or an approved release property for release variants.
2. Fail Gradle configuration for `.example`, loopback, missing `/api/v1/`, non-HTTPS, or malformed release URLs.
3. Keep the emulator default only for debug builds and add Gradle tests for accepted/rejected URLs.

Acceptance: `assembleRelease` fails without a real approved URL and succeeds only with a validated HTTPS API base.

### P2-10 — Documentation describes obsolete contracts and parity

**Evidence**

- Android `RecipeDraftRepository.kt:21-25` says backend recipe CRUD does not exist.
- Web `docs/android-native-flow-parity.md` repeats the device-local recipe assumption.
- Web `docs/operations/local-development.md` says API coverage has no exceptions, while `backend-api-coverage.json` has three.

**Codex-executable targeted solution**

Scope: `foodmind-android`, `foodmind-web`, and `foodmind-docs`.

1. After implementing P0-02, update all parity and local-development documents from the generated capability manifest.
2. Link every claimed client capability to its OpenAPI operation and automated test.
3. Add a docs check that fails on stale operation counts and forbidden statements such as “backend has no recipe CRUD endpoints.”

Acceptance: documentation reports the same operation totals and parity status as the machine-generated checks.

## 8. P3 — low-priority maintenance finding

### P3-11 — Cooking's clean suite emits 22 dependency deprecation warnings

The passing clean-archive run emitted warnings around Starlette/httpx test client behavior and deprecated HTTP 422 constants. These are not current functional failures but can become upgrade blockers.

**Codex-executable targeted solution**

Scope: `foodmind-intelligence/agent-service/app/agents/cooking`.

1. Capture the full warning list with `uv run pytest -q -W default`.
2. Replace deprecated application constants/usages and upgrade or pin compatible Starlette/httpx versions.
3. Add `-W error::DeprecationWarning` for project-owned modules while temporarily filtering only documented third-party warnings.

Acceptance: the normal suite passes with no project-owned deprecation warning.

## 9. Recommended repair order and final release gate

1. Rotate the exposed credential immediately.
2. Fix Android compilation (P0-01).
3. Correct the recommendation public contract and regenerate clients (P0-03).
4. Implement exact client parity and Android API generation/checks (P0-02, P1-05).
5. Repair Web provenance and Backend test isolation (P1-06, P1-07).
6. Add and pass the real-stack release gate (P1-08).
7. Enforce the release URL, update docs, and clear warnings.

Release only when all of the following are true:

- Backend OpenAPI validation and all backend tests pass from `clean`.
- Web `api:check`, `api:coverage`, unit/coverage, build, and both mocked and real-stack Playwright projects pass.
- Android reports 83/83 API coverage, and unit, lint, debug/release builds, instrumentation, and real-stack emulator tests pass.
- All intelligence suites pass from their actual working directories with the documented shared configuration.
- Live probes show stable authenticated links, propagated correlation IDs, bounded timeouts, and tested fallback behavior.
- Web and Android can create, read, update, and act on the same server-owned records with equivalent privacy and safety semantics.

## 10. Repair completion and final acceptance

### 10.1 Defect resolution matrix

| Finding | Priority | Resolution | Verification |
|---|---:|---|---|
| P0-01 Android Kotlin/CI compilation failure | P0 | Restored the missing cooking answer model, removed duplicate decision declarations and overload ambiguity, aligned call sites, and added generated API checks. | `apiCheck clean testDebugUnitTest assembleDebug lintDebug compileDebugAndroidTestKotlin` passed; usable debug APK generated. |
| P0-02 Web/Android functional and interface drift | P0 | Added the 20 missing Android operations and server-backed inventory, shopping, import, and recipe flows; covered the 3 Web operations; removed exemptions; aligned filters, DTO fields, and non-empty decision bodies. | Both coverage gates report **83/83**; real cross-device CRUD and cooking operations passed. |
| P0-03 invalid `RecommendationResponse` public contract | P0 | Corrected enum values and nullability in Backend OpenAPI, regenerated Web/Android models, removed the Web cast, and added status-by-status Backend serialization validation. | Backend contract tests, Web type checking, and Android API/model checks passed. |
| P0-04 exposed credential | Excluded | Credential rotation was deliberately not performed, per task instruction. Configuration hardening was completed without changing or exposing the secret. | No credential file/value was changed or committed. |
| P1-05 no Android API synchronization gate | P1 | Added Gradle `apiGenerate`, `apiCheck`, and `apiCoverage` tasks tied to the canonical Backend OpenAPI document. | `apiCheck` and `apiCoverage` pass at 83/83 with no duplicate methods. |
| P1-06 Web API lock provenance drift | P1 | Locked both the normalized contract and the real Backend source SHA, and updated `npm run api:check` to validate both. | Full Web validation passed against Backend contract commit `b108291`. |
| P1-07 nondeterministic Backend chat test | P1 | Replaced the default live dependency with a deterministic mock; moved the live probe to an opt-in profile. | Offline Backend clean suite passed **202 tests, 0 failures/errors/skips**. |
| P1-08 no real-stack release gate | P1 | Added container builds, health checks, persistent Cooking task storage, and a no-interception Compose/Playwright/Android test path. | Cold `docker compose up -d --build --force-recreate` passed; all six services plus Postgres healthy; Web and Android real-stack suites passed. |
| P2-09 placeholder Android production URL | P2 | Added release-time validation that rejects placeholder/example domains and accepts an explicitly configured HTTPS production origin. | Default release configuration fails safely; `https://api.foodmind.test/api/v1/` passes configuration. |
| P2-10 stale parity and local setup documentation | P2 | Updated API, parity, task-storage, environment, and real-stack instructions; added a documentation consistency checker. | Documentation checker passes all **22** governed documents. |
| P3-11 Cooking deprecation warnings | P3 | Updated owned deprecated usages and aligned the test dependency set. | Cooking suite passed **1,218 tests with zero warnings**; Ruff passed. |

### 10.2 Automated verification record

| Component | Executed acceptance gate | Result |
|---|---|---:|
| Backend | `./mvnw clean test` | **PASS — 202/202** |
| Web | `npm run validate` | **PASS — API 83/83, lint, types, 78 unit tests, coverage, production build** |
| Web real stack | `npm run test:e2e:real` | **PASS — 3/3, no API interception** |
| Android CI-compatible gate | `gradlew apiCheck clean testDebugUnitTest assembleDebug lintDebug compileDebugAndroidTestKotlin` | **PASS — 65 tasks, 42 unit tests, lint clean, APK produced** |
| Android real stack | `gradlew connectedDebugAndroidTest -Pandroid.testInstrumentationRunnerArguments.realStack=true` | **PASS — 3/3 on Pixel 8 Pro API 36 emulator** |
| Intelligence Cooking | `uv run pytest -q` and `uv run ruff check .` | **PASS — 1,218/1,218, zero warnings** |
| Intelligence Recommendation | `uv run pytest -q` and `uv run ruff check .` | **PASS — 171 passed, 1 skipped** |
| Intelligence Chat | `uv run pytest -q` and `uv run ruff check .` | **PASS — 4/4** |
| Intelligence Inference | `uv run pytest -q` and `uv run ruff check .` | **PASS — 3/3** |
| Documentation | `python testing/check_parity_docs.py` and Compose config validation | **PASS — 22 documents, valid stack definition** |

Web coverage after the final source change was 93.23% statements, 81.96% branches, 96.15% functions, and 96.79% lines. The Android Debug APK is emitted at `foodmind-android/app/build/outputs/apk/debug/app-debug.apk` and was installed on the emulator used below.

### 10.3 Real interactive frontend operation record

All actions used account `parity-e2e-20260811@example.test` against the rebuilt real Backend and intelligence stack. No Playwright route interception, fake API server, or Android mock repository was active.

| Business operation | Web Playwright browser | Android emulator | Server/cross-device result |
|---|---:|---:|---|
| Login and authenticated session | PASS | PASS | Same account and server data visible on both clients. |
| Inventory add/edit/delete and filters | PASS | PASS | Web-created lentils appeared on Android; Android-created chickpeas appeared on Web and were then archived. Empty-filter result rendered normally. |
| Shopping list create/complete | PASS | PASS | Completion persisted to Backend inventory; the completed list and item state matched cross-device. |
| Recipe import submit/answer/confirm | PASS | PASS | Ambiguous input produced questions; servings/ingredient answers persisted; confirmation created a server recipe. |
| Cloud recipe create/read/update/delete | PASS | PASS | Records created or edited on one client synchronized to the other and deletion persisted. |
| Cooking generate, decision, purchase, cancel | PASS | PASS | Confirmation decisions generated Ready plans; “buy missing” created a server shopping list; asynchronous cancellation persisted `TASK_CANCELLED`. |
| Recommendation rendering | PASS | PASS | Both clients rendered the successful recommendation candidate response without manual casts or crashes. |
| Chat send/receive | PASS | PASS | Messages traversed Backend to the real Chat service and rendered on both clients. |
| Page navigation and deep links | PASS | PASS | All functional destinations opened without blank screens or activity crashes. |
| Empty, error, and query-filter states | PASS | PASS | Empty search/filter states and a missing Web route rendered explicit recoverable UI. |

Representative interactive evidence:

- [Web cooking ready state](evidence-web-cooking-ready.png)
- [Web inventory after Android synchronization](evidence-web-after-android-sync.png)
- [Web cross-device inventory detail](evidence-web-inventory-cross-device.png)
- [Android cooking parity flow](evidence-android-cooking-parity.png)
- [Android persisted cancellation result](evidence-android-cooking-cancelled.png)

### 10.4 Communication and persistence checks

- Backend health, liveness, and readiness returned `UP` after a cold image rebuild.
- Cooking readiness reported validated settings, a compiled graph, and a ready persistent task API.
- Recommendation reached Inference and returned typed candidates; Chat returned a real service response; Cooking sync and async flows both completed.
- Cross-device records were verified through the UI and direct server persistence, including the cancelled plan `792a6682-432f-44cb-bae3-f17a4410f5a7` with status `FAILED` and error `TASK_CANCELLED`.
- Repeated test-fixture submissions are idempotent enough for the real-stack CI probe, and client polling has bounded error handling instead of leaving pages indefinitely busy.

### 10.5 Repair commits

| Repository | Atomic priority commits |
|---|---|
| Backend | `266d354` P0 recommendation contract; `b108291` P0 cooking decisions; `be0e907` P1 offline chat/container build |
| Web | `cffd339` P0 parity; `4db3082` P1 API lock/real E2E; `6eb28a2` P2 guides; `6e3c20a` P1 real-agent latency |
| Android | `dd47b09` P0 parity/build; `b224f6a` P1 API/real-stack gates; `4063530` P2 release/docs; `2312b5e`, `ca294a9` P1 stable real probes |
| Intelligence | `810b0bc` P0 configuration; `84fe8ec` P1 persistent tasks; `fab2085` P3 warnings |

All application changes are on `fix/e2e-test-blocker-20260811`. Each repository is pushed independently and represented by a draft PR targeting its default branch:

| Repository | Draft PR | Target |
|---|---|---|
| Backend | [foodmind-backend#26](https://github.com/foodmind-team/foodmind-backend/pull/26) | `master` |
| Web | [foodmind-web#11](https://github.com/foodmind-team/foodmind-web/pull/11) | `master` |
| Android | [foodmind-android#9](https://github.com/foodmind-team/foodmind-android/pull/9) | `master` |
| Intelligence | [foodmind-intelligence#61](https://github.com/foodmind-team/foodmind-intelligence/pull/61) | `main` |
| Documentation | [foodmind-docs#8](https://github.com/foodmind-team/foodmind-docs/pull/8) | `main` |

The PRs are intentionally left unmerged for manual review.

## Appendix A — exact client operation differences

**Web-only relative to Android (19):**

- `POST /cooking-plans/{planId}/decisions-async`
- `POST /cooking-plans/{planId}/shopping-list`
- `GET /inventory/lots`
- `POST /inventory/lots`
- `PUT /inventory/lots/{lotId}`
- `DELETE /inventory/lots/{lotId}`
- `GET /shopping-lists`
- `GET /shopping-lists/{shoppingListId}`
- `PATCH /shopping-lists/{shoppingListId}/items/{itemId}`
- `POST /shopping-lists/{shoppingListId}/complete`
- `POST /recipe-imports`
- `GET /recipe-imports/{importId}`
- `POST /recipe-imports/{importId}/answers`
- `POST /recipe-imports/{importId}/confirm`
- `GET /recipes`
- `POST /recipes`
- `GET /recipes/{id}`
- `PUT /recipes/{id}`
- `DELETE /recipes/{id}`

**Android-only relative to Web (2):**

- `POST /cooking-plans/generate`
- `POST /cooking-plans/{planId}/decisions`

**Implemented by neither client (1):**

- `GET /inventory/lots/{lotId}`

## Appendix B — backend schema names not represented by same-named Android types

1. `ChatMessagePageResponse`
2. `CookingPlanAssumption`
3. `CookingPlanCompletionItem`
4. `CookingPlanConfirmationQuestion`
5. `CookingPlanDecision`
6. `CookingPlanDishCompletion`
7. `CookingPlanLotAllocation`
8. `CookingPlanMiseEnPlaceItem`
9. `CookingPlanPolicySource`
10. `CookingPlanQuestionOption`
11. `CookingPlanRepairOption`
12. `CookingPlanSafetyPolicy`
13. `CookingPlanSource`
14. `CookingPlanTimelineTask`
15. `CookingQuestionAnswer`
16. `CreateRecipeImportRequest`
17. `ExploreResultResponse`
18. `ExploreSourceType`
19. `HardConstraintSummary`
20. `HistoryBucket`
21. `InventoryLotPageResponse`
22. `InventoryLotRequest`
23. `InventoryLotResponse`
24. `PageResponse`
25. `RecipeImportAnswer`
26. `RecipeImportAnswerRequest`
27. `RecipeImportAnswersRequest`
28. `RecipeImportDraft`
29. `RecipeImportQuestion`
30. `RecipeImportResponse`
31. `RecommendationMoney`
32. `SearchResultResponse`
33. `SearchSourceType`
34. `ShoppingListItemResponse`
35. `ShoppingListPageResponse`
36. `ShoppingListResponse`
37. `UpdateShoppingListItemRequest`
38. `UserRecipePageResponse`
39. `UserRecipeRequest`
40. `UserRecipeResponse`
41. `WantToTrySourceType`

## Appendix C — evidence file index

- Backend public contract: `foodmind-backend/src/main/resources/openapi/openapi.yaml`
- Backend runtime recommendation assertion: `foodmind-backend/src/test/java/com/foodmind/foodmindbackend/recommendation/RecommendationAgentFlowTest.java`
- Backend Chat defaults/test: `foodmind-backend/src/main/resources/application.properties`, `foodmind-backend/src/test/java/com/foodmind/foodmindbackend/chat/ChatFlowTest.java`
- Backend Cooking wire DTO/adapter: `foodmind-backend/src/main/java/com/foodmind/foodmindbackend/cooking/domain/agent/AgentGeneratePlanRequest.java`, `foodmind-backend/src/main/java/com/foodmind/foodmindbackend/integration/agent/CookingAgentHttpAdapter.java`
- Web routes/runtime cast: `foodmind-web/src/app/router/router.tsx`, `foodmind-web/src/routes/HomeRoutes.tsx`
- Web contract gates: `foodmind-web/contracts/backend-api-coverage.json`, `foodmind-web/contracts/backend-openapi-v1.lock.json`, `foodmind-web/scripts/check-api.mjs`
- Web mocked E2E boundary: `foodmind-web/e2e/fixtures/api.ts`
- Android API/models: `foodmind-android/app/src/main/java/com/foodmind/foodmind_android/core/network/FoodMindApi.kt`, `ApiModels.kt`, `FoodMindNetwork.kt`
- Android local recipes/routes: `foodmind-android/app/src/main/java/com/foodmind/foodmind_android/domain/repository/RecipeDraftRepository.kt`, `foodmind-android/app/src/main/AndroidManifest.xml`
- Android release URL: `foodmind-android/app/build.gradle.kts`
- Cooking configuration/docs: `foodmind-intelligence/agent-service/app/agents/cooking/src/cooking_plan_agent/config/settings.py`, `foodmind-intelligence/agent-service/app/agents/README.md`
- No-mock full stack: `foodmind-docs/testing/full-stack/compose.yaml`
- Web interactive screenshots: `foodmind-docs/testing/evidence-web-cooking-ready.png`, `evidence-web-after-android-sync.png`, `evidence-web-inventory-cross-device.png`
- Android interactive screenshots: `foodmind-docs/testing/evidence-android-cooking-parity.png`, `evidence-android-cooking-cancelled.png`
