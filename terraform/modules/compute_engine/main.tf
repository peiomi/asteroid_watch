resource "google_compute_instance" "discord_bot" {
  name         = "asteroid-watch-discord"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
    }
  }

  network_interface {
    network = "default"

    access_config {}
  }

  service_account {
    email  = var.discord_sa_email
    scopes = ["cloud-platform"]
  }

  metadata_startup_script = file("${path.module}/startup.sh")
}