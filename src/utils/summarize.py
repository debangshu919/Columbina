import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()


client = AsyncOpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)

with open("SUMMARY_PROMPT.txt", "r") as file:
    SYSTEM_PROMPT = file.read()


async def summarize(context: dict):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": str(context)})

    response = await client.chat.completions.create(
        model="mistralai/Mistral-Nemo-Instruct-2407", messages=messages
    )

    reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": reply})

    return reply
