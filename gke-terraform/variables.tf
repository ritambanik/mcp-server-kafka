variable "project_id" {
  type        = string
  description = "GCP project id"
}

variable "region" {
  type        = string
  default     = "us-central1"
}

variable "zone" {
  type        = string
  default     = "us-central1-a"
}

variable "cluster_name" {
  type    = string
  default = "mcp-server-cluster"
}

variable "network_name" {
  type    = string
  default = "mcp-server-network"
}

variable "subnet_name" {
  type    = string
  default = "mcp-server-subnet"
}

variable "subnet_ip_cidr" {
  type    = string
  default = "10.10.0.0/16"
}

variable "node_pool_name" {
  type    = string
  default = "primary-pool"
}

variable "node_count" {
  type    = number
  default = 2
}

variable "node_machine_type" {
  type    = string
  default = "e2-medium"
}

variable "domain_name" {
  description = "The domain name (e.g., example.com)"
  type        = string
  default     = "my.mcp-server.com"
}

variable "dns_zone_name" {
  description = "Name for the DNS zone"
  type        = string
  default     = "my-mcp-server-zone"
}

variable "ttl" {
  description = "TTL for DNS records in seconds"
  type        = number
  default     = 300
}
