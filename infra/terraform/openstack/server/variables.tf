variable "auth_url" {
  type        = string
  description = "OpenStack Keystone auth URL."
}

variable "region" {
  type        = string
  description = "OpenStack region name."
  default     = "RegionOne"
}

variable "interface" {
  type        = string
  description = "OpenStack endpoint interface."
  default     = "public"
}

variable "auth_type" {
  type        = string
  description = "OpenStack auth type."
  default     = "password"
}

variable "username" {
  type        = string
  description = "OpenStack username."
  default     = ""
}

variable "password" {
  type        = string
  description = "OpenStack password."
  default     = ""
  sensitive   = true
}

variable "project_name" {
  type        = string
  description = "OpenStack project name."
  default     = ""
}

variable "user_domain_name" {
  type        = string
  description = "OpenStack user domain name."
  default     = "Default"
}

variable "project_domain_name" {
  type        = string
  description = "OpenStack project domain name."
  default     = "Default"
}

variable "application_credential_id" {
  type        = string
  description = "OpenStack application credential id."
  default     = ""
}

variable "application_credential_secret" {
  type        = string
  description = "OpenStack application credential secret."
  default     = ""
  sensitive   = true
}

variable "insecure" {
  type        = bool
  description = "Disable TLS validation."
  default     = false
}

variable "service_name" {
  type        = string
  description = "Service short name."
  default     = "template-service"
}

variable "application_name" {
  type        = string
  description = "Human-readable application name passed to the backend environment."
  default     = "Template API"
}

variable "phase" {
  type        = string
  description = "Deployment phase."
  default     = "dev"

  validation {
    condition     = contains(["dev", "prod"], lower(var.phase))
    error_message = "phase must be one of: dev, prod"
  }
}

variable "external_network_name" {
  type        = string
  description = "External provider network used for router gateway and floating IP."
  default     = "public"
}

variable "app_network_name" {
  type        = string
  description = "Tenant app network name. Leave empty to derive from service+phase."
  default     = ""
}

variable "app_subnet_name" {
  type        = string
  description = "Tenant app subnet name. Leave empty to derive from service+phase."
  default     = ""
}

variable "app_subnet_cidr" {
  type        = string
  description = "App subnet CIDR."
  default     = "10.42.0.0/24"
}

variable "dns_nameservers" {
  type        = list(string)
  description = "Optional DNS nameservers for the app subnet."
  default     = ["1.1.1.1", "8.8.8.8"]
}

variable "backend_image_name" {
  type        = string
  description = "Boot image name for the API compute instance."
  default     = "ubuntu-24.04-noble-amd64"
}

variable "instance_flavor_name" {
  type        = string
  description = "Flavor for the API compute instance."
  default     = "m1.small"
}

variable "backend_port" {
  type        = number
  description = "API service port."
  default     = 8080
}

variable "associate_floating_ip" {
  type        = bool
  description = "Whether to attach a floating IP to the API instance."
  default     = true
}

variable "backend_ingress_cidrs" {
  type        = list(string)
  description = "CIDRs allowed to reach the API service port."
  default     = ["0.0.0.0/0"]
}

variable "ssh_ingress_cidrs" {
  type        = list(string)
  description = "CIDRs allowed to SSH to the API instance."
  default     = []
}

variable "ssh_keypair_name" {
  type        = string
  description = "OpenStack keypair name used for browser-terminal SSH access."
  default     = ""
}

variable "ssh_public_key" {
  type        = string
  description = "Public key material registered in OpenStack for browser-terminal SSH access."
  default     = ""
}

variable "desired_state" {
  type        = string
  description = "Desired server instance power state."
  default     = "running"

  validation {
    condition     = contains(["running", "stopped"], lower(var.desired_state))
    error_message = "desired_state must be one of: running, stopped"
  }
}

variable "backend_container_image" {
  type        = string
  description = "Prebuilt backend image. If empty, repo bootstrap build is used."
  default     = ""
}

variable "backend_container_name" {
  type        = string
  description = "Runtime container name."
  default     = "template-service-server"
}

variable "backend_repo_url" {
  type        = string
  description = "Repo URL used for bootstrap build."
  default     = "https://github.com/example-org/example-service.git"
}

variable "backend_repo_ref" {
  type        = string
  description = "Repo ref for bootstrap build."
  default     = "main"
}

variable "backend_repo_subdir" {
  type        = string
  description = "Repo-relative server directory."
  default     = "server"
}

variable "jwt_secret_key" {
  type        = string
  description = "JWT secret key. Leave empty to auto-generate."
  default     = ""
  sensitive   = true
}

variable "backend_env" {
  type        = map(string)
  description = "Additional backend environment variables."
  default     = {}
}

variable "tags" {
  type        = map(string)
  description = "Additional metadata tags."
  default     = {}
}
