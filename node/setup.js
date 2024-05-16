const process = require('process');

const { LangChainInstrumentation } = require('@arizeai/openinference-instrumentation-langchain');
const { OpenAIInstrumentation } = require('@arizeai/openinference-instrumentation-openai');
const { trace } = require('@opentelemetry/api');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { Resource } = require('@opentelemetry/resources');
const { BatchSpanProcessor, ConsoleSpanExporter, NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SEMRESATTRS_SERVICE_NAME } = require('@opentelemetry/semantic-conventions');
const CallbackManagerModule = require('@langchain/core/callbacks/manager');
const OpenAI = require('openai');

module.exports = {
  setup(name, scorecardConfig, debug = false) {
    const resource = Resource.default().merge(
      new Resource({
        [SEMRESATTRS_SERVICE_NAME]: name,
      }),
    );

    const provider = new NodeTracerProvider({
      resource,
    });

    if (debug) {
      const consoleExporter = new ConsoleSpanExporter();
      const processor = new BatchSpanProcessor(consoleExporter);
      provider.addSpanProcessor(processor);
    }

    const url = scorecardConfig.telemetryUrl ? scorecardConfig.telemetryUrl : 'https://telemetry.getscorecard.ai';
    const otlpExporter = new OTLPTraceExporter({
      url: `${url}/v1/traces`,
      headers: {
        'Authorization': `Bearer ${scorecardConfig.telemetryKey}`
      },
    });
    const processor = new BatchSpanProcessor(otlpExporter);
    provider.addSpanProcessor(processor);

    provider.register();

    new LangChainInstrumentation().manuallyInstrument(CallbackManagerModule);  
    new OpenAIInstrumentation().manuallyInstrument(OpenAI);

    const tracer = trace.getTracer();

    process.on('beforeExit', async () => {
      await provider.shutdown();
    });

    return tracer;
  }
};
