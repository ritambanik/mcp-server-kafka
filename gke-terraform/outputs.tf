output "cluster_name" {
  value = google_container_cluster.primary.name
}

output "endpoint" {
  value = google_container_cluster.primary.endpoint
}

output "kubeconfig" {
  description = "Kubeconfig entry (base64). You can decode/use it to configure kubectl."
  value       = google_container_cluster.primary.master_auth[0].cluster_ca_certificate
}

output "dns_zone_name" {
  description = "The name of the DNS zone"
  value       = google_dns_managed_zone.main.name
}

output "dns_zone_dns_name" {
  description = "The DNS name of the zone"
  value       = google_dns_managed_zone.main.dns_name
}

output "name_servers" {
  description = "The name servers for the DNS zone"
  value       = google_dns_managed_zone.main.name_servers
}

output "zone_id" {
  description = "The zone ID"
  value       = google_dns_managed_zone.main.id
}
