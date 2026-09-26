output "dataset_id" {
  value = google_bigquery_dataset.asteroid_data.dataset_id
}

output "dataset_name" {
  value = google_bigquery_dataset.asteroid_data.id
}

output "asteroid_records_table" {
  value = google_bigquery_table.asteroid_records.table_id
}

output "risk_scores_table" {
  value = google_bigquery_table.risk_scores.table_id
}