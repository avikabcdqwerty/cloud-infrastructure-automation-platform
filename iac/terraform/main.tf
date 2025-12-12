terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }
  backend "s3" {
    bucket         = var.tf_state_bucket
    key            = "cloud-infra-platform/terraform.tfstate"
    region         = var.aws_region
    encrypt        = true
    dynamodb_table = var.tf_state_lock_table
  }
}

provider "aws" {
  region = var.aws_region
}

# Tagging for audit/compliance
locals {
  common_tags = {
    Project     = "CloudInfraAutomationPlatform"
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "Terraform"
  }
}

# VPC for isolation
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = merge(local.common_tags, { Name = "${var.environment}-vpc" })
}

# Public subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = true
  availability_zone       = var.aws_az
  tags                    = merge(local.common_tags, { Name = "${var.environment}-public-subnet" })
}

# Security group for API server
resource "aws_security_group" "api_sg" {
  name        = "${var.environment}-api-sg"
  description = "Security group for FastAPI server"
  vpc_id      = aws_vpc.main.id

  ingress {
    description      = "Allow HTTP"
    from_port        = 8000
    to_port          = 8000
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    description      = "Allow all outbound"
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, { Name = "${var.environment}-api-sg" })
}

# RDS PostgreSQL for API database
resource "aws_db_instance" "postgres" {
  identifier              = "${var.environment}-cloud-infra-db"
  engine                  = "postgres"
  engine_version          = "15.4"
  instance_class          = var.db_instance_class
  allocated_storage       = var.db_allocated_storage
  storage_encrypted       = true
  username                = var.db_username
  password                = var.db_password
  db_name                 = var.db_name
  vpc_security_group_ids  = [aws_security_group.api_sg.id]
  publicly_accessible     = false
  multi_az                = false
  backup_retention_period = 7
  skip_final_snapshot     = true
  deletion_protection     = false
  tags                    = merge(local.common_tags, { Name = "${var.environment}-cloud-infra-db" })
  subnet_group_name       = aws_db_subnet_group.db_subnet_group.name
}

resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "${var.environment}-db-subnet-group"
  subnet_ids = [aws_subnet.public.id]
  tags       = merge(local.common_tags, { Name = "${var.environment}-db-subnet-group" })
}

# EC2 instance for FastAPI app (containerized)
resource "aws_instance" "api_server" {
  ami                    = var.api_ami_id
  instance_type          = var.api_instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.api_sg.id]
  associate_public_ip_address = true
  key_name               = var.ssh_key_name

  tags = merge(local.common_tags, { Name = "${var.environment}-api-server" })

  # User data to run Docker container (simplified)
  user_data = <<-EOF
    #!/bin/bash
    docker run -d -p 8000:8000 --env DATABASE_URL=${aws_db_instance.postgres.endpoint} cloud-infra-api:latest
  EOF
}

# CloudWatch log group for audit/compliance
resource "aws_cloudwatch_log_group" "api_logs" {
  name              = "/cloud-infra-platform/${var.environment}/api"
  retention_in_days = 30
  tags              = local.common_tags
}

# Outputs for integration
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