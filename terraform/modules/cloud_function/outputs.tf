output "function_name" {
  value = google_cloudfunctions2_function.etl_event_handler.name
}

output "function_uri" {
  value = google_cloudfunctions2_function.etl_event_handler.url
}