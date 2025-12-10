# variables.tf

variable "xo_url" {
  description = "Adresse WebSocket du serveur Xen Orchestra"
  type        = string
}

variable "xo_username" {
  description = "Nom d’utilisateur Xen Orchestra"
  type        = string
}

variable "xo_password" {
  description = "Mot de passe Xen Orchestra"
  type        = string
  sensitive   = true
}

# --- Configuration de la VM ---
variable "vms_config" {
  description = "Configuration de multiples VMs (CPUs, RAM en Mo, Disque en Go)."
  type = map(object({
    cpus = number
    ram_mb = number
    disk_gb = number
    cloud_init_file = string
  }))
  # Un default est optionnel si vous définissez toujours les valeurs dans terraform.tfvars
}

