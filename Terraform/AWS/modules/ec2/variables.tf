# variables.tf
variable "aws_region" {
  type    = string
  default = "us-east-1"
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
