output "secret_id" {
  description = "NASA API secret ID"
  value       = google_secret_manager_secret.nasa_api_key.id
}

output "secret_name" {
  description = "NASA API secret name"
  value       = google_secret_manager_secret.nasa_api_key.secret_id
}