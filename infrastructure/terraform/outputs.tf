output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "public_subnets" {
  description = "List of public subnet IDs"
  value       = module.vpc.public_subnets
}

output "private_subnets" {
  description = "List of private subnet IDs"
  value       = module.vpc.private_subnets
}

output "db_instance_endpoint" {
  description = "The connection endpoint for the RDS instance"
  value       = aws_db_instance.mysql.endpoint
}

output "load_balancer_dns" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "frontend_repository_url" {
  description = "URL of the ECR repository for frontend"
  value       = aws_ecr_repository.frontend.repository_url
}

output "api_repository_url" {
  description = "URL of the ECR repository for API"
  value       = aws_ecr_repository.api.repository_url
}