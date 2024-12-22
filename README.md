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
│   │   └── dependencies.py # FastAPI dependencies
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
├── tasks/             # Task management
│   ├── clean.py      # Cleanup tasks
│   ├── docker.py     # Docker management
│   ├── format.py     # Code formatting
│   ├── lint.py       # Code linting
│   └── test.py       # Test tasks
├── scripts/          # Utility scripts
├── Dockerfile       # Container definition
├── docker-compose.yml # Container orchestration
├── alembic.ini     # Alembic configuration
├── pyproject.toml  # Project configuration
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
  - Flake8 (style guide enforcement)
  - MyPy (static type checking)

- **Testing**:
  - pytest for unit and integration tests
  - async test support
  - test coverage reporting
  - fixture-based test data

- **Docker Support**:
  - Multi-stage builds
  - Development and production configurations
  - PostgreSQL service
  - Volume mapping for development

### Task Automation
Invoke-based task system for common operations:
- Code formatting and linting
- Test execution
- Docker container management
- Database operations
- Development workflow automation

## Prerequisites

- Python 3.12+
- Poetry (Python package manager)
- Docker and Docker Compose
- PostgreSQL (via Docker)

## Installation

1. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone the repository and install dependencies:
   ```bash
   cd backend_core
   poetry install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:
   ```bash
   docker compose up -d postgres
   poetry run alembic upgrade head
   ```

## Development Workflow

1. **Setup Environment**:
   ```bash
   poetry install
   poetry shell
   ```

2. **Start Development Server**:
   ```bash
   invoke up
   # API will be available at http://localhost:8000
   # Swagger docs at http://localhost:8000/docs
   ```

3. **Code Changes**:
   - Make your changes
   - Format code: `invoke format`
   - Run linting: `invoke lint`
   - Run tests: `invoke test`

4. **Database Changes**:
   - Modify SQLAlchemy models
   - Generate migration: `alembic revision --autogenerate -m "description"`
   - Apply migration: `alembic upgrade head`

## Available Tasks

All tasks can be run using `poetry run invoke [task-name]` or just `invoke [task-name]` if Poetry's shell is activated.

### Code Quality
```bash
invoke format           # Format code using black, isort, and autoflake
invoke check-format    # Check code formatting without making changes
invoke lint            # Run linting checks (flake8 and mypy)
```

### Testing
```bash
invoke test            # Run test suite
```

### Docker Operations
```bash
invoke build           # Build Docker images
invoke up              # Start Docker containers
invoke down            # Stop Docker containers
invoke logs            # View Docker container logs
```

## API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

### Environment Variables

Key environment variables (defined in `.env`):
```bash
# Server
API_V1_STR=/api/v1
BACKEND_CORS_ORIGINS=["http://localhost:8000"]
PROJECT_NAME=backend_core

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# PostgreSQL
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=app
```

### Tool Configurations

All tool configurations are in `pyproject.toml`:
- **Black**: Line length 120, Python 3.12 target
- **isort**: Black profile, 120 line length
- **Flake8**: 120 line length, E203 ignored
- **MyPy**: Strict type checking enabled

## Code Style Guidelines

- Line length: 120 characters
- Follow PEP 8 style guide
- Type hints are required (enforced by MyPy)
- Docstrings for all public functions and classes
- Import sorting:
  - Standard library
  - Third-party packages
  - Local imports

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
   - Follow code style guidelines
   - Add tests for new features
   - Update documentation
4. Run quality checks:
   ```bash
   invoke format
   invoke lint
   invoke test
   ```
5. Submit pull request

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.