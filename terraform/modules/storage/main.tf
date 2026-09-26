# ============================
# Storage Bucket Definition
# ============================

resource "google_storage_bucket" "production" {
  name          = "${var.project_id}-production-data"
  location      = var.region
  storage_class = "STANDARD"
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  soft_delete_policy {
    retention_duration_seconds = 604800 # 7 days
  }

  labels = {
    environment = "production"
    team        = "platform"
    managed_by  = "terraform"
  }

  public_access_prevention = "enforced"
}

# Write only to raw/
resource "google_storage_bucket_iam_member" "raw_writer" {
  bucket = google_storage_bucket.production.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${var.etl_sa_email}"

  condition {
    title      = "raw-only"
    expression = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.production.name}/objects/raw/')"
  }
}

# Write only to errors/
resource "google_storage_bucket_iam_member" "error_writer" {
  bucket = google_storage_bucket.production.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${var.etl_sa_email}"

  condition {
    title      = "errors-only"
    expression = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.production.name}/objects/errors/')"
  }
}
