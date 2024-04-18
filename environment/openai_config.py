from environment.dotenv import location
from environment.validated_settings import ValidatedSettings, ValidatedString


class OpenAiConfig(ValidatedSettings):
    class Config:
        env_file = location
        env_file_encoding = "utf-8"
        env_prefix = "openai_"
        extra = "ignore"

    api_key: ValidatedString = ""
