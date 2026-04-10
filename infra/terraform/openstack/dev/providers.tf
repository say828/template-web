provider "openstack" {
  auth_url      = var.auth_url
  region        = var.region
  endpoint_type = var.interface
  insecure      = var.insecure

  user_name           = var.auth_type == "password" ? var.username : null
  password            = var.auth_type == "password" ? var.password : null
  tenant_name         = var.auth_type == "password" ? var.project_name : null
  user_domain_name    = var.auth_type == "password" ? var.user_domain_name : null
  project_domain_name = var.auth_type == "password" ? var.project_domain_name : null

  application_credential_id     = var.auth_type == "application_credential" ? var.application_credential_id : null
  application_credential_secret = var.auth_type == "application_credential" ? var.application_credential_secret : null
}
