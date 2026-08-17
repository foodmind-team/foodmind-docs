# FoodMind DevSecOps v4 — Presenter script

Presentation: SA4106 AD Project — DevSecOps  
Date: 19 August 2026  
Audience: assessor and class

## 1. Opening — 20 seconds

This is not a list of DevSecOps tools. It is the evidence path for one staging release: a reviewable change is tested, scanned before registry publication, deployed by immutable digest with short-lived AWS identity, and checked again in the running environment. I will show the design, the latest verified evidence chain, and a five-minute demo.

Sources: GitHub Actions evidence chain listed in Slide 7; live `/healthz` check.

## 2. Operating loop — 35 seconds

We apply fast feedback close to the pull request, then run integration, image, runtime and monitoring controls when an environment exists. This preserves developer speed without pretending that a unit test alone proves a safe deployment.

Sources: FoodMind repository workflow configuration.

## 3. Toolchain architecture — 45 seconds

The public boundary is Spring Boot: Web and Android call `/api/v1`, not Agent or inference services. Intelligence hosts private Agent and inference workloads. ML remains offline and produces an immutable model package. Infra is the integration and release control plane.

Sources: `foodmind-backend/README.md`, `foodmind-web/README.md`, `foodmind-ml/README.md`, and the FoodMind architecture documentation.

## 4. Continuous integration — 45 seconds

The workflows test correctness and run CodeQL and dependency checks at their defined policy thresholds. One important qualification: a failed relevant workflow fails, but universal GitHub required-check enforcement is not yet complete across every repository. That is a hardening action, not a completed claim.

Sources: FoodMind repository GitHub Actions workflows; `foodmind-infra/docs/branch-protection-rollout.md`.

## 5. Secure supply chain — 45 seconds

The publication workflow builds seven release artifacts. For each candidate, it generates a CycloneDX SBOM, scans before push, and publishes only after the configured fixable Medium-or-higher policy passes. The release manifest records ECR SHA-256 digests, so the deploy step uses the exact scanned artifact. The Model Package is a one-shot release job, not a continuously running service.

Sources: `foodmind-infra/.github/workflows/publish-staging.yml`; publish run 31977105758; staging release manifest.

## 6. Continuous delivery — 45 seconds

GitHub uses OIDC to assume a short-lived, constrained AWS role; no long-lived AWS access key is stored in the workflow. Systems Manager deploys digest-pinned images to the staging EC2 host without SSH. If candidate startup or verification fails, the deployment script restores the previous captured image set. This is a single-EC2 staging design, not a high-availability platform.

Sources: `foodmind-infra/.github/workflows/deploy-staging.yml`; `foodmind-infra/scripts/cd/deploy-staging.sh`; deploy run 31977378261.

## 7. Pipeline demonstration evidence — 50 seconds

Here is the latest verified successful chain: Compose validation, secure image publication, deployment, passive DAST, and scheduled smoke performance. The linked manifest is `staging-b7ef36cdb57b-31977105758-1`; it records seven immutable ECR digests. I call it the latest verified successful release because the public health endpoint does not publish a version string.

Sources: Compose run 31976983656; publish run 31977105758; deploy run 31977378261; DAST run 31977624736; JMeter run 31992358944; live `https://13.229.2.154.sslip.io/healthz`.

## 8. Security testing report — 45 seconds

This is a historical remediation result, not a permanent zero-risk claim. The baseline found 142 fixable Medium-or-higher findings in six images. After OS and dependency remediation and runtime reduction, the declared policy reported zero fixable Medium-or-higher findings across the seven-release-image scan. Unfixed findings and new vulnerabilities still require ongoing monitoring.

Sources: `foodmind-infra/docs/security/devsecops-security-testing-report-2026-08-14.md`; publish run 31977105758.

## 9. Runtime assurance — 45 seconds

The latest 20-request staging smoke had zero errors and a p95 of 876 milliseconds, below the two-second policy. This is a lightweight smoke signal, not a load-capacity claim. ZAP is passive and unauthenticated, and its documented CSP and COEP exceptions remain explicit.

Sources: JMeter run 31992358944; DAST run 31977624736; live `/healthz` response headers.

## 10. Live pipeline demo — 5 to 7 minutes

I will open five preloaded tabs: the application PR checks, Compose run 31976983656, publish run 31977105758, deploy run 31977378261, then the release manifest, live health endpoint, DAST and JMeter evidence. I will show summaries and artifacts only; I will not open secrets, tokens, AWS parameter values or environment files.

Sources: GitHub Actions run URLs in the preloaded browser tabs.

## 11. Local backup — 45 seconds, only if needed

If the network is unstable, the repository-relative source files explain the same controls: `releases/staging-source.json`, the publish workflow, the deployment script and the verification script. Local source explains implementation; successful GitHub Actions artifacts remain the primary operational evidence.

Sources: FoodMind Infra repository files named on the slide.

## 12. Close — 30 seconds

FoodMind has an implemented, evidenced staging release path: digest-pinned image publication, temporary AWS identity, controlled deployment, runtime checks and retained artifacts. The next hardening work is explicit: make the required merge checks universal and retain proof from a deliberate rollback drill.

Sources: evidence chain on Slide 7; `foodmind-infra/docs/branch-protection-rollout.md`; `foodmind-infra/scripts/cd/deploy-staging.sh`.

## Backup checklist

- Export the final deck to PDF before presenting.
- Pre-open the five GitHub Actions / live-assurance browser tabs.
- Show workflow summaries and artifacts only. Never reveal credential status, tokens, `.env` files, SSM values, or AWS command payloads.
