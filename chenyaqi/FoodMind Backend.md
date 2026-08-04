The user wants me to continue reading the remaining files. I still need to read:
1. Security configuration files (common/security/)
2. Auth application services (remaining)
3. Auth API request/response DTOs
4. Global exception handler
5. Integration layer files
6. Recommendation domain files (remaining)
7. Analytics files
8. Media files
9. WantToTry remaining files

Let me read these files directly now.

Now let me read the critical security and infrastructure files.
Now I have a complete picture of all the files. Let me read the key remaining files that haven't been read yet. Let me read the security configuration files, the global exception handler, and a few key application service files.

Now let me read the remaining key application files and the README to complete the picture.
Now I have a comprehensive view. Let me also read a few more key application service files and the README to provide a thorough walkthrough.

I now have a comprehensive understanding of this project. Let me compile a thorough walkthrough. I have read:

1. pom.xml - Dependencies
2. compose.yaml - Docker Compose
3. .env.example - Environment variables
4. application.properties - Main config
5. All profile-specific configs
6. FoodmindBackendApplication.java - Entry point
7. All security infrastructure (SecurityConfiguration, JwtIssuer, JwtAuthenticationFilter, InternalServiceAuthenticationFilter, DelegationTokenIssuer, InternalToolAuthorizer, SecurityProperties, FoodMindPrincipal)
8. GlobalExceptionHandler - Error handling
9. ErrorCode enum, ApiException, ApiErrorResponse, ApiFieldError, PageResponse
10. AuthController - Auth endpoints
11. All auth domain models (AuthSession, RefreshToken, ClientType)
12. All auth application services (LoginUser, RegisterUser, RefreshSession, AuthTokenService, AuthTokens)
13. User domain models (User, UserRole, UserStatus)
14. All catalog domain models (13 files)
15. All record domain models (17 files, including food, drink, history)
16. All group domain models (12 files, including group, membership, invitation, feed)
17. All search domain models (6 files)
18. All chat domain models (18 files, including agent models)
19. All cooking domain models (23 files, including agent models)
20. All recommendation domain models (65+ files including filter/fallback/reason/agent)
21. All analytics domain models (6 files)
22. All wanttotry domain models (5 domain files)
23. All media domain models (3 files)
24. All 12 Flyway migration files
25. All controllers (Auth, Group, History, Explore, Search, Media, Dashboard, WeeklyRecap, Recommendation, WantToTry)
26. Integration agent adapter files
27. Component diagram from architecture docs

Now I can provide a complete walkthrough.
Now I have a complete picture. Here's a thorough walkthrough of the entire FoodMind Spring Boot backend.

---

# FoodMind Backend — Complete Walkthrough

## 1. Project Identity

This is the backend for **FoodMind**, a food discovery & social platform built by **Chen Yaqi** (NUS). It's a **modular monolith** Spring Boot 4.1.0 application using **Java 17**.

---

## 2. Tech Stack

| Layer            | Technology                                                   |
| ---------------- | ------------------------------------------------------------ |
| Framework        | Spring Boot 4.1.0                                            |
| Language         | Java 17                                                      |
| Build            | Maven                                                        |
| Database         | PostgreSQL 18.4 (via Docker Compose)                         |
| ORM              | Spring Data JPA + Hibernate (validate-only, no DDL generation) |
| Migrations       | Flyway                                                       |
| Auth             | HMAC-SHA256 JWT (Nimbus JOSE+JWT)                            |
| Password Hashing | BCrypt                                                       |
| Object Storage   | AWS S3 SDK (local MinIO for dev)                             |
| API Docs         | springdoc-openapi (Swagger UI)                               |
| Testing          | JUnit 5, Testcontainers (PostgreSQL), ArchUnit               |
| Object Mapping   | Jackson (Tools Jackson)                                      |
| Observability    | Actuator (health/info/metrics), CorrelationIdFilter          |

---

## 3. Docker Compose (`compose.yaml`)

Two services:

