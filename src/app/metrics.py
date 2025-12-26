from prometheus_client import Counter, Histogram
from fastapi import FastAPI

# Define Prometheus metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

errors_total = Counter(
    'errors_total',
    'Total errors encountered',
    ['error_type', 'endpoint']
)

def setup_metrics(app: FastAPI):
    """
    Setup Prometheus metrics endpoint for FastAPI app.
    """
    try:
        from prometheus_client import make_asgi_app
        app.mount("/metrics", make_asgi_app())
    except ImportError:
        pass  # Prometheus client not installed, skip metrics endpoint
