resource "google_bigquery_dataset" "asteroid_data" {
  dataset_id = var.dataset_id
  location   = var.location

  description = "NASA NEO analytics dataset"
}