output "bucket_name" {
  description = "production bucket name"
  value       = google_storage_bucket.production.name
}

output "bucket_url" {
  description = "bucket gs:// URL"
  value       = "gs://${google_storage_bucket.production.name}"
}

output "raw_prefix" {
  value = "projects/_/buckets/${google_storage_bucket.production.name}/objects/raw/"
}

output "errors_prefix" {
  value = "projects/_/buckets/${google_storage_bucket.production.name}/objects/errors/"
}