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

resource "google_secret_manager_secret" "discord_bot_token" {
  secret_id = "discord_bot_token"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "discord_bot_token_version" {
  secret      = google_secret_manager_secret.discord_bot_token.id
  secret_data = var.discord_bot_token
}

resource "google_secret_manager_secret" "bluesky_password" {
  secret_id = "bluesky_password"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "bluesky_password_version" {
  secret      = google_secret_manager_secret.bluesky_password.id
  secret_data = var.bluesky_password
}
