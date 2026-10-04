variable "nasa_api_key" {
  description = "NASA API key"
  type        = string
  sensitive   = true
}

variable "discord_bot_token" {
  description = "token for discord bot"
  type        = string
  sensitive   = true
}

variable "bluesky_password" {
  description = "password for asteroid-watch BlueSky account"
  type        = string
  sensitive   = true
}