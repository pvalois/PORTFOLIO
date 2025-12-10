output "dynamodb_table_name" {
  description = "Nom de la table DynamoDB"
  value       = aws_dynamodb_table.this.name
}

output "dynamodb_table_arn" {
  description = "ARN de la table DynamoDB"
  value       = aws_dynamodb_table.this.arn
}

output "dynamodb_table_stream_arn" {
  description = "ARN du stream si activé (sinon vide)"
  value       = aws_dynamodb_table.this.stream_arn
}

