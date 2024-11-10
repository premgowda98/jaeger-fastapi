import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from constants import TRACE_PROVIDER_NAME

# Configure the OpenTelemetry Tracer
def configure_tracer():
    # Set the tracer provider globally
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: TRACE_PROVIDER_NAME})
        )
    )

    # Create the Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=os.getenv('OTEL_EXPORTER_JAEGER_HOST'),  # Jaeger agent host
        agent_port=os.getenv('OTEL_EXPORTER_JAEGER_PORT', 6831)  # Jaeger agent default port
    )

    # Add the Jaeger exporter to the tracer provider
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )

configure_tracer()
RequestsInstrumentor().instrument()