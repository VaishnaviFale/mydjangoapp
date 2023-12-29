# metrics.py
from prometheus_client import Counter, Histogram

requests_counter = Counter('http_requests_total', 'Total HTTP Requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
