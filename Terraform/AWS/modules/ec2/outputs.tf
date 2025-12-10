# outputs.tf

output "instance_id" {
  description = "L'ID unique de l'instance EC2 créée."
  value       = aws_instance.example.id
}

output "public_ip" {
  description = "L'adresse IP publique de l'instance (si elle a une IP publique)."
  value       = aws_instance.example.public_ip
}

output "private_ip" {
  description = "L'adresse IP privée de l'instance."
  value       = aws_instance.example.private_ip
}

output "ssh_command" {
  description = "Commande SSH pour se connecter à l'instance en utilisant l'utilisateur initial."
  value       = "ssh -i <CHEMIN_VERS_VOTRE_CLE_PRIVEE> ${var.initial_user}@${aws_instance.example.public_ip}"
}

output "key_name" {
  description = "Le nom de la paire de clés SSH utilisée pour l'instance."
  value       = aws_key_pair.deployer.key_name
}

output "arn" {
  description = "L'Amazon Resource Name (ARN) complet de l'instance."
  value       = aws_instance.example.arn
}
