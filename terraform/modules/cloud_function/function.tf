data "archive_file" "cloud_function" {
  type        = "zip"
  source_dir  = "${path.root}/../cloud_function"
  output_path = "${path.root}/../cloud_function.zip"
}

resource "google_storage_bucket_object" "function_zip" {

  name   = "cloud_function.zip"

  bucket = "${var.project_id}-production-data"

  source = data.archive_file.cloud_function.output_path
}

resource "google_cloudfunctions2_function" "etl_event_handler" {

  name     = "etl-event-handler"
  location = var.region

  build_config {

    runtime     = "python312"
    entry_point = "etl_event"

    source {

      storage_source {
        bucket = "${var.project_id}-production-data"
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {

    max_instance_count = 1

    available_memory = "256M"

    timeout_seconds = 60

    service_account_email = var.service_account_email
  }

  event_trigger {

    trigger_region = var.region

    event_type = "google.cloud.pubsub.topic.v1.messagePublished"

    pubsub_topic = "projects/${var.project_id}/topics/${var.topic_name}"

    retry_policy = "RETRY_POLICY_RETRY"
  }
}