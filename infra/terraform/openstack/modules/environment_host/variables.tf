variable "availability_zone" {
  description = "Optional availability zone for the environment host"
  type        = string
  default     = ""
}

variable "create_network" {
  description = "Create a dedicated network and subnet for this environment"
  type        = bool
  default     = false
}

variable "network_name" {
  description = "Environment network name"
  type        = string
}

variable "subnet_name" {
  description = "Environment subnet name"
  type        = string
}

variable "subnet_cidr" {
  description = "Environment subnet CIDR"
  type        = string
}

variable "create_router" {
  description = "Create a router and attach the created subnet to the external network"
  type        = bool
  default     = false
}

variable "router_name" {
  description = "Environment router name"
  type        = string
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

  validation {
    condition     = var.create_network || trimspace(var.network_id) != ""
    error_message = "network_id must be set when create_network=false."
  }
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
  description = "CIDR list allowed to reach SSH on the environment host"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "name" {
  description = "Environment host name"
  type        = string
}

variable "image_name" {
  description = "OpenStack image name"
  type        = string
}

variable "flavor_name" {
  description = "OpenStack flavor name"
  type        = string
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
  description = "TCP ports exposed by the environment stack"
  type        = list(number)
  default     = []
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

variable "compose_file" {
  description = "Compose file path relative to the cloned repo"
  type        = string
}

variable "compose_env_filename" {
  description = "Compose env file name written on the host"
  type        = string
}

variable "compose_env_content" {
  description = "Full env file content used for compose boot deployment"
  type        = string
  default     = ""
}

variable "deploy_compose_on_boot" {
  description = "Clone the repo and run docker compose on first boot"
  type        = bool
  default     = false
}
