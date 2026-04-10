variable "auth_url" {
  description = "OpenStack Keystone auth URL"
  type        = string
}

variable "region" {
  description = "OpenStack region name"
  type        = string
  default     = "RegionOne"
}

variable "interface" {
  description = "OpenStack endpoint interface"
  type        = string
  default     = "public"
}

variable "auth_type" {
  description = "OpenStack auth type (password or application_credential)"
  type        = string
  default     = "password"
}

variable "username" {
  description = "OpenStack username"
  type        = string
  default     = ""
}

variable "password" {
  description = "OpenStack password"
  type        = string
  default     = ""
  sensitive   = true
}

variable "project_name" {
  description = "OpenStack project name"
  type        = string
  default     = ""
}

variable "user_domain_name" {
  description = "OpenStack user domain"
  type        = string
  default     = "Default"
}

variable "project_domain_name" {
  description = "OpenStack project domain"
  type        = string
  default     = "Default"
}

variable "application_credential_id" {
  description = "OpenStack application credential id"
  type        = string
  default     = ""
}

variable "application_credential_secret" {
  description = "OpenStack application credential secret"
  type        = string
  default     = ""
  sensitive   = true
}

variable "insecure" {
  description = "Disable TLS certificate validation"
  type        = bool
  default     = false
}

variable "availability_zone" {
  description = "Optional availability zone for the DEV(개발계) host"
  type        = string
  default     = ""
}

variable "create_network" {
  description = "Create a dedicated DEV(개발계) network and subnet"
  type        = bool
  default     = true
}

variable "network_name" {
  description = "DEV(개발계) network name"
  type        = string
  default     = "templates-dev-net"
}

variable "subnet_name" {
  description = "DEV(개발계) subnet name"
  type        = string
  default     = "templates-dev-subnet"
}

variable "subnet_cidr" {
  description = "DEV(개발계) subnet CIDR"
  type        = string
  default     = "10.250.10.0/24"
}

variable "create_router" {
  description = "Create a router and attach the created subnet to the external network"
  type        = bool
  default     = true
}

variable "router_name" {
  description = "DEV(개발계) router name"
  type        = string
  default     = "templates-dev-router"
}

variable "external_network_id" {
  description = "External network id used by the router gateway"
  type        = string
  default     = ""
}

variable "network_id" {
  description = "Existing network id to reuse when create_network=false"
  type        = string
  default     = ""
}

variable "subnet_id" {
  description = "Existing subnet id to reuse when create_network=false"
  type        = string
  default     = ""
}

variable "service_allowed_cidrs" {
  description = "CIDR list allowed to reach published application ports"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "ssh_allowed_cidrs" {
  description = "CIDR list allowed to reach SSH on the DEV(개발계) host"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "name" {
  description = "DEV(개발계) host name"
  type        = string
  default     = "templates-dev"
}

variable "image_name" {
  description = "OpenStack image name"
  type        = string
  default     = "ubuntu-22.04"
}

variable "flavor_name" {
  description = "OpenStack flavor name"
  type        = string
  default     = "m1.medium"
}

variable "keypair_name" {
  description = "OpenStack keypair name"
  type        = string
  default     = ""
}

variable "assign_floating_ip" {
  description = "Allocate and associate a floating IP"
  type        = bool
  default     = false
}

variable "floating_ip_pool" {
  description = "Floating IP pool name"
  type        = string
  default     = ""
}

variable "exposed_tcp_ports" {
  description = "TCP ports exposed by the DEV(개발계) stack"
  type        = list(number)
  default     = [18000, 13000, 13001, 13002, 14000]
}

variable "repo_clone_url" {
  description = "Optional repository clone URL for boot-time deployment"
  type        = string
  default     = ""
}

variable "repo_ref" {
  description = "Git ref used for boot-time deployment"
  type        = string
  default     = "main"
}

variable "compose_env_content" {
  description = "Full .env.dev content used for compose boot deployment"
  type        = string
  default     = ""
}

variable "deploy_compose_on_boot" {
  description = "Clone the repo and run docker compose on first boot"
  type        = bool
  default     = false
}
