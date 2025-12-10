variable "aws_region" {
  type    = string
  default = "us-east-1" 
  description = "Région AWS"
}

variable "table_name" {
  type    = string
  default = "ma_table_dynamodb"
  description = "Nom de la table DynamoDB"
}

variable "billing_mode" {
  type    = string
  default = "PAY_PER_REQUEST"
  description = "Mode de facturation: PAY_PER_REQUEST ou PROVISIONED"
}

variable "hash_key" {
  type    = string
  default = "pk"
  description = "Nom de la clé de partition (hash key)"
}

variable "hash_key_type" {
  type    = string
  default = "S" # S = String, N = Number, B = Binary
}

# range_key et type si tu veux une clé de tri
variable "range_key" {
  type    = string
  default = ""
  description = "Nom de la clé de tri (laisser vide si non utilisé)"
}

variable "range_key_type" {
  type    = string
  default = "S"
}

# GSI example variables
variable "gsi_hash_key" {
  type    = string
  default = "status"
  description = "Attribut utilisé comme hash key du GSI"
}

variable "gsi_hash_key_type" {
  type    = string
  default = "S"
}

variable "enable_ttl" {
  type    = bool
  default = false
}

variable "ttl_attribute_name" {
  type    = string
  default = "expires_at"
  description = "Nom de l'attribut TTL (timestamp en secondes depuis epoch)"
}

variable "common_tags" {
  type = map(string)
  default = {
    "Environment" = "dev"
    "Owner"       = "team-xx"
  }
}

# Optionnel: KMS key ARN si tu veux un CMK dédié
variable "kms_key_arn" {
  type    = string
  default = ""
}

variable "ami" {
  type    = string
  default = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 pour us-east-1
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "ssh_public_key" {
  description = "Clé SSH publique pour accéder à l'instance"
  type        = string
}

variable "initial_user" {
  type    = string
  default = "ec2-user"
}
