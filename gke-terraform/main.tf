# Network + Subnet
resource "google_compute_network" "vpc" {
  name                    = var.network_name
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = var.subnet_name
  ip_cidr_range = var.subnet_ip_cidr
  region        = var.region
  network       = google_compute_network.vpc.id
  private_ip_google_access = true
}

# GKE control plane (autopilot=false; change as desired)
resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.zone

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  remove_default_node_pool = true
  initial_node_count       = 1

  # Basic security/hardening examples:
  enable_legacy_abac = false
  enable_shielded_nodes = true

  ip_allocation_policy {
    # use_ip_aliases is enabled by default when ip_allocation_policy is set
  }

  # Disable deletion protection for allowing terraform to delete the cluster; enable in production
  deletion_protection = false

  # Master authorized networks, logging, monitoring options, etc. can be added here.
}

# Separate node pool (so you can upgrade / scale independently)
resource "google_container_node_pool" "primary_pool" {
  name       = var.node_pool_name
  cluster    = google_container_cluster.primary.name
  location   = var.zone

  node_count = var.node_count

  node_config {
    machine_type = var.node_machine_type

    # Example: use shielded VMs
    shielded_instance_config {
      enable_secure_boot          = true
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 2
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }
}

# Create a static external IP address
# This can be used for LoadBalancer services
resource "google_compute_address" "static_external_ip" {
  name        = "my-ingress-ip"
  region      = "us-central1" # Replace with your desired region
  description = "Static external IP for my application"
}


# Create the managed DNS zone
resource "google_dns_managed_zone" "main" {
  name        = var.dns_zone_name
  dns_name    = "${var.domain_name}."
  description = "DNS zone for ${var.domain_name}"
  
  # Optional: Make it private if needed
  # visibility = "private"
  
  labels = {
    environment = "development"
    managed-by  = "terraform"
  }
}

# A record for root domain
resource "google_dns_record_set" "root_a" {
  name         = google_dns_managed_zone.main.dns_name
  managed_zone = google_dns_managed_zone.main.name
  type         = "A"
  ttl          = var.ttl
  rrdatas      = [google_compute_address.static_external_ip.address]  # Use the static IP address
}