- **postgres** (`postgres:18.4`) — database on port `5432`, data persisted via `foodmind-postgres-data` volume, healthcheck with `pg_isready`
- **minio** (`minio/minio`) — S3-compatible local object storage on ports `9000` (API) / `9001` (console), data persisted via `foodmind-minio-data` volume

---

## 4. Entry Point

[`FoodmindBackendApplication.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/FoodmindBackendApplication.java) — clean `@SpringBootApplication` with a standard `main` method. Nothing special — all configuration is externalized.

---

## 5. Configuration (`application.properties`)

Key decisions in [application.properties](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/application.properties):

| Setting                                                      | Value         | Why                        |
| ------------------------------------------------------------ | ------------- | -------------------------- |
| `server.shutdown=graceful`                                   | 20s timeout   | Clean shutdown for k8s     |
| `spring.jackson.deserialization.fail-on-unknown-properties=true` | Strict        | Rejects malformed JSON     |
| `spring.mvc.throw-exception-if-no-handler-found=true`        | Strict        | No silent 404s             |
| `spring.web.resources.add-mappings=false`                    | Off           | No static resources served |
| `spring.jpa.open-in-view=false`                              | Off           | Anti-pattern disabled      |
| `spring.jpa.hibernate.ddl-auto=validate`                     | Validate only | Flyway owns schema         |
| `spring.jpa.properties.hibernate.jdbc.time_zone=UTC`         | UTC           | Consistent timestamps      |
| `spring.flyway.enabled=true`                                 | On            | Schema managed via Flyway  |

**3 external AI agent integrations** configured:
- `foodmind.recommendation.agent.*` — recommendation generation
- `foodmind.cooking.agent.*` — cooking plan generation  
- `foodmind.chat.agent.*` — chat/conversation

Each agent has: `enabled`, `base-url`, `endpoint-path`, `service-token`, `contract-version`, `connect-timeout`, `read-timeout`, `max-response-bytes`.

**Media storage** (`foodmind.media.storage.*`) — S3-compatible upload, disabled by default (`MEDIA_ENABLED=false`), max 5MB per file.

**4 Spring profiles**: `local`, `docker`, `test`, `prod` — each with its own `application-{profile}.properties`.

---

## 6. Security Architecture

### 6.1 Security Filter Chain

[`SecurityConfiguration.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/common/security/SecurityConfiguration.java) defines a **stateless** security model:

```
CSRF: OFF
HTTP Basic: OFF  
Form Login: OFF
Session: STATELESS

URL Rules:
  /api/v1/auth/register   -> permitAll()
  /api/v1/auth/login      -> permitAll()
  /api/v1/auth/refresh    -> permitAll()
  /api/v1/**              -> authenticated()       (JWT required)
  /internal/v1/**         -> hasAuthority("SERVICE") (internal service token)
  actuator health/info    -> permitAll()
  everything else         -> denyAll()
```

**Two authentication filters** (in order):
1. `InternalServiceAuthenticationFilter` — runs first, handles internal service-to-service calls
2. `JwtAuthenticationFilter` — handles user JWT tokens

### 6.2 JWT Authentication Flow

[`JwtIssuer.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/common/security/JwtIssuer.java) uses **HMAC-SHA256** (symmetric key):

- `issueAccessToken(User)` → creates a JWT with `sub`=userId, `iss`, `aud`, `iat`, `nbf`, `exp`, `jti`, `role` claim
- `verify(String)` → parses, verifies signature, validates all claims, returns `VerifiedAccessToken(userId, role)`
- Requires secret ≥ 32 bytes

[`JwtAuthenticationFilter.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/common/security/JwtAuthenticationFilter.java):
1. Extracts `Authorization: Bearer <token>`
2. Verifies via `JwtIssuer.verify()`
3. Loads `User` from DB, checks `status == ACTIVE`
4. Sets `SecurityContextHolder` with `FoodMindPrincipal`

