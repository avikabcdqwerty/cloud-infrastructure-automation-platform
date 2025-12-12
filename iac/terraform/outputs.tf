output "api_server_public_ip" {
  description = "Public IP of the FastAPI server"
  value       = aws_instance.api_server.public_ip
}

output "db_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group for API logs"
  value       = aws_cloudwatch_log_group.api_logs.name
}