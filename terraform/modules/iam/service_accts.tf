resource "google_service_account" "etl" {
  account_id   = "etl-sa"
  display_name = "ETL Service Account"
}

resource "google_service_account" "bot" {
  account_id   = "bot-sa"
  display_name = "Bot Service Account"
}

resource "google_service_account" "scheduler" {
  account_id   = "scheduler-sa"
  display_name = "Scheduler Service Account"
}