[`FoodMindPrincipal.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/common/security/FoodMindPrincipal.java) — simple record: `id`, `email`, `displayName`, `role`, `status`.

### 6.3 Internal Service Authentication

[`InternalServiceAuthenticationFilter.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/common/security/InternalServiceAuthenticationFilter.java):
- Only applies to `/internal/v1/**` paths
- Expects `Authorization: Bearer <INTERNAL_SERVICE_TOKEN>`
- Static token comparison (not user-based)
- Grants `SERVICE` authority

### 6.4 Delegation Tokens

[`DelegationTokenIssuer.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/common/security/DelegationTokenIssuer.java) — special-purpose JWT for AI agent tools:
- `issue(userId, traceId, scopes, referenceIds)` → 2-minute TTL token
- `typ` claim = `"foodmind-agent-delegation"`
- `scopes` claim: e.g., `CHAT_SEARCH`, `CHAT_REFERENCE_RESOLVE`
- `referenceIds` claim: list of UUIDs the agent is allowed to access

[`InternalToolAuthorizer.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/common/security/InternalToolAuthorizer.java) — validates that the caller has `SERVICE` authority PLUS the required delegation scope.

### 6.5 Refresh Token & Auth Session

[Refresh Token Rotation](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/auth/application/AuthTokenService.java):
- Each session gets a **token family** (`tokenFamilyId`)
- `RefreshToken.generate()` → 32-byte random hex + SHA-256 hash
- Raw token sent to client; only hash stored in DB
- On refresh, old session gets `rotatedAt` set, new session linked via `tokenFamilyId`
- If a rotated/revoked token is reused → entire token family is revoked (theft detection)

[`RefreshSession.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/auth/application/RefreshSession.java):
- `@Transactional(noRollbackFor = ApiException.class)` — revocations persist even when auth fails
- `SELECT ... FOR UPDATE` — prevents concurrent refresh of same session
- Checks user is still ACTIVE; if not, revokes the whole family

Session cleanup via [`AuthSessionCleanup`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/auth/application/AuthSessionCleanup.java) (`@Scheduled`).

### 6.6 CSRF Protection for Web

[`AuthController.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/auth/api/AuthController.java):
- `FM_REFRESH` cookie — HttpOnly, Secure, SameSite=Strict, path=`/api/v1/auth`
- `FM_CSRF` cookie — readable by JS, same security settings
- CSRF token is 32 random bytes (hex-encoded)
- Refresh token accepted from either cookie **or** JSON body (Android compatibility)

---

## 7. Error Handling

