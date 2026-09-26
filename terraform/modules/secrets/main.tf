resource "google_secret_manager_secret" "nasa_api_key" {
  secret_id = "nasa_api_key"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "nasa_api_key_version" {
  secret      = google_secret_manager_secret.nasa_api_key.id
  secret_data = var.nasa_api_key
}
