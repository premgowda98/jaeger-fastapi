from prometheus_client import Counter, Histogram, Summary, Gauge, generate_latest, REGISTRY

# Prometheus metrics
http_request_counter = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'path', 'status_code']
)

request_duration_histogram = Histogram(
    'http_request_duration_seconds',
    'Duration of HTTP requests in seconds',
    ['method', 'path', 'status_code'],
    buckets=[0.1, 0.5, 1, 5, 10]  # Define buckets for histogram
)

request_duration_summary = Summary(
    'http_request_duration_summary_seconds',
    'Summary of the duration of HTTP requests in seconds',
    ['method', 'path', 'status_code'],
)

# Gauge for async task duration
gauge = Gauge(
    'node_gauge_example',
    'Example of a gauge tracking async task duration',
    labelnames=['method', 'status']
)
