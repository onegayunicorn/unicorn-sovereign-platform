# Cloud provisioning — IBM / AWS / GCP. Multi-cloud with sovereign defaults.
terraform {
  required_version = ">= 1.6"
}

variable "cloud_provider" {
  type    = string
  default = "aws"
  validation {
    condition     = contains(["aws", "gcp", "ibm"], var.cloud_provider)
    error_message = "Cloud provider must be aws, gcp, or ibm."
  }
}

variable "region" {
  type    = string
  default = "ap-southeast-2"
}

# Placeholder modules — actual resources defined per provider in modules/
output "selected_provider" {
  value = var.cloud_provider
}

output "region" {
  value = var.region
}
