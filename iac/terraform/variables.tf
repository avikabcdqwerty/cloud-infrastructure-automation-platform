variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "aws_az" {
  description = "AWS availability zone for resources"
  type        = string
  default     = "us-east-1a"
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "owner" {
  description = "Owner or team responsible for resources"
  type        = string
  default     = "cloud-team"
}

variable "tf_state_bucket" {
  description = "S3 bucket for Terraform state"
  type        = string
}

variable "tf_state_lock_table" {
  description = "DynamoDB table for Terraform state locking"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.10.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.10.1.0/24"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "RDS allocated storage (GB)"
  type        = number
  default     = 20
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "postgres"
  sensitive   = true
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "cloud_infra_db"
}

variable "api_ami_id" {
  description = "AMI ID for FastAPI EC2 instance"
  type        = string
}

variable "api_instance_type" {
  description = "EC2 instance type for FastAPI server"
  type        = string
  default     = "t3.micro"
}

variable "ssh_key_name" {
  description = "SSH key name for EC2 access"
  type        = string
}