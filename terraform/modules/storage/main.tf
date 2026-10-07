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

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age = 30
    }
  }

  labels = {
    environment = "production"
    team        = "platform"
    managed_by  = "terraform"
  }

  public_access_prevention = "enforced"
}

resource "google_storage_bucket_iam_member" "etl_storage_admin" {
  bucket = google_storage_bucket.production.name
  role = "roles/storage.objectAdmin"
  member = "serviceAccount:${var.etl_sa_email}"
}
