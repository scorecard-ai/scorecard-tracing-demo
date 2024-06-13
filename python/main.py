import openai
from scorecard.client import Scorecard
from scorecard.telemetry import setup

from environment.openai_config import OpenAiConfig
from environment.scorecard_config import ScorecardConfig
from environment.validate import validate_environment

validate_environment()
openai_config = OpenAiConfig()
scorecard_config = ScorecardConfig()

tracer = setup(name="demo-application", scorecard_config=scorecard_config, debug=True)
openai_client = openai.OpenAI(api_key=openai_config.api_key)

scorecard_client = Scorecard()


@tracer.start_as_current_span("call_llm")
def call_llm(content: str):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
        max_tokens=100,
    )
    print(f"> {content}\n{response.choices[0].message.content}\n")


@tracer.start_as_current_span("create_embedding")
def create_embedding(embedding: str):
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002", input=embedding
    )
    print(f"> {embedding}\n{response.data[0].embedding}\n")


@tracer.start_as_current_span("main")
def main():
    try:
        scorecard_client.run.get(1)
    except:
        pass

    create_embedding("Scorecard identifies the problems you didn't know you had.")
    call_llm("Write a haiku.")
    call_llm("Write an acrostic for the word Scorecard.")
    call_llm("Write a limerick.")


if __name__ == "__main__":
    main()
