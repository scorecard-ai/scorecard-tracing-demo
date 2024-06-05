# Scorecard Tracing Demo - Node

## Usage in CommonJS Applications

At the entry point in your application, add these lines of code:

```js
const { setup } = require('scorecard-ai/telemetry');
const tracer = setup('application-name', {
  telemetryUrl: process.env['SCORECARD_TELEMETRY_URL'],
  telemetryKey: process.env['SCORECARD_TELEMETRY_KEY'],
});
```

You can find a complete example in [`index.cjs`](index.cjs).

## Usage in ES Modules Applications

### Manual Instrumentation of ES Modules Applications

ES Modules specify that imported modules are immutable. This means that every single file which imports `openai` must trigger autoinstrumentation.

If you wish to use ESM, you must manually perform some tasks within your application and cannot rely on them being completed by the helper script:
`npm install --save @arizeai/openinference-instrumentation-openai`

```js
// Extra instrumentation steps that must be performed in every file.
import { OpenAI } from 'openai';
import { OpenAIInstrumentation } from '@arizeai/openinference-instrumentation-openai';
new OpenAIInstrumentation().manuallyInstrument(OpenAI);

// Standard 
import { setup } from 'scorecard-ai/telemetry.js';
const tracer = setup('application-name', {
  telemetryUrl: process.env['SCORECARD_TELEMETRY_URL'],
  telemetryKey: process.env['SCORECARD_TELEMETRY_KEY'],
});
```

You can find a complete example in [`index.mjs`](index.mjs).

### Autoinstrumentation of ES Modules Applications

Existing autoinstrumentation tools for ES Modules (`.mjs`) are not presently compatible with [`openai`](https://www.npmjs.com/package/openai). We are monitoring progress against this. Once this works, the example in [`test.mjs`](test.mjs) application will work.
