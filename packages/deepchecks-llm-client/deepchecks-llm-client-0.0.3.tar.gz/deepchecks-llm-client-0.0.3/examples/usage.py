import os
import uuid

import coloredlogs
import dotenv
import openai

from deepchecks_llm_client.api import AnnotationType, EnvType
from deepchecks_llm_client.client import dc_client, Tags


def run():
    coloredlogs.install(level='DEBUG')

    dotenv.load_dotenv()

    deepchecks_api_key = os.environ.get("DEEPCHECKS_LLM_API_KEY")
    # auto_collect=True wraps `openai.ChatCompletion` and `openai.Completion` APIs
    # so any OpenAI invocation will fire an event to deepchecks with the relevant data
    dc_client.init(host='http://localhost:8000',
                   api_token=deepchecks_api_key,
                   app_name="ShaysApp",
                   version_name="0.0.1-shay",
                   env_type=EnvType.EVAL,
                   auto_collect=True)

    # Adding context to the call, deepchecks will monitor the context together with any OpenAI's request/response
    dc_client.set_tags({Tags.USER_ID: "A05fdfbb2035e@gmail.com"})

    # Set up your OpenAI API credentials
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", temperature=0.7,
                                                   messages=[{"role": "user", "content": "How much is 2 plus 2?"}])

    # print the chat completion`
    print(chat_completion.choices[0].message.content)

    # Annotating based on openai.id
    dc_client.annotate(chat_completion.openai_id, annotation=AnnotationType.GOOD)


    ### Next Iteration ###
    ######################


    dc_client.set_context(app_name="ShaysApp", version_name="0.0.2-shay", env_type=EnvType.EVAL)

    user_input = "what is the most dominant color of tulips?"
    dc_client.set_tags({Tags.USER_ID: "B05fdfbb2035e@gmail.com",
                        Tags.USER_INPUT: user_input})
    full_input = f"Answering the following question as you were a gardener: {user_input}"
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=full_input,
      temperature=0.5,
      max_tokens=150,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["#", ";"]
    )

    print(response)

    # Annotating based on openai id
    dc_client.annotate(response.openai_id, annotation=AnnotationType.BAD)


if __name__ == "__main__":
    #asyncio.run(run())
    run()
