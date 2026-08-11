# Real-stack E2E environment

This Compose project builds and runs PostgreSQL, the Spring backend, Recommendation, Inference, Cooking, Chat, and the production Web image. It contains no public-API interception service and uses only explicit test credentials. The ML runtime package is built from the checked-out `foodmind-ml` candidate artifact into a test-owned volume.

From `foodmind-docs/testing/full-stack`:

```powershell
docker compose up --build --wait
npm --prefix ../../../foodmind-web run test:e2e:real
docker compose logs --no-color > full-stack.log
docker compose down --volumes --remove-orphans
```

Set Android debug API access to the emulator host bridge (the project default), install `foodmind-android/app/build/outputs/apk/debug/app-debug.apk`, and execute the same account/capability scenario. `docker compose down --volumes --remove-orphans` removes only resources labeled under the `foodmind-e2e` project.

The release scenario must verify one caller-provided `X-Request-ID` in backend and intelligence logs for recommendation, cooking, and chat calls, plus explicit timeout/unavailable UI states. Logs, Playwright traces, screenshots, APK, and emulator screenshots are CI artifacts.
