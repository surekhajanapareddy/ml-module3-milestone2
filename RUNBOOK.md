# RUNBOOK — ML API Deployment System

This document provides operational, deployment, and maintenance instructions for the ML API production system.

---

# 1. Dependency Pinning Strategy

All Python dependencies are pinned to exact versions in requirements.txt.

Example:
```
fastapi==0.129.0
scikit-learn==1.8.0
```

Reason:
Ensures reproducible builds across environments and prevents unexpected failures due to upstream package updates.

---

# 2. Docker Image Optimization

Techniques used:

• Multi-stage build  
• Slim Python base image  
• No cache pip install  
• Only runtime files copied  

Benefits:

| Metric | Before | After |
|------|-------|------|
Image Size | ~1.2GB | <250MB |
Startup Time | Slow | Fast |
Security | Large attack surface | Minimal |

---

# 3. Security Considerations

Implemented security best practices:

• Secrets stored in GitHub Secrets  
• No credentials in repository  
• Container runs as non-root user  
• Minimal base image reduces vulnerabilities  
• Artifact Registry access controlled via IAM  

---

# 4. CI/CD Workflow Explanation

Pipeline Stages:

Build Stage
• Build Docker image
• Push to Artifact Registry

Dev Stage
• Deploy to DEV service
• Run API tests

Release Stage (Tag Triggered)
• Deploy TEST → run tests
• Deploy STAGING → run tests
• Manual approval gate
• Deploy PROD → run tests

Failure Handling
If any test fails → pipeline stops → no promotion.

---

# 5. Versioning Strategy

Semantic Versioning format:

vMAJOR.MINOR.PATCH

Example:
v1.2.3

Meaning:

MAJOR → breaking change  
MINOR → feature addition  
PATCH → bug fix  

Tags trigger release pipeline automatically.


---

# 6. Rollback Strategy

If production deployment fails:

List revisions
```
gcloud run revisions list --service ml-api-prod --region us-central1
```

Route traffic back
```
gcloud run services update-traffic ml-api-prod --to-revisions=<REVISION>=100 --region us-central1
```

Rollback is instant and zero-downtime.

---

# 7. Operational Commands

List services
```
gcloud run services list
```

Check logs
```
gcloud run services logs read ml-api-prod
```

Describe service
```
gcloud run services describe ml-api-prod
```

---

# 8. Troubleshooting Guide

Issue: Cloud Run cannot pull image  
Cause: missing permission  
Fix:
Grant Artifact Registry Reader role to Cloud Run service account.

---

Issue: Tests fail in pipeline  
Cause: dependency mismatch  
Fix:
Update requirements.txt and rebuild image.

---

Issue: Deployment stuck  
Cause: incorrect image path  
Fix:
Verify registry URL matches pushed image.

---

# 9. Deployment Architecture Philosophy

This pipeline follows industry-standard progressive delivery:

DEV → TEST → STG → PROD

Benefits:

• Early bug detection  
• Safer releases  
• No broken production deployments  
• Controlled promotion  

---

# 10. System Design Principles Used

Reproducibility  
Automation  
Security  
Observability  
Rollback-Ready Architecture  

---

# 11. Container Security Hardening

The container is configured to run as a non-root user to minimize security risks.

A dedicated user is created during build:
```
RUN useradd -m appuser
USER appuser
```
Running containers as non-root prevents privilege escalation and reduces the attack surface if the container is compromised.

---

# Manual Approval Gate for Production

The CI/CD pipeline implements an approval gate before deploying to production.
Implementation:

```
deploy-prod:
  environment: production
```
Production deployments are protected by a manual approval gate to ensure release safety and controlled rollouts.

---

# Maintainer Notes

Always deploy using version tags.  
Never deploy directly to production.  
Always validate API health before promotion.
