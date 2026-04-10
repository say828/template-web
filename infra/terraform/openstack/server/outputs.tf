output "backend_instance_id" {
  value       = openstack_compute_instance_v2.backend.id
  description = "Server compute instance id."
}

output "backend_fixed_ip" {
  value       = try(openstack_networking_port_v2.backend.all_fixed_ips[0], "")
  description = "Server fixed IP address."
}

output "backend_public_ip" {
  value       = try(openstack_networking_floatingip_v2.backend[0].address, "")
  description = "Server floating IP."
}

output "backend_origin_url" {
  value       = try(openstack_networking_floatingip_v2.backend[0].address, "") != "" ? "http://${openstack_networking_floatingip_v2.backend[0].address}:${var.backend_port}" : "http://${try(openstack_networking_port_v2.backend.all_fixed_ips[0], "")}:${var.backend_port}"
  description = "Reachable backend origin URL."
}

output "app_network_id" {
  value       = openstack_networking_network_v2.app.id
  description = "App network id."
}

output "generated_jwt_secret" {
  value       = local.effective_jwt_secret
  description = "Effective JWT secret."
  sensitive   = true
}
