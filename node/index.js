const { setup } =require('./setup.js');
const OpenAI = require('openai');

// Confirm configuration.
const REQUIRED_ENV_VARS = [
  'OPENAI_API_KEY',
  'SCORECARD_TELEMETRY_KEY',
  'SCORECARD_TELEMETRY_URL',
];
const missingEnvVars = REQUIRED_ENV_VARS.filter((envVariable) => !process.env[envVariable]);
if (missingEnvVars.length > 0) {
  throw new Error(`Missing required environment variables: ${missingEnvVars.join(', ')}`)
}

const tracer = setup('demo-application', {
  telemetryUrl: process.env['SCORECARD_TELEMETRY_URL'],
  telemetryKey: process.env['SCORECARD_TELEMETRY_KEY'],
}, true);

const openai = new OpenAI({
  apiKey: process.env['OPENAI_API_KEY'], // This is the default and can be omitted
});

async function call_llm(content) {
  return tracer.startActiveSpan('call_llm', async (span) => {
    const response = await openai.chat.completions.create({
      messages: [{ role: 'user', content }],
      model: 'gpt-3.5-turbo',
      max_tokens: 100,
    });
  
    console.log(`> ${content}\n${response.choices[0].message.content}\n`);

    span.end();
  });
}

async function main() {
  return tracer.startActiveSpan('main', async (span) => {
    await call_llm('Write a haiku.');
    await call_llm('Write an acrostic for the word Scorecard.');
    await call_llm('Write a limerick.');

    span.end();
  });
}

main();
