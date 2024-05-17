# Scorecard Tracing Demo - Python

## Quick Start

At the entry point in your application, add these lines of code:

```python
from scorecard.telemetry import setup

tracer = setup(
    name="demo-application",
    scorecard_config={
        "telemetry_url": os.getenv("SCORECARD_TELEMETRY_URL"),
        "telemetry_key": os.getenv("SCORECARD_TELEMETRY_KEY"),
    },
)
```

You can find a complete example with more-complete handling in [`main.py`](main.py).
