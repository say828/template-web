output "network_id" {
  description = "Effective network id used by the environment host"
  value       = local.effective_network_id
}

output "subnet_id" {
  description = "Effective subnet id used by the environment host"
  value       = local.effective_subnet_id
}

output "router_id" {
  description = "Created router id when create_router=true"
  value       = length(openstack_networking_router_v2.environment) > 0 ? openstack_networking_router_v2.environment[0].id : ""
}

output "instance" {
  description = "Environment host summary"
  value = {
    id           = openstack_compute_instance_v2.host.id
    name         = openstack_compute_instance_v2.host.name
    fixed_ip     = try(openstack_compute_instance_v2.host.network[0].fixed_ip_v4, "")
    floating_ip  = try(openstack_networking_floatingip_v2.host[0].address, "")
    compose_file = var.compose_file
  }
}
