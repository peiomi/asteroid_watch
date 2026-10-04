# ============================
# Storage
# ============================

output "production_bucket_name" {
  description = "Production bucket name"
  value       = module.storage.bucket_name
}

output "production_bucket_url" {
  description = "Production bucket URL"
  value       = module.storage.bucket_url
}

output "raw_prefix" {
  description = "Raw data storage prefix"
  value       = module.storage.raw_prefix
}

output "errors_prefix" {
  description = "Error storage prefix"
  value       = module.storage.errors_prefix
}

# ============================
# Service Accounts
# ============================

output "etl_sa_email" {
  description = "ETL service account email"
  value       = module.iam.etl_sa_email
}

output "bot_sa_email" {
  description = "Bot service account email"
  value       = module.iam.bot_sa_email
}

output "scheduler_sa_email" {
  description = "Scheduler service account email"
  value       = module.iam.scheduler_sa_email
}

# ============================
# Secrets
# ============================


# ============================
# BigQuery
# ============================

output "dataset_id" {
  description = "BigQuery dataset id"
  value       = module.bigquery.dataset_id
}

output "asteroid_records_table" {
  description = "Asteroid records table"
  value       = module.bigquery.asteroid_records_table
}

output "risk_scores_table" {
  description = "Risk scores table"
  value       = module.bigquery.risk_scores_table
}

# ============================
# Artifact Registry
# ============================

output "artifact_registry_name" {
  description = "Artifact Registry repository name"
  value       = module.artifact_registry.repository_name
}

output "artifact_registry_id" {
  description = "Artifact Registry repository id"
  value       = module.artifact_registry.repository_id
}

output "cloud_run_job_name" {
  value = module.cloud_run.job_name
}

output "cloud_run_job_id" {
  value = module.cloud_run.job_id
}




