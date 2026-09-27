terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "artifact_registry" {
  source = "./modules/artifact_registry"

  region        = var.region
  repository_id = "asteroid-watch"
  description   = "Docker images for Asteroid Watch"
}

module "storage" {
  source = "./modules/storage"

  project_id   = var.project_id
  region       = var.region
  etl_sa_email = module.iam.etl_sa_email
}

module "iam" {
  source = "./modules/iam"

  project_id = var.project_id
}

module "secrets" {
  source = "./modules/secrets"

  nasa_api_key = var.nasa_api_key
}

module "bigquery" {
  source = "./modules/bigquery"

  dataset_id = "asteroid_data"
  location   = "US"
}

module "cloud_run" {
  source = "./modules/cloud_run"

  region = var.region

  service_account_email = module.iam.etl_sa_email

  container_image = "us-central1-docker.pkg.dev/asteroid-watch-506918/asteroid-watch/asteroid-watch:latest"
}

module "scheduler" {
  source = "./modules/scheduler"

  project_id = var.project_id
  region = var.region
  job_name = module.cloud_run.job_name
  scheduler_sa_email = module.iam.scheduler_sa_email
}

module "pubsub" {
  source = "./modules/pubsub"
}