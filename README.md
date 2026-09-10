# Asteroid Watch

Asteroid Watch is a cloud/data engineering project that turns NASA's Near Earth Object data into a repeatable ingestion and risk-analysis pipeline.

The project is designed to demonstrate how I approach an end-to-end data platform: fetching external data, storing the raw data, turning it into analytics-friendly records, and preparing secure cloud infrastructure for scheduled execution.

> **Project status:** Active development. The ingestion and infrastructure foundations are in place; risk scoring, BigQuery persistence, alerting, and production deployment are the next implementation steps.

## What This Project Demonstrates

- Python service boundaries for API clients, normalization, storage, scoring, and warehouse writes
- Integration with the NASA Near Earth Object Feed API
- Google Cloud Secret Manager usage for API credentials
- Terraform-managed Google Cloud infrastructure
- IAM separation for ETL, bot, and scheduler service accounts
- Least-privilege Cloud Storage permissions for `raw/` and `errors/` object paths
- Automated test entry point using Python's `unittest` framework

## Architecture

```text
Cloud Scheduler
	|
	v
ETL service --> NASA NEO API
	|
	+--> raw JSON in Cloud Storage
	+--> normalized asteroid records
	+--> risk scoring
	+--> BigQuery analytics table
	|
	+--> future hazard alerts / bot integrations
```

The current Python pipeline is organized around small components:

| Component        | Responsibility                                                     |
| ---------------- | ------------------------------------------------------------------ |
| `NasaClient`     | Fetches NEO data with a timeout and HTTP error handling            |
| `SecretsManager` | Reads the NASA API key from Google Cloud Secret Manager            |
| `CloudStorage`   | Persists raw JSON payloads for replay and troubleshooting          |
| `Normalizer`     | Maps NASA's nested response into analytics-oriented fields         |
| `RiskScorer`     | Domain boundary for deriving an asteroid risk score                |
| `BigQueryWriter` | Persistence boundary for scored records                            |
| Terraform        | Defines storage, IAM, secrets, scheduling, and supporting services |

## Data Model

The normalized record is intended to include:

- Asteroid ID and name
- Estimated diameter range in kilometers
- Close-approach miss distance in kilometers
- Relative velocity in kilometers per second
- NASA's potentially hazardous classification
- Close-approach date
- Derived risk score

## Tools

- Python
- `requests`
- GCP
- BigQuery
- Terraform
- `unittest`

## Repository Layout

```text
src/etl/                 Pipeline and integration components
tests/                   Unit tests for ETL building blocks
terraform/               Root infrastructure configuration and modules
project_plan.py          Initial design notes and future work
requirements.txt         Python dependencies
test.sh                  Test entry point
```

## Run Tests

From the repository root:

```bash
./test.sh
```

The test suite is intentionally kept separate from cloud deployment. Tests that exercise external services require valid Google Cloud credentials and project configuration.

## Local Configuration

The application expects:

- `GCP_PROJECT` set to the Google Cloud project ID
- Application Default Credentials configured for Secret Manager access
- A Secret Manager secret named `nasa_api_key`

## Planned Improvements

1. Complete the risk-scoring model and add tests for boundary conditions.
2. Implement typed normalized models and BigQuery schema management.
3. Add retries, structured logging, and explicit error-object persistence.
4. Add scheduler-triggered execution and deployment automation.
5. Add monitoring for latency, failures, and pipeline freshness.
6. Add a small analytics API and hazard-alert bot backed by the warehouse.

## Why I Built It

I built Asteroid Watch to practice the parts of cloud and data engineering that matter beyond a single script: reliable ingestion, recoverable raw data, secure secret handling, infrastructure as code, efficient data storage, and unittesting.
