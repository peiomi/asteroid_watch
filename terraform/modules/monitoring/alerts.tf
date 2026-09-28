resource "google_monitoring_alert_policy" "cloud_run_job_failure" {

  display_name = "Asteroid ETL Job Failure"

  combiner = "OR"

  conditions {

    display_name = "Cloud Run Job Failed"

    condition_threshold {

      filter = <<EOT
metric.type="run.googleapis.com/job/completed_task_attempt_count"
resource.type="cloud_run_job"
resource.label."job_name"="${var.job_name}"
metric.label."result"="failed"
resource.label."project_id"="${var.project_id}"
EOT

      comparison      = "COMPARISON_GT"
      threshold_value = 0

      aggregations {
        alignment_period   = "300s"
        per_series_aligner = "ALIGN_SUM"
      }

      duration = "0s"

      trigger {
        count = 1
      }
    }
  }

  enabled = true
}