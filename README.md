![CI Status](https://github.com/surekhajanapareddy/ml-module3-milestone2/actions/workflows/build.yml/badge.svg) 

# Project Overview

This project demonstrates a production-grade MLOps CI/CD pipeline that automatically builds, tests, versions, and deploys a machine learning API across multiple environments using:

    Docker
    Google Cloud Run
    Google Artifact Registry
    GitHub Actions CI/CD

The system follows a real-world promotion pipeline:

``` bash
DEV → TEST → STAGING → PRODUCTION
```
# Architecture

    Developer Push / Tag
            ↓
    GitHub Actions CI/CD
            ↓
    Build Docker Image
            ↓
    Push → Artifact Registry
            ↓
    Deploy → Cloud Run (DEV)
            ↓
    API Test
            ↓
    Deploy → TEST
            ↓
    API Test
            ↓
    Deploy → STAGING
            ↓
    API Test
            ↓
    Manual Approval
            ↓
    Deploy → PRODUCTION
            ↓
    Final API Test

# Environments

| Environment | Service Name | Trigger           |
| ----------- | ------------ | ----------------- |
| DEV         | ml-api-dev   | push to main      |
| TEST        | ml-api-test  | version tag       |
| STG         | ml-api-stg   | after TEST passes |
| PROD        | ml-api-prod  | after approval    |

# CI/CD Pipeline Logic (Implemented Flow)

On push to main branch

``` bash
Test API → Build → Deploy DEV → Test API
```
On tag push (vX.Y.Z)

``` bash
Build (same image)
      ↓
Deploy TEST → Test
      ↓
Deploy STG → Test
      ↓
Manual Approval
      ↓
Deploy PROD → Test
```
If any test fails → pipeline stops automatically.

# Container Registry Integration

Container Registry Integration

## Registry URL

``` bash 
us-central1-docker.pkg.dev/mlops-module3-milestone2-sj/ml-api/ml-api
```

## Image tag format:

``` bash
<commit-sha>
```

## Example

``` bash 
us-central1-docker.pkg.dev/mlops-module3-milestone2-sj/ml-api/ml-api:92cf967e4648f0ea67e707ba67dad0043781c345
```

# Automated Testing Strategy

Tests run:

    before build
    after every deployment

Health check endpoint used:

``` bash
GET /health
```

Example validation command:

``` bash
https://ml-api-dev-827099598475.us-central1.run.app/health
```
Pipeline fails if response ≠ 200.

# Versioning Strategy

Semantic versioning is used:

``` bash
vMAJOR.MINOR.PATCH
```

Example:

``` bash
v1.0.2
```
Tags trigger release pipeline.

# Secrets Used

Stored securely in GitHub Actions Secrets:

| Secret         | Purpose                     |
| -------------- | --------------------------- |
| GCP_PROJECT_ID | GCP Project                 |
| GCP_SA_KEY     | Service account credentials |

# Deployment Platform

All services are deployed to:
    Google Cloud Run

Features used:
    serverless container hosting
    auto scaling
    HTTPS endpoints
    IAM access control

# Running Locally

## Clone repo:

``` bash 
git clone https://github.com/surekhajanapareddy/ml-module3-milestone2
cd repo
```

## Build image:

``` bash 
docker build -t ml-api .
```

## Run container:

``` bash
docker run -p 8000:8000 ml-api
```

## Test locally:

``` bash
http://localhost:8000/docs
```

# Reproducibility Guarantee

Anyone can reproduce deployment in under 5 minutes:

``` bash
git clone repo
docker build .
```
No manual environment setup required.

# Production-Grade Features Implemented

    ✔ Multi-environment promotion pipeline
    ✔ Immutable container builds
    ✔ Artifact reuse across stages
    ✔ Automated testing gates
    ✔ Manual approval for production
    ✔ Secure secret handling
    ✔ Semantic version releases
    ✔ Infrastructure-independent deployment
    ✔ Rollback capability

# Evidence

Include screenshots of:
    successful pipeline run
    artifact registry images
    cloud run services
    version tag deployment

# Learning Outcomes Demonstrated

This project demonstrates real-world MLOps capabilities:
    CI/CD pipeline design
    cloud deployment
    containerization
    environment promotion strategy
    automated validation
    release management
    production readiness

# Final Status

    Pipeline Status: ✅ Fully Working
    Deployment: ✅ Multi-Environment
    Testing: ✅ Automated
    Release Flow: ✅ Version-Controlled