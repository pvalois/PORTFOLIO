### variables.auto.tfvars
clone_node_name        = "localhost"
clone_vm_id            = 500
cloudinit_dns_domain   = "maison.local"
cloudinit_dns_servers  = ["8.8.8.8"]
cloudinit_ssh_keys     = ["ssh-rsa ssh-ed25519 ..."]
cloudinit_user_account = "johncarter"
datastore_id           = "Store1"
disk_file_format       = "raw"
node_name              = "crucible"
pve_api_token          = "root@pam!terraform=REDACTED-REDA-REDA-REDA-REDACTEDREDA"
pve_host_address       = "https://promoxer1:8006/"
tmp_dir                = "/tmp"
vm_bridge_lan          = "vmbr0"
vm_cpu_cores_number    = 1
vm_cpu_type            = "x86-64-v2-AES"
vm_description         = "Managed by terraform"
vm_disk_size           = 10
vm_id                  = 602
vm_memory_max          = 1024
vm_memory_min          = 1024
vm_name                = "mars"
vm_socket_number       = 1
