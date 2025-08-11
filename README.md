# Flask Calculator - MLOps Demo

A production-ready Flask application demonstrating MLOps best practices including containerization, logging, monitoring, CI/CD, and testing.

## Features

- **Visual Calculator**: Web-based calculator with basic and scientific operations
- **RESTful API**: JSON API endpoints for calculations
- **Structured Logging**: JSON-formatted logs with request tracking
- **Metrics & Monitoring**: Basic metrics collection and health endpoints (candidates should implement monitoring)
- **Containerization**: Multi-stage Docker build with security best practices
- **CI/CD Pipeline**: Automated testing, building, and deployment with GitHub Actions
- **Test Coverage**: Unit and integration tests with coverage reporting

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

3. Access the calculator at http://localhost:8080

### Docker Compose

```bash
docker-compose up
```

This starts the Flask Calculator at http://localhost:8080

## API Endpoints

### Health Check
```bash
GET /health
```

### Metrics
```bash
GET /metrics
```
Returns basic metrics (request counts, duration, uptime). Candidates should implement proper monitoring solution.

### Calculate
```bash
POST /api/calculate
Content-Type: application/json

{
  "operation": "+",
  "a": 5,
  "b": 3
}
```

Supported operations: `+`, `-`, `*`, `/`, `sqrt`, `sin`, `cos`, `tan`, `log`, `ln`

### Evaluate Expression
```bash
POST /api/evaluate
Content-Type: application/json

{
  "expression": "5 + 3"
}
```

## Testing

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

Run linting:
```bash
flake8 app/
black --check app/
```

## Environment Variables

- `FLASK_ENV`: Set to `development` or `production`
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FORMAT`: Log format (`json` or `console`)
- `SECRET_KEY`: Flask secret key
- `METRICS_ENABLED`: Enable/disable metrics endpoint
- `PORT`: Port to run the application (default: 8080)

## Architecture Decisions

### Logging
- Structured logging using `structlog` for better observability
- Request ID tracking for distributed tracing
- JSON format for easy parsing by log aggregators

### Monitoring
- Basic metrics collection (request count, duration, uptime)
- Health check endpoint for container orchestration
- Candidates should implement proper monitoring solution (Prometheus, DataDog, CloudWatch, etc.)

### Security
- Non-root user in Docker container
- Multi-stage build to minimize attack surface
- Security scanning with Trivy in CI/CD
- No hardcoded secrets

### Testing
- Comprehensive unit tests for calculator logic
- Integration tests for API endpoints
- Coverage reporting with pytest-cov
- Automated testing in CI pipeline

## CI/CD Pipeline

The GitHub Actions workflow includes:
1. **Testing**: Unit tests on multiple Python versions
2. **Linting**: Code quality checks with flake8 and black
3. **Security Scanning**: Vulnerability scanning with Trivy
4. **Docker Build**: Multi-platform image building
5. **Deployment**: Staging and production deployment stages

## Deployment

The application is designed for container orchestration platforms:

```yaml
# Example Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-calculator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flask-calculator
  template:
    metadata:
      labels:
        app: flask-calculator
    spec:
      containers:
      - name: calculator
        image: ghcr.io/yourorg/flask-calculator:latest
        ports:
        - containerPort: 8080
        env:
        - name: FLASK_ENV
          value: "production"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
```

## Development

### Project Structure
```
flask-calculator-app/
├── app/
│   ├── __init__.py
│   ├── calculator.py      # Core calculation logic
│   ├── config.py         # Configuration management
│   ├── logging_config.py # Logging setup
│   ├── metrics.py        # Basic metrics collection
│   └── routes.py         # API endpoints
├── static/               # Frontend assets
├── templates/            # HTML templates
├── tests/               # Test suite
├── Dockerfile           # Container definition
├── docker-compose.yml   # Local development stack
└── requirements.txt     # Python dependencies
```

### Adding New Features

1. Implement the logic in `app/calculator.py`
2. Add API endpoint in `app/routes.py`
3. Write tests in `tests/`
4. Update documentation
5. Submit PR with passing CI checks

## License

MIT