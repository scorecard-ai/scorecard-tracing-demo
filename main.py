import openai
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from environment.openai_config import OpenAiConfig
from environment.scorecard_config import ScorecardConfig
from environment.validate import validate_environment

validate_environment()
openai_config = OpenAiConfig()
scorecard_config = ScorecardConfig()

OpenAIInstrumentor().instrument()

provider = TracerProvider(
    resource=Resource(attributes={SERVICE_NAME: "demo-application"})
)
exporter = OTLPSpanExporter(
    endpoint="https://telemetry.getscorecard.ai:4318/v1/traces",
    headers={"Authorization": f"Bearer {scorecard_config.telemetry_key}"},
)

processor = BatchSpanProcessor(span_exporter=exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(instrumenting_module_name=__name__, tracer_provider=provider)

client = openai.OpenAI(api_key=openai_config.api_key)


@tracer.start_as_current_span("call_llm")
def call_llm(content: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
        max_tokens=100,
    )
    print(f"> {content}\n{response.choices[0].message.content}\n")


@tracer.start_as_current_span("main")
def main():
    call_llm("Write a haiku.")
    call_llm("Write an acrostic for the word Scorecard.")
    call_llm("Write a limerick.")


if __name__ == "__main__":
    main()
