import glob
from os.path import dirname, join

from environment.openai_config import OpenAiConfig
from environment.scorecard_config import ScorecardConfig


def validate_environment() -> None:
    configs: list[type] = [
        ScorecardConfig,
        OpenAiConfig,
    ]

    # Make sure that all config types are enumerated.
    count = len(glob.glob(join(dirname(__file__), "*_config.py")))

    if len(configs) != count:
        raise ValueError("All configurations not included in validation.")

    errors = []
    for config in configs:
        try:
            config()
        except Exception as e:
            errors.append(e)

    if len(errors) > 0:
        raise ExceptionGroup("Environment Configuration Errors", errors)
