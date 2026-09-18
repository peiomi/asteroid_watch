resource "google_bigquery_dataset" "asteroid_data" {
    dataset_id = "asteroid_data"
    location = "US"

    description = "NASA NEO analytics dataset"
}