# My FastAPI Application

A production-grade FastAPI backend application.

## Prerequisites

- Python 3.11 or higher
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd my-api-project
```

### 2. Install uv (Python Package Manager)

**On macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**On Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, **close and reopen your terminal**.

### 3. Install Dependencies
```bash
# This will automatically create a virtual environment and install all dependencies
uv sync
```

That's it! All dependencies from `pyproject.toml` will be installed automatically.

### 4. Configure Environment (Optional)

The project comes with default development settings. If you need to customize:
```bash
# Copy the example env file (if you create one)
cp .env.example .env

# Edit .env with your preferred settings
```

### 5. Run the Application

**On macOS/Linux:**
```bash
./run.sh
```

**On Windows:**
```batch
run.bat
```

**Or manually:**
```bash
uv run uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the Application

- **API Root:** http://localhost:8000
- **Health Check:** http://localhost:8000/api/v1/health
- **Interactive Docs:** http://localhost:8000/docs
- **API Documentation:** http://localhost:8000/redoc

## Project Structure
```
my-api-project/
├── src/app/           # Application source code
│   ├── main.py        # FastAPI application
│   └── config.py      # Configuration management
├── settings.toml      # Application settings
├── .env               # Environment variables
└── pyproject.toml     # Project dependencies
```

## Development

### Running Tests
```bash
uv run pytest
```

### Code Formatting
```bash
uv run ruff format .
```

### Type Checking
```bash
uv run mypy src/
```

## Troubleshooting

**Issue: "uv: command not found"**
- Make sure you've installed uv and restarted your terminal

**Issue: Port 8000 already in use**
- Change the port in `settings.toml` or run with: `uv run uvicorn src.app.main:app --port 8001`

**Issue: Module not found errors**
- Run `uv sync` to ensure all dependencies are installed

## Support

For issues or questions, please open an issue on GitHub.