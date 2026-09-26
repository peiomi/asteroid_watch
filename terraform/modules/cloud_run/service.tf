resource "google_cloud_run_v2_service" "etl" {
  name     = "asteroid-watch-etl"
  location = var.region

  template {
    service_account = var.service_account_email

    containers {
      image = var.container_image
    }
  }
}