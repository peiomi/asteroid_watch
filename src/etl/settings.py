class Settings:
    PROJECT_ID = "asteroid-watch-506918"
    DATASET_ID = "asteroid_watch"
    BUCKET_NAME = f"{PROJECT_ID}-production-data"
    ASTEROID_TABLE = f"{PROJECT_ID}.{DATASET_ID}.asteroid_records"
    RISK_TABLE = f"{PROJECT_ID}.{DATASET_ID}.risk_scores"
