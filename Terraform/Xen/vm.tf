# vm.tf

locals {
  cloud_init_paths = {
    for name, cfg in var.vms_config :
    name => "${path.module}/${cfg.cloud_init_file}"
  }
}

data "xenorchestra_pool" "pool" {
  name_label = "xenomorph"
}

data "xenorchestra_template" "vm_template" {
  name_label = "Ubuntu 24.04 Cloud Template"
}

data "xenorchestra_sr" "sr" {
  name_label = "Local storage"
  pool_id = data.xenorchestra_pool.pool.id
}

data "xenorchestra_network" "network" {
  name_label = "Pool-wide network associated with eth0"
  pool_id = data.xenorchestra_pool.pool.id
}

resource "xenorchestra_vm" "xo_vms" {
  for_each = var.vms_config # Boucle sur la map

  # Utiliser le nom dynamique (la clé de la map) pour le name_label
  name_label       = "vm-${each.key}"
  name_description = "VM créée pour le rôle : ${each.key}"

  template         = data.xenorchestra_template.vm_template.id
  
  # Utiliser les attributs dynamiques (la valeur de la map)
  cpus             = each.value.cpus
  memory_max       = each.value.ram_mb * 1024 * 1024
  
  # ... (autres arguments)
  
  disk {
    name_label = "disk-os-${each.key}"
    sr_id      = data.xenorchestra_sr.sr.id
    size       = each.value.disk_gb * 1024 * 1024 * 1024
  }

  network {
    network_id = data.xenorchestra_network.network.id
  }

  auto_poweron = true

  cloud_config = templatefile(local.cloud_init_paths[each.key], {
    CLOUD_CONFIG_HOSTNAME = each.key
  })
}
