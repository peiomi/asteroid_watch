resource "google_bigquery_table" "asteroid_records" {
  dataset_id = google_bigquery_dataset.asteroid_data.dataset_id
  table_id   = "asteroid_records"

  deletion_protection = false

  time_partitioning {
    type = "DAY"
    field = "processed_at"
    expiration_ms = 604800000
  }

  schema = jsonencode([
    {
      name = "id"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "name"
      type = "STRING"
    },
    {
      name = "diameter_min"
      type = "FLOAT"
    },
    {
      name = "diameter_max"
      type = "FLOAT"
    },
    {
      name = "miss_distance_km"
      type = "FLOAT"
    },
    {
      name = "relative_velocity_km_s"
      type = "FLOAT"
    },
    {
      name = "is_hazardous"
      type = "BOOL"
    },
    {
      name = "close_approach_date"
      type = "DATE"
    },
    {
      name = "processed_at"
      type = "TIMESTAMP"
    }
  ])
}

resource "google_bigquery_table" "risk_scores" {
  dataset_id = google_bigquery_dataset.asteroid_data.dataset_id
  table_id   = "risk_scores"

  deletion_protection = false

  time_partitioning {
    type = "DAY"
    field = "processed_at"
    expiration_ms = 604800000
  }

  schema = jsonencode([
    {
      name = "id"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "name"
      type = "STRING"
    },
    {
      name = "size"
      type = "STRING"
    },
    {
      name = "speed"
      type = "STRING"
    },
    {
      name = "distance"
      type = "STRING"
    },
    {
      name = "risk_score"
      type = "INTEGER"
    },
    {
      name = "risk_level"
      type = "STRING"
    },
    {
      name = "processed_at"
      type = "TIMESTAMP"
    }
  ])
}