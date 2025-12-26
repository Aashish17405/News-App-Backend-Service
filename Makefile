.PHONY: install dev lint format test clean run

# Install dependencies
install:
	uv sync

# Install dev dependencies + setup hooks
dev:
	uv sync
	uv run pre-commit install
	@echo "✅ Development environment ready!"

# Run linter
lint:
	uv run ruff check src/

# Auto-fix linting issues
lint-fix:
	uv run ruff check --fix src/

# Format code
format:
	uv run ruff format src/

# Type checking
typecheck:
	uv run mypy src/

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=src --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

# Security check
security:
	uv run bandit -r src/

# Run all checks
check: lint typecheck security test

# Run pre-commit on all files
pre-commit:
	uv run pre-commit run --all-files

# Clean up cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

# Run the application
run:
	uv run uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000

# Run in production mode
prod:
	export ENV_FOR_DYNACONF=production && uv run uvicorn src.app.main:app --host 0.0.0.0 --port 8000