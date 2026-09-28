output "cloud_run_failure_alert_id" {
  value = google_monitoring_alert_policy.cloud_run_job_failure.id
}

output "cloud_run_failure_alert_name" {
  value = google_monitoring_alert_policy.cloud_run_job_failure.display_name
}