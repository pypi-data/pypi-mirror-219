import sys

import openai
from gpt.util import get_token_amount_from_string


def openai_request(prompt: str, model: str, temperature: float):
    TOKEN_LIMIT = 6500
    if get_token_amount_from_string(prompt) > TOKEN_LIMIT:
        print(f"Token amount of {get_token_amount_from_string(prompt)} is to big. Stay below {TOKEN_LIMIT}!")
        return
    response = openai.ChatCompletion.create(
        model=model,
        temperature=temperature,
        stream=True,
        messages=[
            {"role": "system",
             "content": "Help answer user questions, provide solutions step by step."},
            {"role": "user", "content": prompt}
        ]
    )

    return response


def print_streamed_response(response):
    # create variables to collect the stream of events
    collected_events = []
    # iterate through the stream of events
    for event in response:
        collected_events.append(event)  # save the event response
        if event['choices'][0]['delta'].get('content') is not None:
            event_text = event['choices'][0]['delta']['content']  # extract the text
            sys.stdout.write(event_text)
            sys.stdout.flush()  # ensures output is displayed immediately
