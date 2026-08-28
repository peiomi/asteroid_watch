terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Production bucket with versioning, encryption, and access controls
resource "google_storage_bucket" "production" {
  name          = "${var.project_id}-production-data"
  location      = var.region
  storage_class = "STANDARD"
  force_destroy = false

  # Enable uniform bucket-level access
  # This disables ACLs and uses IAM exclusively
  uniform_bucket_level_access = true

  # Enable object versioning to protect against accidental deletes
  versioning {
    enabled = true
  }

  # Encryption with a customer-managed key
  # encryption {
  #   default_kms_key_name = google_kms_crypto_key.bucket_key.id
  # }

  # Soft delete policy - retain deleted objects for 7 days
  soft_delete_policy {
    retention_duration_seconds = 604800  # 7 days
  }

  # Labels for cost tracking and organization
  labels = {
    environment = "production"
    team        = "platform"
    managed_by  = "terraform"
  }

  # Public access prevention
  public_access_prevention = "enforced"
}

# IAM ROLES 

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

# Write only to raw/
resource "google_storage_bucket_iam_member" "raw_writer" {
  bucket = google_storage_bucket.production.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.etl.email}"

  condition {
    title      = "raw-only"
    expression = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.production.name}/objects/raw/')"
  }
}

# Write only to errors/
resource "google_storage_bucket_iam_member" "error_writer" {
  bucket = google_storage_bucket.production.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.etl.email}"

  condition {
    title      = "errors-only"
    expression = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.production.name}/objects/errors/')"
  }
}
