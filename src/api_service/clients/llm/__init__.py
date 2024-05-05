from typing import List

from groq import Groq
from typing_extensions import Required, TypedDict


class LLMMessage(TypedDict):
    content: Required[str]
    role: Required[str]


async def invoke_groq(messages: List[LLMMessage]):
    groq_client = Groq(
        api_key="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"
    )
    groq_model = "llama3-8b-8192"

    chat_completion = groq_client.chat.completions.create(
        messages=messages, model=groq_model  # type: ignore
    )

    return chat_completion.choices[0].message.content
