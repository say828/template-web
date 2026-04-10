module "environment_host" {
  source = "../modules/environment_host"

  availability_zone      = var.availability_zone
  create_network         = var.create_network
  network_name           = var.network_name
  subnet_name            = var.subnet_name
  subnet_cidr            = var.subnet_cidr
  create_router          = var.create_router
  router_name            = var.router_name
  external_network_id    = var.external_network_id
  network_id             = var.network_id
  subnet_id              = var.subnet_id
  service_allowed_cidrs  = var.service_allowed_cidrs
  ssh_allowed_cidrs      = var.ssh_allowed_cidrs
  name                   = var.name
  image_name             = var.image_name
  flavor_name            = var.flavor_name
  keypair_name           = var.keypair_name
  assign_floating_ip     = var.assign_floating_ip
  floating_ip_pool       = var.floating_ip_pool
  exposed_tcp_ports      = var.exposed_tcp_ports
  repo_clone_url         = var.repo_clone_url
  repo_ref               = var.repo_ref
  compose_file           = "infra/compose/prod.yml"
  compose_env_filename   = ".env.prod"
  compose_env_content    = var.compose_env_content
  deploy_compose_on_boot = var.deploy_compose_on_boot
}

output "network_id" {
  description = "Effective network id used by the PROD host"
  value       = module.environment_host.network_id
}

output "subnet_id" {
  description = "Effective subnet id used by the PROD host"
  value       = module.environment_host.subnet_id
}

output "router_id" {
  description = "Created router id when create_router=true"
  value       = module.environment_host.router_id
}

output "instance" {
  description = "PROD host summary"
  value       = module.environment_host.instance
}
