# Backend Core

Core backend services for personal website built with FastAPI, SQLAlchemy, and modern Python practices.

[![Build Status](https://github.com/macayaven/backend-core/actions/workflows/main.yml/badge.svg)](https://github.com/macayaven/backend-core/actions)
[![Code Quality](https://img.shields.io/codeclimate/maintainability/macayaven/backend-core)](https://codeclimate.com/github/macayaven/backend-core)
[![Coverage Status](https://coveralls.io/repos/github/macayaven/backend-core/badge.svg?branch=main)](https://coveralls.io/github/macayaven/backend-core?branch=main)
[![License](https://img.shields.io/github/license/macayaven/backend-core)](https://github.com/macayaven/backend-core/blob/main/LICENSE)
[![Docker Image](https://img.shields.io/docker/pulls/macayaven/backend-core)](https://hub.docker.com/r/macayaven/backend-core)
[![Contributors](https://img.shields.io/github/contributors/macayaven/backend-core)](https://github.com/macayaven/backend-core/graphs/contributors)
[![Stars](https://img.shields.io/github/stars/macayaven/backend-core?style=social)](https://github.com/macayaven/backend-core/stargazers)
[![Open Issues](https://img.shields.io/github/issues/macayaven/backend-core)](https://github.com/macayaven/backend-core/issues)

## Project Structure

```
backend_core/
├── backend_core/           # Main application package
│   ├── api/               # API endpoints and routers
│   │   └── v1/           # API version 1
│   │       └── endpoints/ # API endpoint implementations
│   ├── core/             # Core functionality
│   │   ├── config.py     # Configuration management
│   │   ├── security.py   # Security utilities
│   │   └── deps.py       # FastAPI dependencies
│   ├── db/               # Database
│   │   ├── base.py      # Base models
│   │   └── session.py   # Database session management
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── main.py         # FastAPI application setup
├── alembic/             # Database migrations
│   ├── versions/       # Migration versions
│   └── env.py         # Alembic environment
├── tests/              # Test suite
│   ├── api/           # API tests
│   │   └── v1/       # Version 1 API tests
│   └── conftest.py   # Test configurations
├── tasks_modules/      # Task management modules
│   ├── docker.py      # Docker management tasks
│   ├── format.py      # Code formatting tasks
│   ├── lint.py       # Code linting tasks
│   └── test.py       # Test tasks
├── scripts/          # Utility scripts
├── Dockerfile       # Multi-stage container definition
├── docker-compose.yml # Container orchestration
├── alembic.ini     # Alembic configuration
├── pyproject.toml  # Poetry project configuration
├── pytest.ini     # Pytest configuration
└── .env.example   # Environment template
```

## Features

### API Framework
- **FastAPI**: High-performance async web framework
  - OpenAPI (Swagger) documentation
  - Automatic data validation
  - Dependency injection system
  - Async request handling

### Database
- **SQLAlchemy**: SQL toolkit and ORM
  - Async database operations
  - Model relationships
  - Connection pooling
- **Alembic**: Database migrations
  - Version control for database schema
  - Auto-generated migrations
  - Migration history

### Authentication & Security
- JWT token authentication
- Password hashing with bcrypt
- Role-based access control
- Secure password reset flow
- Environment variable management

### Data Validation
- **Pydantic**: Data validation using Python type annotations
  - Request/Response models
  - Configuration management
  - Email validation
  - Custom validators

### Development Tools
- **Code Quality**:
  - Black (code formatting)
  - isort (import sorting)
  - autoflake (unused import removal)
  - Ruff (fast Python linter)
  - MyPy (static type checking)

- **Testing**:
  - pytest for unit and integration tests
  - async test support
  - test coverage reporting
  - fixture-based test data
  - Docker-based testing environment

- **Docker Support**:
  - Multi-stage builds
  - Development and production configurations
  - Docker Compose orchestration
  - Automated testing in containers

## Quick Start

### Prerequisites
- Python 3.12+
- Poetry (Python package manager)
- Docker and Docker Compose
- Make (optional, for convenience)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/macayaven/backend-core.git
   cd backend-core
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database and create first superuser:
   ```bash
   invoke setup
   ```

5. Start the development environment:
   ```bash
   invoke docker.up  # Starts all services
   # OR
   invoke docker.up-db  # Starts only the database
   ```

### Development Tasks

The project uses [Invoke](http://www.pyinvoke.org/) for task management. Here are the main tasks:

- **Setup**:
  - `invoke setup`: Initialize database, run migrations, and create first superuser
  - `invoke docker.up-db`: Start only the database container
  - `invoke docker.up`: Start all services in Docker

- **Development**:
  - `invoke local.dev`: Start local development server
  - `invoke local.shell`: Open Python shell with project context
  - `invoke docker.logs`: View Docker container logs

- **Testing**:
  - `invoke test`: Run tests with coverage
  - `invoke local.test`: Run tests in local environment
  - `invoke docker.test`: Run tests in Docker environment

- **Code Quality**:
  - `invoke quality.format`: Format code with Black
  - `invoke quality.check-format`: Check code formatting
  - `invoke quality.lint`: Run linting tools

- **Cleanup**:
  - `invoke local.clean`: Clean local development environment
  - `invoke docker.clean`: Clean Docker development environment

### Testing

The project supports two testing approaches:

1. **Local Testing**:
   ```bash
   invoke test
   ```
   - Runs against localhost PostgreSQL
   - Faster for development
   - Requires local PostgreSQL

2. **Docker Testing**:
   ```bash
   invoke docker.test
   ```
   - Runs in isolated containers
   - Matches production environment
   - No local dependencies needed
   - Used in CI/CD pipeline

### Continuous Integration

The project uses GitHub Actions for CI/CD with the following workflow:

1. **Code Quality**:
   - Dependency security review
   - Code formatting check
   - Linting
   - Static type checking

2. **Testing**:
   - Unit and integration tests
   - Coverage reporting
   - Both local and Docker-based tests

3. **Security**:
   - CodeQL analysis
   - Container scanning
   - Dependency scanning

4. **Deployment**:
   - Multi-arch Docker builds
   - Automatic version tagging
   - Container registry publishing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
