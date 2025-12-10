# main.tf
resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = var.ssh_public_key
}

resource "aws_instance" "example" {
  ami           = var.ami
  instance_type = var.instance_type
  key_name      = aws_key_pair.deployer.key_name

  user_data = <<-EOF
              #!/bin/bash
              # Création utilisateur
              useradd -m -s /bin/bash ${var.initial_user}

              # Mise en place de la clé SSH pour l'utilisateur
              mkdir -p /home/${var.initial_user}/.ssh
              echo "${var.ssh_public_key}" > /home/${var.initial_user}/.ssh/authorized_keys
              chown -R ${var.initial_user}:${var.initial_user} /home/${var.initial_user}/.ssh
              chmod 700 /home/${var.initial_user}/.ssh
              chmod 600 /home/${var.initial_user}/.ssh/authorized_keys
              EOF
}

