from openinference.instrumentation.bedrock import BedrockInstrumentor
from openinference.instrumentation.dspy import DSPyInstrumentor
from openinference.instrumentation.langchain import LangChainInstrumentor
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from openinference.instrumentation.mistralai import MistralAIInstrumentor
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def setup(name, scorecard_config, debug=False):
    BedrockInstrumentor().instrument()
    DSPyInstrumentor().instrument()
    LangChainInstrumentor().instrument()
    LlamaIndexInstrumentor().instrument()
    MistralAIInstrumentor().instrument()
    OpenAIInstrumentor().instrument()

    provider = TracerProvider(resource=Resource(attributes={SERVICE_NAME: name}))

    if debug:
        # Export the trace to the console.
        console_exporter = ConsoleSpanExporter()
        console_processor = BatchSpanProcessor(span_exporter=console_exporter)
        provider.add_span_processor(console_processor)

    # Export the trace to the Scorecard Telemetry server.
    otlp_exporter = OTLPSpanExporter(
        endpoint=f"{scorecard_config.telemetry_url}/v1/traces",
        headers={"Authorization": f"Bearer {scorecard_config.telemetry_key}"},
    )
    otlp_processor = BatchSpanProcessor(span_exporter=otlp_exporter)
    provider.add_span_processor(otlp_processor)

    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(
        instrumenting_module_name=__name__, tracer_provider=provider
    )

    return tracer
