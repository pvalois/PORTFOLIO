terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
  required_version = ">= 1.0"
}

resource "aws_dynamodb_table" "this" {
  name         = var.table_name
  billing_mode = var.billing_mode # "PAY_PER_REQUEST" ou "PROVISIONED"

  hash_key  = var.hash_key
  # Si tu veux une clé de tri (range), décommente la ligne ci-dessous et remplis variable range_key
  # range_key = var.range_key

  attribute {
    name = var.hash_key
    type = var.hash_key_type # "S", "N", ou "B"
  }

  # Exemple: attribut pour un GSI
  attribute {
    name = var.gsi_hash_key
    type = var.gsi_hash_key_type
  }

  # Global Secondary Index (exemple)
  global_secondary_index {
    name               = "gsi-by-status"
    hash_key           = var.gsi_hash_key
    projection_type    = "ALL"
    # Si en mode PROVISIONED, indiquer read/write_capacity:
    # read_capacity  = 5
    # write_capacity = 5
  }

  # Time to Live (TTL) — désactive par défaut si vide
  ttl {
    attribute_name = var.ttl_attribute_name
    enabled        = var.enable_ttl
  }

  # Encryption: AWS-owned CMKs by default; pour utiliser CMK géré par KMS, configurer kms_key_arn
  server_side_encryption {
    enabled     = true
    # kms_key_arn = var.kms_key_arn
  }

  tags = merge(
    var.common_tags,
    {
      "Name" = var.table_name
    }
  )
}


