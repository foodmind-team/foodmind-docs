# FoodMind DevSecOps v4 — Mac execution handover

**Prepared:** 2026-08-18 (Asia/Singapore)  
**Owner for execution:** Mac-side presentation editor  
**Goal:** Create a corrected, presentation-ready v4 from the existing v3 deck; add a standalone presenter script; commit and push only the two new v4 deliverables to `foodmind-docs/main`.

## 1. Inputs and outputs

Use the existing deck as the visual template. Duplicate it; do not edit v3 in place.

| Item | Path / name |
| --- | --- |
| Source deck | `presentation/slides/FoodMind-DevSecOps-Presentation-v3.pptx` |
| New deck | `presentation/slides/FoodMind-DevSecOps-Presentation-v4.pptx` |
| New script | `presentation/scripts/FoodMind-DevSecOps-Presentation-v4-script.md` |
| Repository | `foodmind-docs`, branch `main` |

Keep the v3 master, typography, palette, slide numbering and layout language. Retain 12 slides unless splitting the architecture slide is necessary for legibility. Do not expose tokens, AWS account credentials, environment files, GitHub token output, SSM parameter values, or personal data.

## 2. What is accurate, and what must be corrected

The intended story is valid: a change is checked, scanned before image publication, deployed through short-lived identity with digest-pinned artifacts, and assessed in the running staging environment.

However, the v3 deck uses an older verified chain (`3496a39b`, run IDs `31949…`) and makes a few claims that are broader than the current implementation proves.

### Latest verified successful evidence chain

Use this chain in v4, after re-running the verification commands below immediately before presenting:

