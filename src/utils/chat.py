import json
import logging
import re

from openai import AsyncOpenAI

from configs.env import NEBIUS_API_KEY
from services.memory_service import memory_client


def remove_discord_tags(text: str) -> str:
    pattern = r"<[@#&]\d+>"
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text.strip()


logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    base_url="https://api.studio.nebius.com/v1/", api_key=NEBIUS_API_KEY
)

with open("CHATBOT_PROMPT.txt", "r") as file:
    SYSTEM_PROMPT = file.read()

CONTEXT_PROMPT = """
    Context: 
    {context}
"""


async def chatbot(query: str, uid: int, username: str, ctx: str = None):
    query = remove_discord_tags(query)
    try:
        relevant_context = memory_client.search(query=query, user_id=str(uid))
    except Exception as exc:
        logger.warning("Memory search failed: %s", exc)
        relevant_context = {"results": []}

    if not relevant_context.get("results"):
        context = "No previous context available."
    else:
        context = [
            f"ID: {ctx.get('id')}, Context: {ctx.get('memory')}"
            for ctx in relevant_context.get("results")
        ]
    if ctx:
        print("CTX: ", ctx)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": CONTEXT_PROMPT.format(context=context)},
            {"role": "assistant", "content": ctx},
            {"role": "user", "content": query},
        ]
    else:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": CONTEXT_PROMPT.format(context=context)},
            {"role": "user", "content": query},
        ]

    response = await client.chat.completions.create(
        model="openai/gpt-oss-20b",
        response_format={"type": "json_object"},
        messages=messages,
    )

    reply = response.choices[0].message.content
    parsed_response = json.loads(reply)

    try:
        memory_client.add(
            messages=[
                {"role": "user", "content": query},
                {"role": "assistant", "content": reply},
            ],
            user_id=str(uid),
            metadata={
                "username": username,
                "query": query,
                "response": parsed_response.get("content"),
            },
        )
    except Exception as exc:
        logger.warning("Memory add failed: %s", exc)

    return parsed_response.get("content")
