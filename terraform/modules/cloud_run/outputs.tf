output "job_name" {
  value = google_cloud_run_v2_job.etl.name
}

output "job_id" {
  value = google_cloud_run_v2_job.etl.id
}

output "recovery_job_name" {
value = google_cloud_run_v2_job.recovery.name
}