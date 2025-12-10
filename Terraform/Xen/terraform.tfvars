# terraform.tfvars

vms_config = {
  db01 = {
    cpus     = 2
    ram_mb   = 2048 
    disk_gb  = 10
    cloud_init_file = "ubuntu-cloud.yaml"
  },

  web01 = {
    cpus     = 2
    ram_mb   = 2048 
    disk_gb  = 10
    cloud_init_file = "ubuntu-cloud.yaml"
  }

}