| Stage | Latest verified successful run | Infra SHA |
| --- | ---: | --- |
| Compose integration | [31976983656](https://github.com/foodmind-team/foodmind-infra/actions/runs/31976983656) | `b7ef36cdb57b54b7ded623f0508d9fe15ca49ec9` |
| Publish staging images | [31977105758](https://github.com/foodmind-team/foodmind-infra/actions/runs/31977105758) | same |
| Deploy staging | [31977378261](https://github.com/foodmind-team/foodmind-infra/actions/runs/31977378261) | same |
| Staging DAST | [31977624736](https://github.com/foodmind-team/foodmind-infra/actions/runs/31977624736) | same |
| Scheduled JMeter smoke | [31992358944](https://github.com/foodmind-team/foodmind-infra/actions/runs/31992358944) | same |

The publication artifact reports:

```text
release_id: staging-b7ef36cdb57b-31977105758-1
images: 7, each recorded as an ECR sha256 digest
database_migrations: true
```

The most recent JMeter run recorded 20 samples, 0 errors, and `p95_ms: 876` against a policy of p95 <= 2000 ms. The public `https://13.229.2.154.sslip.io/healthz` endpoint returned `ok` and the expected security headers during review, but it does not expose a release version. Therefore call the manifest **the latest verified successful release**, not an independently version-confirmed live release.

### Claims that must be qualified

1. **Merge enforcement:** Workflows fail at their configured threshold, but enforced branch policy is not universal. At review time, Web required only `validate`; Intelligence and ML required their aggregate gates; Backend, Android, Infra and Docs returned no classic branch protection/ruleset. Do not claim that every Medium+ finding universally blocks merging. Say: *“Relevant workflows fail on their policy threshold; universal required-check enforcement is the next hardening item.”*
2. **No CVSS equivalence:** Do not equate CodeQL “Medium” with CVSS 4.0. Use “Medium+ policy threshold” only.
3. **Artifact failure policy:** Some artifact uploads use `if-no-files-found: ignore` or `warn`. Do not claim that all missing evidence fails closed. Say: *“Security controls fail the workflow; selected diagnostic uploads are best-effort.”*
4. **Container result:** The seven-image Trivy policy scans `MEDIUM,HIGH,CRITICAL` with `--ignore-unfixed`. If preserving the 142-to-0 story, label it **historical baseline** and say **“0 fixable Medium+ findings under the declared scanner policy”**, never “zero risk” or “zero vulnerabilities.”
5. **DAST:** This is a passive, unauthenticated ZAP baseline. Its policy has named accepted CSP/COEP exceptions. It is post-deployment HTTP assurance, not a full authenticated application penetration test.
6. **Performance:** 20 samples are a lightweight availability/latency smoke, not a capacity, load, endurance, or production-SLO proof.
7. **Rollback:** `scripts/cd/deploy-staging.sh` includes automatic restoration of the captured prior image set when candidate startup or verification fails. State that the rollback path is **implemented**. Do not state that a rollback drill has been independently evidenced unless a real drill is shown.
8. **Topology:** There are six product repositories plus Infra as delivery control plane. The `model-package` image is a one-shot release job, not a seventh continuously running service. Do not describe all seven images as seven microservices.
9. **Availability and privacy:** This is a single-EC2 / Single-AZ RDS cost-controlled staging demo; do not imply high availability. Also do not claim the repositories are private: the GitHub repositories were visible as public during review, while Docs describes restricted material. Treat that as a remediation item, not a claim of completed security.

## 3. Slide-by-slide revision plan

| Slide | Keep | Revise |
| --- | --- | --- |
| 1 | Title and six-step visual | If not presenting on 19 Aug, replace the date. Add no new “production” claim. |
| 2 | Operating-loop framing | Change the analysis caption to “SAST, SCA and repository-specific secret checks”; retain fast-feedback vs later assurance. |
| 3 | Brand and overall architecture idea | Best: split into two slides if time permits—(a) public/private/offline trust boundaries, (b) delivery evidence chain. If kept as one, enlarge it and narrate only the three boundaries; do not read every logo. Remove/soften green check marks that imply universal enforcement. |
| 4 | CI structure | Replace the red callout with: **WORKFLOW POLICY / Medium+ findings fail the relevant check / Universal required-check enforcement is next.** Remove `CVSS 4.0` and “Fail closed when evidence is missing or incomplete.” Add a small footnote: “Controls vary by repository; Android has no workflow secret scan.” |
| 5 | Build -> SBOM -> Trivy -> ECR sequence | Keep seven-image list. Change bottom copy to “Each candidate is scanned before push; the policy blocks fixable Medium+ findings. SBOM and Trivy JSON are retained for audit.” Call Model Package a release job if explained verbally. |
| 6 | OIDC -> IAM -> SSM -> Compose sequence | Change title to **“AWS credentials are temporary; a rollback path is automated.”** Replace “rollback is automatic” wording with “candidate readiness/verification failure restores the captured previous image set.” Add “single-EC2 staging; not HA” in speaker notes. |
| 7 | Evidence-chain format | Update all run IDs to 31976983656, 31977105758, 31977378261, 31977624736 and 31992358944. Change “CURRENT RELEASE” to **“LATEST VERIFIED SUCCESSFUL RELEASE”**. |
| 8 | Detect -> fix -> re-scan layout | Label before count as **“Historical baseline: six images”**. Label result as **“Seven release images: 0 fixable Medium+ under declared policy”**. Keep the zero-risk caveat prominent. |
| 9 | Assurance metrics | Update p95 to **876 ms**. Change title to **“Latest staging smoke passes post-deployment assurance”**. Change “20 samples” to “20-request smoke”; add “Passive unauthenticated ZAP; accepted exceptions are documented.” |
| 10 | Five-screen demo order | Update run IDs. The last item should read “Latest verified release manifest + live `/healthz` + ZAP + JMeter”. Preserve 5–7 minutes. |
| 11 | Local backup | Keep only repository-relative locations. Remove the Mac-specific `/Users/huangqijun/...` paths from speaker notes. State that local files explain implementation; GitHub Actions evidence is the primary proof. |
| 12 | Close | Change title to **“The staging release path is implemented and evidenced.”** Update SHA/release ID/p95. Replace “All application security gates are merged” with **“Security workflows are configured; universal merge enforcement remains next.”** End with the next two hardening actions: enforce required checks and record a rollback drill. |

## 4. Required speaker notes and standalone script

Create the standalone script file named above. Add equivalent concise notes to the relevant slides, including a `[Sources]` block on every externally verifiable claim. The visible slides should remain concise; do not add presenter prose to slide bodies.

### Slide 1 — 20 seconds

> This is not a list of DevSecOps tools. It is the evidence path for one staging release: a reviewable change is tested, scanned before registry publication, deployed by immutable digest with short-lived AWS identity, and checked again in the running environment. I will show the design, the latest verified evidence chain, and a five-minute demo.

### Slide 2 — 35 seconds

> We apply fast feedback close to the pull request, then run integration, image, runtime and monitoring controls when an environment exists. This preserves developer speed without pretending that a unit test alone proves a safe deployment.

### Slide 3 — 45 seconds

> The public boundary is Spring Boot: Web and Android call `/api/v1`, not Agent or inference services. Intelligence hosts private Agent and inference workloads. ML remains offline and produces an immutable model package. Infra is the integration and release control plane.

### Slide 4 — 45 seconds

> The workflows test correctness and run CodeQL and dependency checks at their defined policy thresholds. One important qualification: a failed relevant workflow fails, but universal GitHub required-check enforcement is not yet complete across every repository. That is a hardening action, not a completed claim.

### Slide 5 — 45 seconds

> The publication workflow builds seven release artifacts. For each candidate, it generates a CycloneDX SBOM, scans before push, and publishes only after the configured fixable Medium-or-higher policy passes. The release manifest records ECR SHA-256 digests, so the deploy step uses the exact scanned artifact.

### Slide 6 — 45 seconds

> GitHub uses OIDC to assume a short-lived, constrained AWS role; no long-lived AWS access key is stored in the workflow. Systems Manager deploys digest-pinned images to the staging EC2 host without SSH. If candidate startup or verification fails, the deployment script restores the previous captured image set. This is a staging design, not a high-availability platform.

### Slide 7 — 50 seconds

> Here is the latest verified successful chain: Compose validation, secure image publication, deployment, passive DAST, and scheduled smoke performance. The linked manifest is `staging-b7ef36cdb57b-31977105758-1`; it records seven immutable ECR digests. I call it the latest verified release because the public health endpoint does not publish a version string.

### Slide 8 — 45 seconds

> This is a historical remediation result, not a permanent zero-risk claim. The baseline found 142 fixable Medium-or-higher findings in six images. After OS and dependency remediation and runtime reduction, the declared policy reported zero fixable Medium-or-higher findings across the seven-release-image scan. Unfixed findings and new vulnerabilities still require ongoing monitoring.

### Slide 9 — 45 seconds

> The latest 20-request staging smoke had zero errors and a p95 of 876 milliseconds, below the two-second policy. This is a lightweight smoke signal, not a load-capacity claim. ZAP is passive and unauthenticated, and its documented CSP and COEP exceptions remain explicit.

### Slide 10 — 5 to 7 minutes

> I will open five preloaded tabs: the application PR checks, Compose run 31976983656, publish run 31977105758, deploy run 31977378261, then the release manifest, live health endpoint, DAST and JMeter evidence. I will show summaries and artifacts only; I will not open secrets, tokens, AWS parameter values or environment files.

### Slide 11 — 45 seconds, backup only

> If the network is unstable, the repository-relative source files explain the same controls: `releases/staging-source.json`, the publish workflow, the deployment script and the verification script. Local source explains implementation; successful GitHub Actions artifacts remain the primary operational evidence.

### Slide 12 — 30 seconds

> FoodMind has an implemented, evidenced staging release path: digest-pinned image publication, temporary AWS identity, controlled deployment, runtime checks and retained artifacts. The next hardening work is explicit: make the required merge checks universal and retain proof from a deliberate rollback drill.

## 5. Re-verify immediately before editing/presenting

Run these commands from a GitHub-authenticated Mac shell. If the SHA, run IDs or metrics have changed, refresh slides 7, 9, 10, 12 and the script; never keep stale “current” values.

```bash
gh run view 31976983656 --repo foodmind-team/foodmind-infra --json conclusion,headSha,url
gh run view 31977105758 --repo foodmind-team/foodmind-infra --json conclusion,headSha,url
gh run view 31977378261 --repo foodmind-team/foodmind-infra --json conclusion,headSha,url
gh run view 31977624736 --repo foodmind-team/foodmind-infra --json conclusion,headSha,url
gh run view 31992358944 --repo foodmind-team/foodmind-infra --log | grep -E 'p95_ms|JMeter gate passed|Err:'

tmpdir="$(mktemp -d)"
gh run download 31977105758 --repo foodmind-team/foodmind-infra --name staging-release --dir "$tmpdir"
cat "$tmpdir/release-manifest.json"
curl --fail --silent --show-error https://13.229.2.154.sslip.io/healthz
curl --fail --silent --show-error --head https://13.229.2.154.sslip.io/healthz
```

## 6. Mac editing and QA checklist

1. Duplicate v3 to the v4 output name before editing.
2. Preserve all master/layout relationships, typography, logos, slide numbers and footer styling.
3. Replace obsolete run IDs and old release values everywhere, including speaker notes and hyperlinks.
4. Remove the old `/Users/huangqijun/Documents/ADProject/...` note paths.
5. Verify no content overlaps, clips, wraps unexpectedly, or falls below the deck's existing body-text size.
6. Render/export every final slide to PDF or PNG and review each at full slide size. Confirm the architecture slide is legible on a projected screen.
7. Check that every visible technical claim is either qualified as above or backed by a current run/artifact. Preserve `[Sources]` notes.
8. Keep a presentation fallback: exported PDF plus pre-opened browser tabs. Do not show raw GitHub credential status, `.env` files, release manifest account details, token output, AWS console secrets, or SSM command payloads.

## 7. Git delivery

Do not commit the PowerPoint lock file (`presentation/slides/~$FoodMind-DevSecOps-Presentation-v3.pptx`) or any export/preview artifacts. First confirm the worktree and remote state; then stage only the v4 deck and v4 script.

```bash
git status --short
git fetch origin --prune
git pull --ff-only origin main

git add \
  presentation/slides/FoodMind-DevSecOps-Presentation-v4.pptx \
  presentation/scripts/FoodMind-DevSecOps-Presentation-v4-script.md
git diff --cached --stat
git commit -m "docs(presentation): correct DevSecOps evidence and script"
git push origin main

git fetch origin --prune
git rev-list --left-right --count HEAD...origin/main
git status --short
```

Expected final divergence is `0\t0`; the lock file should either be absent after PowerPoint closes or remain untracked and unstaged.

## 8. Primary repository sources

- `foodmind-infra/.github/workflows/compose.yml`
- `foodmind-infra/.github/workflows/publish-staging.yml`
- `foodmind-infra/.github/workflows/deploy-staging.yml`
- `foodmind-infra/.github/workflows/security-dast.yml`
- `foodmind-infra/.github/workflows/performance-jmeter.yml`
- `foodmind-infra/scripts/cd/publish-staging-images.sh`
- `foodmind-infra/scripts/cd/deploy-staging.sh`
- `foodmind-infra/scripts/verify-aws-demo.sh`
- `foodmind-infra/docs/security/devsecops-security-testing-report-2026-08-14.md`
- `foodmind-infra/docs/branch-protection-rollout.md`
- `foodmind-backend/README.md`
- `foodmind-web/README.md`
- `foodmind-ml/README.md`

