# Store Management Backend

Containerized store management backend consisting of multiple role-specific microservices, built with Flask, PostgreSQL, and Docker Compose.

[In Progress] Ethereum smart contract integration for payment processing.

## Technologies

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose
- [In Progress] Ethereum / Ganache CLI
- [In Progress] Web3.py

## Features

- User registration and authentication
- JWT-based authorization
- Product import via CSV
- Product search
- Order creation and tracking
- Courier order pickup and delivery
- Product and category statistics
- [In Progress] Ethereum blockchain payment integration

## Architecture

### Services:

- Authentication Service
- Store Service
    - Owner Service
    - Customer Service
    - Courier Service

### Databases:

- Authentication Database
- Store Database

## Running

Start databases and services:

```bash
.\cmd_app.bat up
```

Reset system:

```bash
.\cmd_app.bat reset
```

Stop system:

```bash
.\cmd_app.bat down
```

Run grading tests without blockchain integration:

```bash
.\cmd_test.bat no-blockchain all
```

[In Progress] Run grading tests with blockchain integration:

```bash
.\cmd_test.bat blockchain all
```

## Testing

1. Grading tests assume a clean database state. Before each test run, reset the system and wait for all services to become available:

```bash
.\cmd_app.bat reset
```

2. After the services start successfully, run tests without blockchain integration:

```bash
.\cmd_test.bat no-blockchain all
```

or with it:

[In Progress]

```bash
.\cmd_test.bat blockchain all
```
