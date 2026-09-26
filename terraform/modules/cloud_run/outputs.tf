ouput "service_name" {
  value = google_cloud_run_v2_service.etl.name
}

output "service_uri" {
  value = google_cloud_run_v2_service.etl.service_uri
}