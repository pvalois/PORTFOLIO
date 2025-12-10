# Définition du fournisseur Xen Orchestra (XO)

terraform {
  required_version = ">= 1.0" 
  required_providers {
    xenorchestra = {
      source  = "vatesfr/xenorchestra"
      version = "~> 0.9"
    }
  }
}

provider "xenorchestra" {
  url      = var.xo_url
  username = var.xo_username
  password = var.xo_password
  insecure = true
}

