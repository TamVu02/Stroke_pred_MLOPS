import os
from fastapi import FastAPI, Request
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from prometheus_client import start_http_server, Summary, Counter, Gauge
import time
from .main import app

# Tracing with Jaeger via OTLP
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "fastapi-stroke-pred-service"}))
)

otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv("JAEGER_URI", "http://host.docker.internal:4318/v1/traces"),  # Jaeger OTLP endpoint
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument FastAPI app
FastAPIInstrumentor.instrument_app(app)

# Prometheus metrics
# Expose Prometheus metrics on http://localhost:8001
start_http_server(8001, addr=os.getenv("METRICS_URI", "0.0.0.0"))

REQUEST_TIME = Summary("request_duration_seconds", "Time spent processing request")
REQUEST_COUNTER = Counter("http_requests_total", "Total HTTP requests")

@app.middleware("http")
async def metrics_middleware(request, call_next):
    REQUEST_COUNTER.inc()
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    REQUEST_TIME.observe(duration)
    return response