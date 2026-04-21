# SKILL: MiniStack — Free Local AWS Emulator
**Source:** https://github.com/Nahuel990/ministack
**Domain:** code
**Trigger:** When you need a free, LocalStack-compatible local AWS emulator for development or CI/CD

## Summary
Drop-in LocalStack replacement. 40+ AWS services on port 4566, ~270MB image, <2s startup. Real infrastructure: RDS uses actual Postgres/MySQL, ElastiCache uses real Redis, Athena uses DuckDB. MIT licensed.

## Key Patterns
- Single port 4566, compatible with boto3, AWS CLI, Terraform, CDK, Pulumi
- Multi-tenancy: 12-digit numeric AWS_ACCESS_KEY_ID = account ID (fully isolated state)
- Reset endpoint for CI: `POST /_ministack/reset` for clean state between tests
- `MINISTACK_REGION` and `MINISTACK_ACCOUNT_ID` env vars

## Usage
Replace LocalStack in any dev or CI environment. Use reset endpoint in test setUp/beforeEach.

## Code/Template
```bash
pip install ministack && ministack    # runs on http://localhost:4566

# Docker
docker run -p 4566:4566 ministackorg/ministack

# With real infra (RDS, ECS, Lambda containers)
docker run -p 4566:4566 -v /var/run/docker.sock:/var/run/docker.sock ministackorg/ministack

# CI: reset between tests
curl -X POST http://localhost:4566/_ministack/reset

# boto3 usage
import boto3
s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
```
