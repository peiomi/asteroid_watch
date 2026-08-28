output "production_bucket_name" {
  description = "Name of the production storage bucket."
  value       = google_storage_bucket.production.name
}

output "production_bucket_url" {
  description = "gs:// URL of the production bucket."
  value       = "gs://${google_storage_bucket.production.name}"
}

output "app_service_account_email" {
  description = "Email of the application service account."
  value       = google_service_account.app.email
}

output "raw_prefix" {
  value = "projects/_/buckets/${google_storage_bucket.production.name}/objects/raw/"
}

output "errors_prefix" {
  value = "projects/_/buckets/${google_storage_bucket.production.name}/objects/errors/"
}
