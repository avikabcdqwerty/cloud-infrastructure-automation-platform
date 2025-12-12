package terraform.security

# Enforce encryption for RDS instances
deny[msg] {
  input.resource_type == "aws_db_instance"
  not input.resource.storage_encrypted
  msg := sprintf("RDS instance '%s' must have storage_encrypted=true for compliance.", [input.resource.identifier])
}

# Enforce public accessibility off for RDS
deny[msg] {
  input.resource_type == "aws_db_instance"
  input.resource.publicly_accessible
  msg := sprintf("RDS instance '%s' must not be publicly accessible.", [input.resource.identifier])
}

# Enforce security group ingress restrictions (no 0.0.0.0/0 except HTTP/HTTPS)
deny[msg] {
  input.resource_type == "aws_security_group"
  some i
  ingress := input.resource.ingress[i]
  ingress.cidr_blocks[_] == "0.0.0.0/0"
  not allowed_ports[ingress.from_port]
  msg := sprintf("Security group '%s' allows ingress from 0.0.0.0/0 on port %d, which is not allowed.", [input.resource.name, ingress.from_port])
}

allowed_ports = {80, 443, 8000}

# Enforce audit logging for API server (CloudWatch log group must exist)
deny[msg] {
  input.resource_type == "aws_instance"
  not input.resource.tags["AuditLogEnabled"]
  msg := sprintf("API server '%s' must have AuditLogEnabled tag for compliance.", [input.resource.tags["Name"]])
}

# Enforce tagging for all resources
deny[msg] {
  not input.resource.tags["Project"]
  msg := sprintf("Resource '%s' must have 'Project' tag for traceability.", [input.resource_type])
}

# Export deny rules for use in OPA/Terraform validation