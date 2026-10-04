resource "google_pubsub_topic" "etl_events" {
  name = "etl-events"
}

resource "google_pubsub_subscription" "etl_events_sub" {
  name  = "etl-events-sub"
  topic = google_pubsub_topic.etl_events.name
}