module "app_server" {
  source = "../../modules/ec2"

  # Transmission au module EC2
  aws_region     = var.aws_region     
  ami            = var.ami
  instance_type  = var.instance_type
  initial_user   = var.initial_user
  ssh_public_key = var.ssh_public_key
}
