FoodMind local deployment overview
==================================

Purpose
-------
This guide starts FoodMind on one workstation when the public demonstration
site is unavailable or a local end-to-end environment is needed. The preferred
route is one Docker Compose stack from foodmind-infra, followed by separately
started Web and Android clients.

Repository responsibilities
---------------------------

  foodmind-infra          Local integration and release configuration
  foodmind-backend        Public API, authentication, domain rules, database
  foodmind-intelligence   Private chat, cooking, recommendation, inference
  foodmind-ml             Offline model package source and validation
  foodmind-web            Browser client; calls Backend /api/v1 only
  foodmind-android        Native client; calls Backend /api/v1 only
  foodmind-docs           Architecture, operations, contracts, evidence

  Web / Android
       |
       v
  Backend :8080 ---- PostgreSQL :15432, MinIO :9000/:9001
       |
       +---- private Intelligence services and ML model-package job

Do not configure either client with a database, MinIO, Agent, or Inference URL.

Prerequisites
-------------

- Docker Desktop (or Docker Engine) with Docker Compose
- Git and PowerShell
- Node.js 24.16.x with npm for Web
- Android Studio, JDK 17, and Android SDK for Android
- Optional: Python 3.13 and uv for standalone ML/Intelligence development

1. Start the integrated local backend stack
-------------------------------------------

    git clone --recurse-submodules https://github.com/foodmind-team/foodmind-infra.git
    Set-Location foodmind-infra
    git submodule update --init --recursive
    Copy-Item .env.example .env
    docker compose config --quiet
    docker compose up --build -d --wait
    Invoke-RestMethod http://localhost:8080/actuator/health/readiness
    docker compose ps

The expected readiness result is UP. Default host addresses are:

    Backend API            http://localhost:8080/api/v1
    Backend readiness      http://localhost:8080/actuator/health/readiness
    PostgreSQL             localhost:15432
    MinIO API              http://localhost:9000
    MinIO console          http://localhost:9001

The default .env uses deterministic AI fallbacks. Put a real optional provider
key only in the ignored .env file; never commit it. If a host port is busy,
change its public port value in .env and rerun the Compose commands.

2. Start Web separately
-----------------------

Open another PowerShell window after Backend readiness is UP:

    git clone https://github.com/foodmind-team/foodmind-web.git
    Set-Location foodmind-web
    Copy-Item .env.example .env.local
    # Keep FOODMIND_BACKEND_ORIGIN=http://localhost:8080
    npm ci
    npm run dev

Open the Vite URL, normally http://localhost:5173. The development proxy sends
same-origin /api/v1 requests to Backend. If 5173 is occupied, use
`npm run dev -- --port <unused-port>` and allow that exact origin in a
Backend-only local setup.

3. Start Android separately
---------------------------

With the Infra Backend running, start the Android project in Android Studio or
build a debug APK for an emulator:

    git clone https://github.com/foodmind-team/foodmind-android.git
    Set-Location foodmind-android
    .\gradlew.bat --no-daemon assembleDebug `
      -Pfoodmind.debugApiBaseUrl=http://10.0.2.2:8080/api/v1/

For a USB-connected physical device, forward the port first and use the device
loopback address:

    adb reverse tcp:8080 tcp:8080
    .\gradlew.bat --no-daemon assembleDebug `
      -Pfoodmind.debugApiBaseUrl=http://127.0.0.1:8080/api/v1/

The API base URL must end in /api/v1/. Do not use 10.0.2.2 on a physical device.

Verification and troubleshooting
--------------------------------

- `docker compose ps` should show the health-gated runtime ready.
- `docker compose logs -f backend postgres inference recommendation cooking chatbot`
  shows startup failures.
- `docker compose down` stops the stack but retains development data.
- `docker compose down --volumes` deletes local database, MinIO, and model
  package volumes. Use it only when this data loss is intended.
- Do not expose private runtime service ports to a browser or mobile client.

Cloud service fallback
----------------------

The public demonstration URL is https://13.229.2.154.sslip.io/. If it is
unavailable, a cloud-account balance or billing issue is one possible cause,
not a confirmed diagnosis. Check the deployment/account status through the
project owner. For development or demonstration continuity, deploy the local
Infra stack above, then start Web and/or Android separately against the local
Backend instead of waiting for the cloud environment.
