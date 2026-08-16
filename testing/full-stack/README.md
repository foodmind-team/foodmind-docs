# Real-stack E2E environment

This Compose project runs PostgreSQL, a private MinIO bucket, the Spring Backend, Recommendation, Inference, Cooking, Chat, and the production Web image. It has no public-API interception service. The ML runtime package is built from the checked-out `foodmind-ml` candidate into a test-owned volume.

## Media topology

- Backend S3 API endpoint: `http://minio:9000` on the private Compose network.
- Presigned client endpoint: `http://10.0.2.2:9000` by default.
- Host MinIO binding: port `9000` on all interfaces so the Android emulator bridge can reach it.
- Bucket: `foodmind-e2e-media`, created with no anonymous access.
- CORS: exact `http://127.0.0.1:4173` and `http://localhost:4173` Web origins.
- Upload/read TTL: 5 minutes / 15 minutes.

CI assigns `10.0.2.2/32` to the Linux loopback device. Host Chromium and the Android emulator therefore use the same host in the Backend-generated signature. For a browser-only local run, set `FOODMIND_E2E_MEDIA_PUBLIC_ENDPOINT=http://127.0.0.1:9000`; restore the default before an Android parity run.

## Run locally

Keep all six repositories as siblings of `foodmind-docs`. From `foodmind-docs/testing/full-stack`:

```powershell
docker compose config
docker compose up --build --wait
npm --prefix ../../../foodmind-web run test:e2e:real
docker compose logs --no-color > full-stack.log
docker compose down --volumes --remove-orphans
```

The Web scenario creates a trusted group, uploads a valid PNG through a real presigned PUT, finalises it, attaches it to a group-visible record, and checks:

- Web record detail image `naturalWidth > 0`;
- Web Explore card and preview image `naturalWidth > 0`;
- an unauthorised user cannot retrieve the record or see it in Explore.

The Android real-stack instrumentation then logs into the shared account through `10.0.2.2` and waits for the same Explore image to reach the `LOADED` state.

## Cross-PR CI

The manual `Full real-stack E2E` workflow accepts a Git ref for every repository. Before the four dependent PRs merge, run it with:

- docs, Backend, Web, and Android: `fix/aws-media-upload-viewing`;
- Intelligence and ML: the desired `main` revisions.

The current Backend contract contains 84 operations; both client contract gates must cover all 84 before the real-stack scenario starts.

The workflow builds the selected refs, runs Web no-interception Playwright, compiles and tests Android, starts an API 35 emulator, and archives logs/reports/APKs. No AWS account or credentials are used.

## Ownership and cleanup

All credentials in this Compose file are test-only. MinIO data and the generated model package are named volumes owned by the `foodmind-e2e` project. `docker compose down --volumes --remove-orphans` removes only those test-owned resources. Logs, Playwright traces, screenshots, APKs, and emulator reports are CI artifacts; do not record presigned query strings in long-lived evidence.
