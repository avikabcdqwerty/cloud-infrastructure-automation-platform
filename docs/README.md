# Cloud Infrastructure Automation Platform

A DevOps-focused platform to provision, manage, and monitor cloud resources using Infrastructure as Code (IaC), automated CI/CD pipelines, and integrated monitoring/alerting. Ensures consistency, security, and compliance across all environments. Includes a secure, RESTful CRUD API for managing product resources.

---

## Features

- **Infrastructure as Code (IaC):** Automated, version-controlled provisioning of cloud resources (AWS, Azure, GCP).
- **CI/CD Pipelines:** Automated build, test, security scan, and deployment workflows.
- **Monitoring & Alerting:** Real-time cloud-native monitoring and incident response integration.
- **Security & Compliance:** Policy enforcement, audit logging, and access controls.
- **Product CRUD API:** Sample FastAPI application for managing products (Create, Read, Update, Delete).

---

## Directory Structure

```
.
├── api/                  # FastAPI application (CRUD API)
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
├── iac/terraform/        # Terraform IaC modules
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── policies.rego
├── ci-cd/                # CI/CD pipeline and security scan configs
│   ├── pipeline.yaml
│   └── security_scan.yaml
├── monitoring/           # Monitoring and alerting configuration
│   └── monitoring-config.yaml
├── docs/                 # Documentation
│   ├── README.md
│   ├── IaC-usage.md
│   └── monitoring-alerting.md
└── .gitignore
```

---

## Quick Start

### Prerequisites

- Docker
- Python 3.11+
- PostgreSQL (local or cloud RDS)
- Terraform >= 1.6.0
- AWS CLI (if deploying to AWS)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/cloud-infra-automation-platform.git
cd cloud-infra-automation-platform
```

### 2. API Setup (Local Development)

#### a. Install Python dependencies

```bash
cd api
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### b. Set up environment variables

Create a `.env` file or set the following:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/cloud_infra_db
```

#### c. Run the API server

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### d. Run tests

```bash
pytest tests
```

### 3. Containerization

Build and run the API with Docker:

```bash
docker build -t cloud-infra-api:latest .
docker run -p 8000:8000 --env DATABASE_URL=... cloud-infra-api:latest
```

### 4. Infrastructure Provisioning (Terraform)

See [docs/IaC-usage.md](./IaC-usage.md) for full instructions.

```bash
cd iac/terraform
terraform init
terraform plan
terraform apply
```

### 5. CI/CD Pipeline

- GitHub Actions pipeline is defined in `ci-cd/pipeline.yaml`.
- Security scanning workflow is in `ci-cd/security_scan.yaml`.

### 6. Monitoring & Alerting

See [docs/monitoring-alerting.md](./monitoring-alerting.md) for setup and incident response.

---

## API Usage

- **Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check:** `GET /health`
- **Products CRUD:** `POST /products/`, `GET /products/`, `GET /products/{id}`, `PUT /products/{id}`, `DELETE /products/{id}`

All endpoints require OAuth2/JWT authentication (see main.py for integration).

---

## Security & Compliance

- All infrastructure and API changes are logged.
- IaC and pipeline configs are validated via OPA policies.
- Security scanning is automated (Bandit, OPA).
- Access controls and encryption enforced by default.

---

## Documentation

- [IaC Usage](./IaC-usage.md)
- [Monitoring & Alerting](./monitoring-alerting.md)

---

## Contributing

1. Fork the repo and create a feature branch.
2. Ensure all code is tested and passes security scans.
3. Submit a pull request for review.

---

## License

MIT License

---

## Maintainers

- Cloud Team <cloud-team@company.com>