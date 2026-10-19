resource "google_cloud_run_v2_service" "discord_bot" {
  name     = "asteroid-watch-discord"
  location = var.region

  template {
    service_account = google_service_account.cloud_run_sa.email

    containers {
      image = var.discord_image

      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "DISCORD_TOKEN"
        value_source {
          secret_key_ref {
            secret  = "discord-token"
            version = "latest"
          }
        }
      }
    }
  }
}

resource "google_cloud_run_service_iam_member" "public" {
  location = google_cloud_run_v2_service.discord_bot.location
  name     = google_cloud_run_v2_service.discord_bot.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}