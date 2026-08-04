Let me read the remaining workflow nodes and test files to complete my understanding.
The user wants me to continue with the walkthrough. I've now read all the key files and have a comprehensive understanding. Let me now read a few more files to complete the picture, then build the full walkthrough. Let me read the remaining files I haven't checked yet - the cooking plan agent's remaining workflow nodes, the tests, and a few more key files.

I have a very comprehensive understanding now. Let me read the remaining files I haven't checked - recommendation agent's domain models and error handling, cooking plan agent's remaining directories, and the CI files.

Let me read a few more critical files - CI workflows, test files, and remaining implementation details.
Now I have a very thorough understanding of the entire foodmind-intelligence repository. I need to read a few more files to be thorough - the recommendation agent's tests, the CI pipelines for both agents, and a few more implementation details. Let me also check the .github workflows.

Now I have a comprehensive understanding. Let me now prepare the comprehensive walkthrough presentation to the user. I have all the information I need. Let me update todos and present the one-page executive overview first as instructed by the user.
Now I have a thorough understanding of the entire repository. Let me present the walkthrough, starting with Section A: the one-page executive overview.

---

# FoodMind Intelligence — Repository Walkthrough

## A. One-Page Executive Overview

**FoodMind Intelligence** is a **private internal AI microservice** deployed alongside the main FoodMind backend (Java/Spring Boot). It hosts **two independent LangGraph agent services** that answer two distinct business problems:

| Agent                    | Problem it solves                                            | Configuration             |
| ------------------------ | ------------------------------------------------------------ | ------------------------- |
| **Recommendation Agent** | "From up to 100 meal candidates, pick up to 3 personalized recommendations with safe, explainable reasons." | `recommendation-agent-v2` |
| **Cooking Plan Agent**   | "From raw recipe text, extract a structured cooking plan with safety validation, inventory checks, and an optimized schedule." | `cooking-agent-v1`        |

**Key architectural facts:**

1. **No shared runtime.** Each agent is a separate Python process with its own Docker image, `pyproject.toml`, settings, and CI pipeline. They share nothing at runtime beyond git history and the contracts folder.

2. **Both use FastAPI** as the HTTP framework, `langgraph` for workflow orchestration, and `pydantic` for strict schema validation. Neither exposes gRPC.

3. **Authentication is constant-time Bearer token comparison** (or `X-Internal-Token` for cooking). This is an internal service-to-service call from Spring Boot — not end-user auth.

4. **Both are v2-only.** The Recommendation Agent rejects all contract versions except `recommendation-agent-v2`. The Cooking Plan Agent accepts `cooking-agent-v1`. Neither translates v1 payloads.

5. **The local recommendation agent has a fake inference client.** The real inference service (`recommendation-inference-v1`) is owned by a separate team. Production integration awaits external owner approval — the agent runs against local test doubles.

6. **The Cooking Plan Agent is far more mature**, with a complete 15-node LangGraph, OR-Tools CP-SAT scheduling, multi-region food-safety policies (USDA, SFA), Tavily web search integration, and a compat adapter that maps Spring Boot DTOs.

7. **Contracts are strict.** Every schema is validated with `extra="forbid"` and `strict=True`. Candidate count is capped at 100. Result count is capped at 3. Explanations cannot contain forbidden claims (`best`, `healthy`, `safe`, etc.). Response payloads are capped at ~256 KB.

8. **The repository is under active development** with pending external approvals. The `contracts/` folder explicitly marks fixtures as `"approvalPending": true`.

---

Before we continue to the repository tree and architecture diagrams, let me check your understanding with a few quick questions:

**Q1:** How many separate Python services run in the foodmind-intelligence repository?

**Q2:** True or False: The Recommendation Agent and Cooking Plan Agent share a single FastAPI process.

**Q3:** Which agent has a working recommendation selection with diversity-aware ranking, and which has a full CP-SAT scheduling solver?

*(Please answer these three, and I'll continue with Section B — the repository tree with explanations.)*