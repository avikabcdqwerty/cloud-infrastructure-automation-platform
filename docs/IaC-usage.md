# IaC Usage Guide

This document describes how to use, update, and validate the Infrastructure as Code (IaC) templates for the Cloud Infrastructure Automation Platform.

---

## Overview

- **Tool:** [Terraform](https://www.terraform.io/) (>= 1.6.0)
- **Cloud Provider:** AWS (can be adapted for Azure/GCP)
- **Modules:** VPC, Subnets, Security Groups, RDS PostgreSQL, EC2 (API server), CloudWatch, tagging, compliance
- **Policy Enforcement:** [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) policies in `policies.rego`
- **State Management:** S3 backend with DynamoDB locking

---

## Prerequisites

- Terraform CLI >= 1.6.0
- AWS CLI configured with appropriate credentials
- S3 bucket and DynamoDB table for state management
- Access to required AMI for API server
- SSH key pair for EC2 access

---

## Initial Setup

1. **Configure Terraform Backend**

   Edit `variables.tf` and set:
   - `tf_state_bucket`: S3 bucket name for state
   - `tf_state_lock_table`: DynamoDB table name for state locking

2. **Set Required Variables**

   Update `variables.tf` with values for:
   - `api_ami_id`: AMI ID for EC2 API server
   - `ssh_key_name`: SSH key name for EC2 access
   - `db_password`: Secure password for RDS

   You can override variables via CLI or `.tfvars` files.

---

## Workflow

### 1. Initialize Terraform

```bash
cd iac/terraform
terraform init
```

### 2. Validate Configuration

```bash
terraform validate
```

### 3. OPA Policy Validation

Validate IaC against compliance/security policies:

```bash
opa eval --input terraform.tfplan --data policies.rego "data.terraform.security.deny"
```

Or use the CI/CD pipeline (`ci-cd/pipeline.yaml`) for automated checks.

### 4. Plan Infrastructure Changes

```bash
terraform plan -out=tfplan
```

### 5. Apply Infrastructure Changes

```bash
terraform apply tfplan
```

### 6. Destroy Infrastructure (if needed)

```bash
terraform destroy
```

---

## Updating IaC Templates

- **Version Control:** All changes must be committed to Git and peer-reviewed.
- **Parameterization:** Use variables in `variables.tf` for environment-specific values.
- **Compliance:** All resources must have required tags and comply with OPA policies.
- **Security:** Never commit secrets or sensitive values to source control.

---

## Environments

- Use `environment` variable to set `dev`, `staging`, or `prod`.
- Each environment should have isolated resources and state.

---

## Troubleshooting

- **State Locking Issues:** Check DynamoDB table and S3 bucket permissions.
- **Policy Violations:** Review OPA policy output for details.
- **Resource Conflicts:** Ensure unique names/tags per environment.

---

## Best Practices

- Always run `terraform plan` before `apply`.
- Validate with OPA before provisioning.
- Use secure, encrypted storage for state and secrets.
- Tag all resources for traceability.
- Monitor changes via CloudWatch and audit logs.

---

## References

- [Terraform Documentation](https://www.terraform.io/docs/)
- [OPA Policy Authoring](https://www.openpolicyagent.org/docs/latest/policy-language/)
- [AWS Terraform Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

## Contact

For support or questions, contact the Cloud Team: cloud-team@company.com