resource "google_cloud_scheduler_job" "etl_schedule" {
  name        = "asteroid_watch_schedule"
  description = "Run asteroid ETL daily"

  schedule  = "0 6 * * *"
  time_zone = "America/Chicago"

  http_target {
    http_method = "POST"

    uri = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${var.job_name}:run"

    oauth_token {
      service_account_email = var.scheduler_sa_email
    }
  }
}

resource "google_cloud_scheduler_job" "recovery_schedule" {
  name = "asteroid_watch_recovery"
  description = "Replay failed batches from Cloud Storage"

  schedule  = "*/30 * * * *"
  time_zone = "America/Chicago"

  http_target {
    http_method = "POST"

    uri = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${var.recovery_job_name}:run"

    oauth_token {
      service_account_email = var.scheduler_sa_email
    }
  }
}