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

resource "google_project_iam_member" "etl_bigquery" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.etl.email}"
}

resource "google_project_iam_member" "etl_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.etl.email}"
}

resource "google_project_iam_member" "etl_pubsub" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.etl.email}"
}

resource "google_project_iam_member" "bot_bigquery" {
  project = var.project_id
  role    = "roles/bigquery.dataViewer"
  member  = "serviceAccount:${google_service_account.bot.email}"
}

resource "google_project_iam_member" "bot_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.bot.email}"
}

resource "google_project_iam_member" "bot_pubsub_subscriber" {
  project = var.project_id
  role    = "roles/pubsub.subscriber"
  member  = "serviceAccount:${google_service_account.bot.email}"
}

resource "google_project_iam_member" "scheduler_pubsub" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.scheduler.email}"
}