# Scorecard Tracing Demo

This repository contains sample code for integrating with Scorecard's tracing.

## Development

If you wish to extend a demo application in this monorepo, get started by cloning this repository and opening the workspace in VS Code.

```sh
git clone https://github.com/scorecard-ai/scorecard-tracing-demo
code demo.code-workspace
```

Each individual project is self-contained and has a `.vscode/launch.json` file that will execute the demo successfully.

Configuration should be placed in `scorecard-tracing-demo/python/.env` and `scorecard-tracing-demo/node/.env`:

```sh
OPENAI_API_KEY=
SCORECARD_API_KEY=
SCORECARD_TELEMETRY_KEY=
SCORECARD_TELEMETRY_URL=https://telemetry.getscorecard.ai:4318
```

### Python

If you want to develop against a local version of the Scorecard Python SDK:

```sh
cd scorecard-tracing-demo/python
poetry install --no-root
poetry add --editable /path/to/scorecard-python --extras "telemetry instrument-openai"
```

### Node.js

If you want to develop against a local version of the Scorecard Node.js SDK:

```sh
cd scorecard-node
rm scorecard-ai-*.tgz

# Uses Yarn 1
yarn
yarn build
yarn pack
```

```sh
cd scorecard-tracing-demo/node
pnpm install
pnpm install /path/to/scorecard-node/scorecard-ai-*.tgz
```

Since the SDK needs to be transpiled prior to publishing there is presently no way to live link this and the process must be repeated in each test cycle.