[`GlobalExceptionHandler.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/common/error/GlobalExceptionHandler.java) — `@RestControllerAdvice` covering:

| Exception                                            | HTTP Status | ErrorCode                        |
| ---------------------------------------------------- | ----------- | -------------------------------- |
| `ApiException`                                       | Custom      | Custom                           |
| `MethodArgumentNotValidException`                    | 400         | VALIDATION_ERROR                 |
| `HandlerMethodValidationException`                   | 400         | VALIDATION_ERROR                 |
| `ConstraintViolationException`                       | 400         | VALIDATION_ERROR                 |
| `HttpMessageNotReadableException` (unknown property) | 400         | VALIDATION_ERROR (UNKNOWN_FIELD) |
| `HttpMessageNotReadableException` (malformed)        | 400         | MALFORMED_JSON                   |
| `MissingServletRequestParameterException`            | 400         | VALIDATION_ERROR (REQUIRED)      |
| `MethodArgumentTypeMismatchException`                | 400         | VALIDATION_ERROR (TYPE_MISMATCH) |
| `NoHandlerFoundException` / 404s                     | 404         | RESOURCE_NOT_FOUND               |
| `DataIntegrityViolationException`                    | 409         | CONFLICT                         |
| `AccessDeniedException`                              | 403         | ACCESS_DENIED                    |
| `AuthenticationException`                            | 401         | AUTHENTICATION_REQUIRED          |
| `Exception` (catch-all)                              | 500         | INTERNAL_ERROR                   |

[`ErrorCode`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/common/error/ErrorCode.java) enum: `VALIDATION_ERROR`, `MALFORMED_JSON`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMITED`, `UPSTREAM_UNAVAILABLE`, `INTERNAL_ERROR`.

[`ApiErrorResponse`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/common/api/ApiErrorResponse.java) record: `timestamp`, `status`, `code`, `message`, `path`, `traceId`, `fieldErrors[]`.

Every response includes a `traceId` (correlation ID) for distributed tracing.

Error codes use `SCREAMING_SNAKE_CASE`; field names from Java beans are converted (e.g., `displayName` → `DISPLAY_NAME`).

---

## 8. Domain Model & Database

### 8.1 Flyway Migrations (12 versions)

All schema is managed declaratively by Flyway. Hibernate is set to `validate` — it verifies the schema matches entities but never modifies it.

| Migration                                                    | Content                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [V1](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V1__platform_extensions.sql) | `pg_trgm` extension, `foodmind_set_updated_at()` trigger function |
| [V2](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V2__identity_and_auth.sql) | `app_user`, `auth_session` tables with self-referencing FK chain + guard trigger |
| [V3](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V3__preferences.sql) | `cuisine`, `dietary_tag`, `allergen` taxonomies + `user_preference`, `user_cuisine_preference`, `user_dietary_tag`, `user_allergen`, `user_preferred_meal_type` |
| [V4](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V4__catalogue.sql) | `meal`, `place`, `place_meal`, `food_product`, `recipe`, `ingredient`, `recipe_ingredient`, `recipe_step` + junction tables |
| [V5](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V5__groups_and_records.sql) | `trusted_group`, `group_membership`, `group_invitation`, `media_asset`, `food_record`, `drink_record` |
| [V6](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V6__saved_search_and_explore.sql) | `want_to_try`, full-text search vectors (tsvector) on `food_record`/`place`/`food_product`, GIN + trigram indexes, `foodmind_search_documents_for_user()` + `foodmind_explore_documents_for_user()` functions |
| [V7](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V7__recommendations.sql) | `recommendation_session`, `recommendation_candidate`, `candidate_reason`, `recommendation_feedback`, `group_recommendation_share` |
| [V8](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V8__cooking.sql) | `cooking_plan`, `cooking_plan_input`, `cooking_plan_ingredient`, `cooking_plan_step`, `cooking_plan_warning` |
| [V9](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V9__chat.sql) | `chat_session`, `chat_message`, `chat_reference`, `chat_message_source` |
| [V10](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V10__cross_cutting_and_analytics.sql) | `idempotency_record`, `audit_event`, `foodmind_resolve_time_zone()`, 10+ analytics views (`analytics_consumption_*`, `analytics_spending_*`, `analytics_cuisine_*`, `analytics_recommendation_*`, `analytics_weekly_recap_v1`, `ml_interaction_export_*`) |
| [V11](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V11__seed_catalogue.sql) | Seed data: 5 cuisines, 2 dietary tags, 9 allergens, 8 meals, 4 places, 10 offerings, 4 place observations, 3 food products, 3 recipes |
| [V12](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/resources/db/migration/V12__active_group_authorised_search.sql) | Forward fix: `active_group` CTE in search/explore functions to exclude archived groups |

### 8.2 Database Design Patterns

- **UUID primary keys** — generated by application (not PostgreSQL), so no `uuid-ossp` extension
- **Optimistic locking** — every mutable table has a `version` column (integer)
- **`updated_at` trigger** — `foodmind_set_updated_at()` auto-sets `updated_at = statement_timestamp()` on row updates, ensuring it's authoritative even when writes bypass Hibernate
- **Soft deletes** — `food_record`, `drink_record`, `want_to_try` use `deleted_at`; `media_asset` uses `status = DELETED`; audit trail preserved
- **Guard triggers** — custom functions enforce business invariants at the database level (e.g., `auth_session` immutability, `recommendation_session` status transitions, `media_asset` soft-delete only)
- **Partial unique indexes** — e.g., `group_membership` enforces exactly one active OWNER per group
- **tsvector full-text search** — `food_record.search_vector`, `place.search_vector`, `food_product.search_vector` are GENERATED ALWAYS columns with weighted GIN indexes
- **pg_trgm indexes** — for fuzzy/prefix search on names
- **Permission-scoped search functions** — `foodmind_search_documents_for_user()` and `foodmind_explore_documents_for_user()` embed authorization logic (ownership + group membership + curation status) directly in SQL for performance

---

## 9. Bounded Contexts Walkthrough

### 9.1 Auth Context

```
auth/
  api/
    AuthController.java        → /api/v1/auth/{register,login,refresh,logout,logout-all}
    request/{LoginRequest,RegisterRequest,RefreshRequest}
    response/AuthTokenResponse
  application/
    LoginUser.java             → email+password → JWT + refresh tokens
    RegisterUser.java          → create user + issue tokens
    RefreshSession.java        → rotate token family
    LogoutSession.java         → revoke single session or all sessions
    AuthTokenService.java      → core token issuance / refresh rotation logic
    AuthSessionCleanup.java    → @Scheduled cleanup of expired sessions
    port/AuthSessionRepository
  domain/
    AuthSession.java           → session record with tokenFamilyId, rotation chain
    RefreshToken.java          → raw token + SHA-256 hash
    ClientType.java            → WEB, ANDROID
  infrastructure/
    JpaAuthSessionRepository   → JPA implementation with SELECT FOR UPDATE
```

**Auth flow**: Register → user created (ACTIVE) → `AuthTokenService.issueNewSession()` → refresh token (stored as cookie `FM_REFRESH`) + access token (15min JWT) + CSRF token. Login → verify password + status → update `lastLoginAt` → issue session. Refresh → verify refresh token hash → check not rotated/revoked → rotate to new session → if old rotation detected, revoke entire family (theft detection).

---

### 9.2 User Context

[`User.java`](file:///d:/DevRepo/MyProjects/FoodMind/foodmind-backend/src/main/java/com/foodmind/foodmindbackend/user/domain/User.java):
- Fields: `id`, `email`, `normalisedEmail`, `passwordHash`, `displayName`, `role`, `status`, `timeZone`, `createdAt`, `updatedAt`, `lastLoginAt`, `deactivatedAt`, `version`
- `role`: `USER` | `ADMIN`
- `status`: `ACTIVE` | `SUSPENDED` | `DEACTIVATED`
- Email case-normalised for uniqueness

---

### 9.3 Catalog Context

The catalog is the **food knowledge graph** — meals, places, products, recipes, and their relationships.

Key domain objects:
- **MealDetail** — a dish (e.g., Hainanese Chicken Rice) with cuisine, meal type, spice level, dietary tags, allergens, and offerings across places
- **PlaceDetail** — a restaurant/hawker center with type, area, GPS coordinates, price band, cleanliness observations, meal offerings
- **ProductDetail** — packaged food product (e.g., Unsweetened Soy Drink) with brand, price, dietary/allergen tags
- **OfferingCandidate** / **RecipeCandidate** — what gets sent to AI agents as context
- **CatalogueReferenceData** — aggregate of all reference lists (cuisines, dietary tags, allergens, meal types, place types) for frontend dropdowns

Cleanliness system: `PlaceObservation` records `observationType`, `score`, `note`, `sourceKind`, `observedAt` — used by recommendation filters.

---

### 9.4 Record Context

Food & drink consumption tracking.

**FoodRecord**: `mealId`, `mealNameSnapshot`, `placeId`, `placeNameSnapshot`, `cuisineId`, `occurredAt`, `price` (Money), `rating` (0.0-5.0), `comment`, `wouldEatAgain`, `visibility` (PRIVATE/GROUP), `groupId`, `mediaAssetId`

**DrinkRecord**: `drinkName`, `placeId`, `shopNameSnapshot`, `price`, `rating`, `sweetnessLevel`, `iceLevel`, `wouldBuyAgain`, `visibility`, `groupId`

Both validated via `FoodRecordValidation` / `DrinkRecordValidation` static validators checking: name length, money amount/currency, rating range, visibility+groupId consistency, expected version for updates.

**History system**: Unified timeline of food + drink records with:
- `HistoryPeriod`: DAY | WEEK | MONTH
- `HistoryBucket`: aggregated counts per time bucket
- `HistoryEntry`: per-record timeline entry
- `HistoryCursor`: Base64-encoded cursor for keyset pagination
- `HistoryFilter`: rich filtering (from/to, period, type, timezone, groupId, cuisineId, placeId)

---

### 9.5 Group Context

Social groups for sharing food records and recommendations.

- **TrustedGroup**: `id`, `name`, `description`, `createdByUserId`, `status` (ACTIVE/ARCHIVED)
- **GroupMember**: `membershipId`, `groupId`, `userId`, `displayName`, `role` (OWNER/MEMBER), `status` (INVITED/ACTIVE/LEFT/REMOVED), `joinedAt`, `endedAt`
- **GroupInvitation**: token-based invites with `expiresAt`, `maxUses`, `useCount`, status lifecycle
- **GroupFeedEvent**: unified timeline of group activity — food records + recommendation shares, with cursor-based pagination
- **GroupRecommendationShare**: member shares an AI recommendation to the group feed
- **GroupValidation**: enforces name length (3-80 chars), description length, invitation TTL, share message length

Critical constraint: ONE active OWNER per group (enforced by partial unique index).

---

### 9.6 Search & Explore Context

**Search** (`/api/v1/search?q=&types=&after=&page=0&size=20`):
- Full-text search across `FOOD_RECORD`, `FOOD_PRODUCT`, `PLACE`
- PostgreSQL tsvector with trigram fallback
- Permission-scoped: returns only user's own records + group-visible records + curated catalogue items
- Cursor-based pagination (enforces `page=0`)
- Type filter via comma-separated enum

**Explore** (`/api/v1/explore?types=&topics=&after=&size=20`):
- Discovery feed — group-visible content + curated catalogue
- Same cursor-based pagination
- Optional `topics` filter (≤200 chars)

Both backed by PostgreSQL functions `foodmind_search_documents_for_user()` and `foodmind_explore_documents_for_user()` that embed authorization logic and use the `active_group` CTE (V12) to exclude archived groups.

---

### 9.7 Chat Context

AI chat with food context grounding.

- **ChatSession**: conversation container with title and status (ACTIVE/ARCHIVED)
- **ChatMessage**: each message has `role` (USER/ASSISTANT), `content`, `route`, `responseStatus`, `correlationId`, `agentTraceId`
  - USER messages: route/status/traceId are null
  - ASSISTANT messages: route/status/traceId are non-null
- **ChatReference**: links a session to searchable sources (food records, products, places) with `origin` (USER_SHARED / MESSAGE_INTRODUCED)
- **ChatMessageSource**: links messages to references with `sequenceNo` and `groundingMetadata`
- **ChatRoute**: SEARCH | SUMMARY | COMPARE | NAVIGATION | OUT_OF_SCOPE
- **ChatResponseStatus**: SUCCEEDED | FALLBACK_SUCCEEDED | UNSUPPORTED | FAILED

Agent integration:
- `ChatAgentCommand` — sent to AI agent with delegation token, message context, shared references
- Agent returns `ChatAgentGenerationResult` which is validated by `ChatAgentResultValidator`:
  - IDs must match request
  - Answer ≤ 4000 chars
  - Sources ≤ 10
  - OUT_OF_SCOPE must have 0 sources
  - Source ordering and uniqueness enforced

---

### 9.8 Recommendation Context

The most complex bounded context — AI-powered food recommendations with filtering pipelines.

**Request Flow**:
1. User submits `GenerateRecommendationRequest` with constraints (budget, area, dietary, meal type, mood, etc.)
2. `RecommendationRequestContext` normalizes inputs
3. Context is enriched with `PreferenceEvidence` (user preferences) + `CandidateEvidence` objects (potential meals with rich evidence: pricing, cleanliness, distance, personal/group history, dietary/allergen compatibility)
4. **Hard Filter Pipeline** runs — 13 filter policies applied in sequence:

| Filter                                  | What it rejects                 |
| --------------------------------------- | ------------------------------- |
| `BudgetCurrencyFilterPolicy`            | Over budget / currency mismatch |
| `AreaDistanceFilterPolicy`              | Outside area / too far          |
| `AllergenFilterPolicy`                  | Contains user's allergens       |
| `RequiredDietaryTagFilterPolicy`        | Missing required dietary tags   |
| `SpiceFilterPolicy`                     | Too spicy                       |
| `CleanlinessEvidenceFilterPolicy`       | Below cleanliness threshold     |
| `DislikedCuisineFilterPolicy`           | User-disliked cuisine           |
| `RecentRepeatFilterPolicy`              | Recently eaten (≤1 day)         |
| `RequestedTimeAvailabilityFilterPolicy` | Not available at requested time |

5. Filtered candidates + context sent to **Recommendation AI Agent** via HTTP
6. Agent returns ranked candidates with `recommendationType` (PERSONAL/EXPLORATORY/GROUP_INSPIRED), `reasonCodes`, `explanation`
7. `AgentResultValidator` validates contract version, candidate limits, reason ordering, score ranges
8. If agent fails, **FallbackSelector** provides rule-based alternatives

**Feedback System**:
- Events: ACCEPTED | REJECTED | RERECOMMEND_REQUESTED | LATER_RATED | WOULD_EAT_AGAIN
- `RejectionReason`: TOO_EXPENSIVE (constraint 7d), TOO_FAR (7d), NOT_IN_MOOD (1d), DIETARY_CONCERN (14d), ALLERGEN_CONCERN (30d), RECENTLY_EATEN (14d), PLACE_CONCERN (14d), OTHER (no constraint)
- `FeedbackPolicy.validatePayload()` — validates event matrix (e.g., you can't ACCEPT+LATER_RATED in same event)
- Idempotency-protected via `idempotency_key`
- Temporary constraints derived from rejections affect future recommendations

**Training Snapshot**: `BuildTrainingSnapshot` exports ML-ready data via `ml_interaction_export_source_v1` view.

---

### 9.9 Cooking Context

AI-generated cooking plans from ingredients.

- **CookingPlanInput**: what the user has (ingredient name, quantity, unit, source MANUAL/AUTHORISED_PANTRY)
- **CookingPlanRequestContext**: constraints — servings, maxMinutes, maxBudget, dietary/allergen codes
- **CookingPreferenceRules**: required dietary tags + avoided allergens derived from user preferences
- **CookingPlanStatus** lifecycle: CREATED → PROCESSING → SUCCEEDED / FALLBACK_SUCCEEDED / NO_VALID_RECIPE / FAILED

Agent flow:
1. `CookingAgentCommand` sent with request context, preference rules, recipe candidates
2. Agent returns `CookingAgentGenerationResult` with ingredients, steps, warnings
3. `CookingPlanResultValidator` validates: contract version match, ID consistency, ingredient step contiguity, warning codes validity, constraint checks
4. Results stored as `CookingPlanIngredient` (with `availability`: AVAILABLE/TO_BUY), `CookingPlanStep`, `CookingPlanWarning`

---

### 9.10 Analytics Context

Read-only analytics via database views.

**Dashboard** (`/api/v1/analytics/dashboard`):
- `DashboardProjection` wraps `AnalyticsWindow` (from/to/timezone) + `MetricValue[]`
- Connects to 6+ PostgreSQL views: consumption counts/ratings, spending, cuisine distribution, repeat frequency, recommendation acceptance/rejection rates, candidate type selection
- `MetricValue`: `code`, `label`, `period`, `value` (BigDecimal), `unit`, `currency`, `samples`, `denominator`, `dimension`, `empty`

**Weekly Recap** (`/api/v1/analytics/recap`):
- `WeeklyRecapProjection` — concise weekly summary distinct from live dashboard
- Backed by `analytics_weekly_recap_v1` view

---

### 9.11 Want-To-Try Context

Bookmarking system for items to try later.

- `WantToTryItem`: `id`, `ownerUserId`, `source` (type + id), `note`, `sourceAvailable`, `sourceSummary`
- `WantToTrySourceType`: FOOD_RECORD | MEAL | FOOD_PRODUCT | PLACE
- `WantToTrySourceSummary`: title, subtitle, snippet, visibility info
- CRUD via `SaveWantToTry`, `ListWantToTry`, `DeleteWantToTry`
- Offset-based pagination (`WantToTryPage` with `totalItems`)

---

### 9.12 Media Context

Bounded upload lifecycle for user-generated media.

- **Status flow**: PENDING → (user confirms upload) → READY → (user deletes) → DELETED
- **Enforced by DB trigger**: `foodmind_guard_media_asset_mutation()` — only allows soft-delete, validates status transitions
- `CreateMediaUploadUseCase`: generates pre-signed S3 upload URL (5-min TTL), creates `MediaAsset` in PENDING state
- `FinaliseMediaUploadUseCase`: verifies object exists in S3, transitions to READY
- `DeleteMediaAssetUseCase`: marks as DELETED in DB, deletes from S3
- `MediaAssetCleanup`: `@Scheduled` job reaps expired PENDING uploads (15-min delay)
- Controller conditionally enabled via `@ConditionalOnProperty(foodmind.media.storage.enabled=true)`

---

### 9.13 Integration Layer

Three HTTP adapters for AI agent communication:

- **`RecommendationAgentHttpAdapter`** — calls recommendation agent, maps JSON DTOs ↔ domain objects
- **`CookingAgentHttpAdapter`** — calls cooking plan agent
- **`ChatAgentHttpAdapter`** — calls chat agent

All share:
- `AgentClientProperties` — base URL, endpoint path, service token, contract version, timeouts, max response bytes
- `AgentClientConfiguration` — Spring `@Configuration` for bean wiring
- Delegation token issuance for scoped access control
- Response validation via domain validators before storage

---

## 10. Package Architecture

The project follows a **modular monolith** with hexagonal/ports-and-adapters principles:

```
com.foodmind.foodmindbackend/
├── {bounded-context}/
│   ├── api/              → REST controllers, request/response DTOs
│   ├── application/      → use cases (services with @Transactional)
│   │   └── port/         → interfaces (ports) for infrastructure
│   ├── domain/           → domain models, enums, validation, policies
│   │   ├── agent/        → agent integration models
│   │   ├── filter/       → recommendation filter pipeline
│   │   ├── fallback/     → recommendation fallback logic
│   │   └── reason/       → recommendation reason codes & templates
│   └── infrastructure/   → JPA/JDBC repos, external adapters (S3, agents)
└── common/
    ├── api/              → shared API DTOs (ErrorResponse, PageResponse)
    ├── error/            → GlobalExceptionHandler, ErrorCode, ApiException
    ├── security/         → JWT, filter chain, auth filters
    └── validation/       → shared validation utilities
```

This provides: domain isolation, testability (ports can be mocked), and path to microservice extraction if ever needed.

---

## 11. Testing

Tests use **Testcontainers** for real PostgreSQL integration tests + **ArchUnit** for architecture rules. Test fixtures include:
- Contract tests for AI agents (valid/invalid responses in JSON)
- Flow tests for each bounded context (AuthFlow, CatalogFlow, FoodRecordFlow, etc.)
- Unit tests for JwtIssuer, validators

---

## 12. Summary

This is a **production-quality** Spring Boot backend with:
- **Stateless JWT auth** with refresh token rotation and theft detection
- **12 Flyway migrations** that completely own the database schema
- **DB-level guard triggers** enforcing business invariants
- **Permission-scoped SQL search functions** for performance
- **3 AI agent integrations** with contract versioning and validation
- **Recommendation engine** with 13-policy filter pipeline + fallback selector + feedback loop
- **Cursor-based pagination** (Base64-encoded) for search, explore, history, chat, group feeds
- **Idempotency**, **audit logging**, **analytics views**, **training data export**
- **Comprehensive error handling** with traceId on every response

The total file count is approximately **200+ Java source files** across 14 bounded contexts.