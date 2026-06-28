from mistralai import Mistral
from config import Config
import os


def mistral_api(question):
    with Mistral(
        api_key=Config.API_KEY,
    ) as mistral:

        res = mistral.chat.complete(model="mistral-large-latest", messages=[
            {
                "role": "user",
                "content": question,
            },
        ], stream=False, response_format={
            "type": "text",
        })

        # Handle response
        return res.choices[0].message.content


