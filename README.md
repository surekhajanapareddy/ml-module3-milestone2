# ML API Deployment Pipeline — Milestone 2

[![CI Status](https://github.com/surekhajanapareddy/ml-module3-milestone2/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/surekhajanapareddy/ml-module3-milestone2/actions/workflows/build.yml)

---

## Project Overview
This project demonstrates a production-grade MLOps CI/CD pipeline that automatically builds, tests, versions, and deploys a machine learning API across multiple environments using Docker, GitHub Actions, and Google Cloud Run.

It implements a real DevOps release lifecycle:

DEV → TEST → STAGING → PRODUCTION

---

## Architecture Flow

Developer Push → GitHub Actions → Build → Push Image → Deploy → Test → Promote

---

## Environments

| Environment | Cloud Run Service | Trigger |
|------------|-------------------|--------|
DEV | ml-api-dev | push to main |
TEST | ml-api-test | version tag |
STAGING | ml-api-stg | after TEST passes |
PRODUCTION | ml-api-prod | manual approval |

---

## CI/CD Pipeline Logic

### On Push to main
    1. Run API tests
    2. Build Docker image
    3. Push image to Artifact Registry
    4. Deploy to DEV
    5. Test deployed API

---

### On Version Tag (vX.Y.Z)
    1. Deploy same build to TEST
    2. Test API
    3. Deploy to STAGING
    4. Test API
    5. Manual approval
    6. Deploy to PRODUCTION
    7. Final API test

---

## Container Registry

Images are tagged using both semantic versioning (vX.Y.Z) and commit SHA to ensure traceability, reproducibility, and safe rollbacks. Images are stored using a student-specific namespace dynamically to prevent collisions and ensure traceability.

Images are stored in Google Artifact Registry:

```
us-central1-docker.pkg.dev/mlops-module3-milestone2-sj/ml-api/ml-api-surekhajanapareddy:<tag>
```

---

## Quick Start — Local Run

Clone repo
```
git clone https://github.com/surekhajanapareddy/ml-module3-milestone2.git
cd ml-module3-milestone2
```

Build image
```
docker build -t ml-api .
```

Run container
```
docker run -p 8000:8000 ml-api
```

Test API
```
http://localhost:8000/docs
```

Pull image from Artifact Registry
```
docker pull us-central1-docker.pkg.dev/mlops-module3-milestone2-sj/ml-api/ml-api-surekhajanapareddy:v2.0.1
```

Run container
```
docker run -p 8000:8000 us-central1-docker.pkg.dev/mlops-module3-milestone2-sj/ml-api/ml-api-surekhajanapareddy:v2.0.1
```

---

## Project Status

Pipeline Status → Fully Automated  
Deployment → Multi-Environment Progressive Delivery  
Testing → Automated Post-Deployment Validation  

---

## Final API endpoints per environment

```
DEV: https://ml-api-dev-827099598475.us-central1.run.app/docs
TEST: https://ml-api-test-240926533780.us-central1.run.app/docs
STG: https://ml-api-stg-240926533780.us-central1.run.app/docs
PROD: https://ml-api-prod-240926533780.us-central1.run.app/docs
```

---

## Documentation

For operational and engineering details see:

**RUNBOOK.md**

---


