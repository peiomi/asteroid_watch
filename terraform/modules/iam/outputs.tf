output "etl_sa_email" {
  value = google_service_account.etl.email
}

output "bot_sa_email" {
  value = google_service_account.bot.email
}

output "scheduler_sa_email" {
  value = google_service_account.scheduler.email
}