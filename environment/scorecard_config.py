from environment.dotenv import location
from environment.validated_settings import ValidatedSettings, ValidatedString


class ScorecardConfig(ValidatedSettings):
    class Config:
        env_file = location
        env_file_encoding = "utf-8"
        env_prefix = "scorecard_"
        extra = "ignore"

    telemetry_key: ValidatedString = ""
