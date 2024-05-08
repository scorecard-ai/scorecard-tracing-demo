import openai

from environment.openai_config import OpenAiConfig
from environment.scorecard_config import ScorecardConfig
from environment.validate import validate_environment
from helper import setup

validate_environment()
openai_config = OpenAiConfig()
scorecard_config = ScorecardConfig()

tracer = setup(name="demo-application", scorecard_config=scorecard_config, debug=True)
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
