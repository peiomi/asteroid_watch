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