# Asteroid Watch

Asteroid Watch is a cloud/data engineering project that turns NASA's Near Earth Object data into a fully automated ETL (Extract, Transform, Load) pipeline running on Google Cloud.

The project is designed to demonstrate how I approach a full ETL cloud pipeline project: fetching external data, storing the raw data, turning it into analytics-friendly records, and preparing secure cloud infrastructure for scheduled execution.

> **Project status:** Active development. The ETL pipeline is deployed and successfully running on Google Cloud Run Jobs. The Terraform code successfully configured the cloud infrastructure. NASA asteroid data is being successfully ingested and archived in Cloud Storage, normalized, and written to BigQuery. Pub/Sub is successfully sending updates. The Bluesky account and discord bot have been created and integrated into the codebase, still need to test connection. Risk scoring still needs improvement and I want to add some sort of data visualization before deployment.

## What This Project Demonstrates

- Python service boundaries for API clients, normalization, storage, scoring, and warehouse writes
- Integration with the NASA Near Earth Object Feed API
- Google Cloud Secret Manager usage for credential management
- Terraform-managed Google Cloud infrastructure
- IAM separation for ETL, bot, and scheduler service accounts
- Automated test entry point using Python's `unittest`

## Architecture

```text
Cloud Scheduler
	|
	v
Cloud Run Job
	|
	v
	ETL Pipeline
		|
		+--> Secret Manager
		+--> NASA NEO API
		+--> raw JSON in Cloud Storage
		+--> normalized asteroid records
		+--> risk scoring
		+--> BigQuery analytics table
		+--> Pub/Sub events
		+--> hazard alerts / bot integrations
```

The current Python pipeline is organized around small components:

| Component         | Responsibility                                            |
| ----------------- | --------------------------------------------------------- |
| `NasaClient`      | Fetches NEO data with a timeout and HTTP error handling   |
| `SecretsManager`  | Retrieves credentials from Google Cloud Secret Manager    |
| `CloudStorage`    | Persists raw JSON payloads for replay and troubleshooting |
| `Normalizer`      | Maps NASA's nested response into normalized records       |
| `RiskScorer`      | Generates asteroid risk classifications                   |
| `BigQueryWriter`  | Persists processed records to Bigquery                    |
| `PubSubPublisher` | Publishes ETL status and event notifications              |
| `ETLPipeline`     | Runs the full pipeline workflow                           |
| Terraform         | Configures the Google Cloud infrastructure                |

## Data Models

### Asteroid Record

The normalized record is intended to include:

- Asteroid name
- ID
- Min estimated diameter (km)
- Max estimated diameter (km)
- Close-approach miss distance (km)
- Relative velocity (km/s)
- NASA's potentially hazardous classification
- Close-approach date
- `processed_at` timestamp

### Risk Score Record

Each scored record contains:

- Asteroid ID
- Name
- Size classification
- Velocity classification
- Distance classification
- Numerical risk score out of 100
- Risk level
- `processed_at` timestamp

## Tools

- Python
- `requests`
- GCP
- BigQuery
- Terraform
- `unittest`

## Run Tests

From the repository root:

```bash
./test.sh
```

## Planned Improvements

1. Refine risk-scoring calculations. I need to research what astronomy professionals actually consider 'fast', 'slow', 'big', 'small' or what is considered 'far' or 'close' in terms of asteroids.
2. Code is written for BlueSky/Discord bot integration but hasn't been tested.
3. Add some data visualization with Jupyter
4. Add scheduler-triggered execution and deployment automation.
5. Add a small analytics API and hazard-alert bot backed by the warehouse.

## Why I Built It

I built Asteroid Watch to practice the parts of cloud and data engineering that matter beyond a single script: reliable ingestion, recoverable raw data, secure secret handling, infrastructure as code, efficient data storage, and automated testing.

[>> Asteroid Watch BlueSky Account <<](https://bsky.app/profile/asteroid-watch.bsky.social)
