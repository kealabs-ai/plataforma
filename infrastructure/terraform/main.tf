provider "aws" {
  region = var.aws_region
}

# VPC e Subnets
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "kognia-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
  
  tags = {
    Environment = var.environment
    Project     = "KogniaOne"
  }
}

# Security Groups
resource "aws_security_group" "web" {
  name        = "kognia-web-sg"
  description = "Security group for web traffic"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name        = "kognia-web-sg"
    Environment = var.environment
  }
}

resource "aws_security_group" "db" {
  name        = "kognia-db-sg"
  description = "Security group for database"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name        = "kognia-db-sg"
    Environment = var.environment
  }
}

# RDS Database
resource "aws_db_instance" "mysql" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "5.6.23"
  instance_class       = "db.t3.micro"
  name                 = "kognia_db"
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.mysql5.6"
  db_subnet_group_name = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.db.id]
  skip_final_snapshot  = true
  
  tags = {
    Name        = "kognia-mysql"
    Environment = var.environment
  }
}

resource "aws_db_subnet_group" "default" {
  name       = "kognia-db-subnet-group"
  subnet_ids = module.vpc.private_subnets
  
  tags = {
    Name        = "kognia-db-subnet-group"
    Environment = var.environment
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "kognia-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Name        = "kognia-ecs-cluster"
    Environment = var.environment
  }
}

# ECR Repositories
resource "aws_ecr_repository" "frontend" {
  name = "kognia-frontend"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "api" {
  name = "kognia-api"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

# Load Balancer
resource "aws_lb" "main" {
  name               = "kognia-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = module.vpc.public_subnets
  
  tags = {
    Name        = "kognia-alb"
    Environment = var.environment
  }
}