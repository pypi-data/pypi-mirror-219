# Configure the Hetzner Cloud Provider
provider "hcloud" {
  token = var.hetzner_api_key
}
