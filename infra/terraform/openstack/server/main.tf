resource "random_password" "jwt" {
  count   = var.jwt_secret_key == "" ? 1 : 0
  length  = 40
  special = false
}

locals {
  phase                = lower(var.phase)
  stack_name           = "${var.service_name}-${local.phase}"
  app_network_name     = var.app_network_name != "" ? var.app_network_name : "${local.stack_name}-net"
  app_subnet_name      = var.app_subnet_name != "" ? var.app_subnet_name : "${local.stack_name}-subnet"
  effective_jwt_secret = var.jwt_secret_key != "" ? var.jwt_secret_key : random_password.jwt[0].result
  power_state          = lower(var.desired_state) == "stopped" ? "shutoff" : "active"
  runtime_root         = "/opt/${var.service_name}"
  common_tags = merge(
    {
      Name       = local.stack_name
      Service    = var.service_name
      Phase      = local.phase
      ManagedBy  = "terraform"
      ManagedVia = "aspace"
      Cloud      = "openstack"
    },
    var.tags,
  )
  backend_env_lines = concat(
    [
      "APP_NAME=${var.application_name}",
      "DEBUG=${local.phase == "prod" ? "false" : "true"}",
      "JWT_SECRET_KEY=${local.effective_jwt_secret}"
    ],
    [for key, value in var.backend_env : "${key}=${value}"]
  )
}

data "openstack_images_image_v2" "backend" {
  name        = var.backend_image_name
  most_recent = true
}

data "openstack_compute_flavor_v2" "backend" {
  name = var.instance_flavor_name
}

data "openstack_networking_network_v2" "external" {
  name     = var.external_network_name
  external = true
}

resource "openstack_networking_network_v2" "app" {
  name           = local.app_network_name
  admin_state_up = true
}

resource "openstack_networking_subnet_v2" "app" {
  name            = local.app_subnet_name
  network_id      = openstack_networking_network_v2.app.id
  cidr            = var.app_subnet_cidr
  ip_version      = 4
  dns_nameservers = var.dns_nameservers
}

resource "openstack_networking_router_v2" "app" {
  name                = "${local.stack_name}-router"
  external_network_id = data.openstack_networking_network_v2.external.id
  enable_snat         = true
}

resource "openstack_networking_router_interface_v2" "app" {
  router_id = openstack_networking_router_v2.app.id
  subnet_id = openstack_networking_subnet_v2.app.id
}

resource "openstack_networking_secgroup_v2" "backend" {
  name                 = "${local.stack_name}-backend"
  description          = "Template backend ingress"
  delete_default_rules = true
}

resource "openstack_networking_secgroup_rule_v2" "backend_http" {
  for_each          = toset(var.backend_ingress_cidrs)
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = var.backend_port
  port_range_max    = var.backend_port
  remote_ip_prefix  = each.value
  security_group_id = openstack_networking_secgroup_v2.backend.id
}

resource "openstack_networking_secgroup_rule_v2" "backend_ssh" {
  for_each          = toset(var.ssh_ingress_cidrs)
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 22
  port_range_max    = 22
  remote_ip_prefix  = each.value
  security_group_id = openstack_networking_secgroup_v2.backend.id
}

resource "openstack_networking_secgroup_rule_v2" "backend_egress" {
  direction         = "egress"
  ethertype         = "IPv4"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.backend.id
}

resource "openstack_compute_keypair_v2" "terminal" {
  count      = trimspace(var.ssh_public_key) != "" ? 1 : 0
  name       = trimspace(var.ssh_keypair_name) != "" ? trimspace(var.ssh_keypair_name) : "${local.stack_name}-terminal"
  public_key = trimspace(var.ssh_public_key)
}

resource "openstack_networking_port_v2" "backend" {
  name               = "${local.stack_name}-backend"
  network_id         = openstack_networking_network_v2.app.id
  security_group_ids = [openstack_networking_secgroup_v2.backend.id]

  fixed_ip {
    subnet_id = openstack_networking_subnet_v2.app.id
  }
}

resource "openstack_compute_instance_v2" "backend" {
  name         = "${local.stack_name}-backend"
  image_id     = data.openstack_images_image_v2.backend.id
  flavor_id    = data.openstack_compute_flavor_v2.backend.id
  key_pair     = length(openstack_compute_keypair_v2.terminal) > 0 ? openstack_compute_keypair_v2.terminal[0].name : null
  config_drive = true
  user_data = templatefile("${path.module}/templates/server-user-data.sh.tftpl", {
    runtime_root            = local.runtime_root
    service_name            = var.service_name
    backend_container_image = var.backend_container_image
    backend_container_name  = var.backend_container_name
    backend_port            = var.backend_port
    backend_repo_url        = var.backend_repo_url
    backend_repo_ref        = var.backend_repo_ref
    backend_repo_subdir     = var.backend_repo_subdir
    backend_env_text        = join("\n", local.backend_env_lines)
  })
  power_state = local.power_state
  metadata    = local.common_tags

  network {
    port = openstack_networking_port_v2.backend.id
  }

  depends_on = [openstack_networking_router_interface_v2.app]
}

resource "openstack_networking_floatingip_v2" "backend" {
  count = var.associate_floating_ip ? 1 : 0
  pool  = var.external_network_name
}

resource "openstack_networking_floatingip_associate_v2" "backend" {
  count       = var.associate_floating_ip ? 1 : 0
  floating_ip = openstack_networking_floatingip_v2.backend[0].address
  port_id     = openstack_networking_port_v2.backend.id
}
