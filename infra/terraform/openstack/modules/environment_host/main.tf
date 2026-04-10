locals {
  effective_network_id = trimspace(var.network_id) != "" ? trimspace(var.network_id) : (
    var.create_network ? openstack_networking_network_v2.environment[0].id : ""
  )

  effective_subnet_id = trimspace(var.subnet_id) != "" ? trimspace(var.subnet_id) : (
    var.create_network ? openstack_networking_subnet_v2.environment[0].id : ""
  )

  service_ingress_rules = flatten([
    for port in var.exposed_tcp_ports : [
      for cidr in var.service_allowed_cidrs : {
        key  = "${port}-${replace(cidr, "/", "_")}"
        port = port
        cidr = cidr
      }
    ]
  ])

  ssh_ingress_rules = [
    for cidr in var.ssh_allowed_cidrs : {
      key  = replace(cidr, "/", "_")
      cidr = cidr
    }
  ]
}

resource "openstack_networking_network_v2" "environment" {
  count = var.create_network ? 1 : 0

  name           = var.network_name
  admin_state_up = true
}

resource "openstack_networking_subnet_v2" "environment" {
  count = var.create_network ? 1 : 0

  name       = var.subnet_name
  network_id = openstack_networking_network_v2.environment[0].id
  cidr       = var.subnet_cidr
  ip_version = 4
}

resource "openstack_networking_router_v2" "environment" {
  count = var.create_router && var.create_network && trimspace(var.external_network_id) != "" ? 1 : 0

  name                = var.router_name
  admin_state_up      = true
  external_network_id = var.external_network_id
}

resource "openstack_networking_router_interface_v2" "environment" {
  count = length(openstack_networking_router_v2.environment) > 0 ? 1 : 0

  router_id = openstack_networking_router_v2.environment[0].id
  subnet_id = openstack_networking_subnet_v2.environment[0].id
}

data "openstack_images_image_v2" "host" {
  name = var.image_name
}

data "openstack_compute_flavor_v2" "host" {
  name = var.flavor_name
}

resource "openstack_networking_secgroup_v2" "host" {
  name        = "${var.name}-secgroup"
  description = "Security group for ${var.name} docker host"
}

resource "openstack_networking_secgroup_rule_v2" "ssh" {
  for_each = { for rule in local.ssh_ingress_rules : rule.key => rule }

  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 22
  port_range_max    = 22
  remote_ip_prefix  = each.value.cidr
  security_group_id = openstack_networking_secgroup_v2.host.id
}

resource "openstack_networking_secgroup_rule_v2" "service" {
  for_each = { for rule in local.service_ingress_rules : rule.key => rule }

  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = each.value.port
  port_range_max    = each.value.port
  remote_ip_prefix  = each.value.cidr
  security_group_id = openstack_networking_secgroup_v2.host.id
}

resource "openstack_networking_port_v2" "host" {
  name               = "${var.name}-port"
  network_id         = local.effective_network_id
  admin_state_up     = true
  security_group_ids = [openstack_networking_secgroup_v2.host.id]

  dynamic "fixed_ip" {
    for_each = local.effective_subnet_id != "" ? [local.effective_subnet_id] : []
    content {
      subnet_id = fixed_ip.value
    }
  }
}

resource "openstack_compute_instance_v2" "host" {
  name              = var.name
  image_id          = data.openstack_images_image_v2.host.id
  flavor_id         = data.openstack_compute_flavor_v2.host.id
  key_pair          = trimspace(var.keypair_name) != "" ? var.keypair_name : null
  availability_zone = trimspace(var.availability_zone) != "" ? var.availability_zone : null
  config_drive      = true
  user_data = templatefile("${path.module}/templates/docker-host-user-data.sh.tftpl", {
    environment_name           = var.name
    repo_clone_url             = var.repo_clone_url
    repo_ref                   = var.repo_ref
    compose_file               = var.compose_file
    compose_env_filename       = var.compose_env_filename
    compose_env_content_base64 = base64encode(var.compose_env_content)
    deploy_compose_on_boot     = var.deploy_compose_on_boot ? "true" : "false"
  })

  network {
    port = openstack_networking_port_v2.host.id
  }
}

resource "openstack_networking_floatingip_v2" "host" {
  count = var.assign_floating_ip && trimspace(var.floating_ip_pool) != "" ? 1 : 0

  pool = var.floating_ip_pool
}

resource "openstack_networking_floatingip_associate_v2" "host" {
  count = length(openstack_networking_floatingip_v2.host) > 0 ? 1 : 0

  floating_ip = openstack_networking_floatingip_v2.host[0].address
  port_id     = openstack_networking_port_v2.host.id
}
