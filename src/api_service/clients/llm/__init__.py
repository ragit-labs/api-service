from typing import List

from groq import Groq
from openai import OpenAI
from openai.types import Embedding
from typing_extensions import Required, TypedDict


class LLMMessage(TypedDict):
    content: Required[str]
    role: Required[str]


async def invoke_groq(messages: List[dict], model_name: str, model_params: dict, response_mode="text"):
    groq_client = Groq(
        api_key="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"
    )
    chat_completion = groq_client.chat.completions.create(
        messages=messages,
        model=model_name,
        temperature=model_params.get("temperature", 0.5),
        max_tokens=model_params.get("max_tokens", 1024),
        top_p=model_params.get("top_p", 1),
        frequency_penalty=model_params.get("frequency_penalty", 0),
        presence_penalty=model_params.get("presence_penalty", 0),
        response_format={"type": response_mode}
    )

    return chat_completion.choices[0].message.content


async def invoke_openai(messages: List[dict], model_name: str, model_params: dict, response_mode="text"):
    openai_client = OpenAI(
        api_key="sk-proj-FMnd5Ng5LlgMjqQwi2kqT3BlbkFJOR5D7bmsro9YrjqFdOwu"
    )
    chat_completion = openai_client.chat.completions.create(
        messages=messages,
        model=model_name,  # type: ignore
        temperature=model_params.get("temperature", 0.5),
        max_tokens=model_params.get("max_tokens", 1024),
        top_p=model_params.get("top_p", 1),
        frequency_penalty=model_params.get("frequency_penalty", 0),
        presence_penalty=model_params.get("presence_penalty", 0),
        response_format={"type": response_mode}
    )

    return chat_completion.choices[0].message.content


async def generate_openai_embeddings(docs: List[str], model="text-embedding-3-small") -> List[Embedding]:
    openai_client = OpenAI(
        api_key="sk-proj-FMnd5Ng5LlgMjqQwi2kqT3BlbkFJOR5D7bmsro9YrjqFdOwu"
    )
    texts = []
    for doc in docs:
        if doc.replace("\n", " ").strip() == "":
            continue
        texts.append(doc.replace("\n", " "))
    return openai_client.embeddings.create(input=texts, model=model).data
