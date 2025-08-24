import json
import sqlite3

from openai import AsyncOpenAI

from configs.config import CONFIG
from configs.env import NEBIUS_API_KEY

# DATABASE
conn = sqlite3.connect("databases/chathistory.db")
c = conn.cursor()

c.execute(
    """
    CREATE TABLE IF NOT EXISTS Chat (
    sl_no INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    username TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user','assistant')),
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
"""
)


def save_to_db(query: str, uid: str, username: str, role: str):
    c.execute(
        """
        INSERT INTO Chat (user_id, username, role, content) VALUES (?, ?, ?, ?)
    """,
        (uid, username, role, query),
    )
    conn.commit()


def fetch_context(limit: int = 50):
    c.execute(
        """
        SELECT role, content 
        FROM Chat 
        ORDER BY sl_no DESC 
        LIMIT ?
    """,
        (limit,),
    )

    rows = c.fetchall()

    messages = [{"role": role, "content": content} for role, content in rows[::-1]]

    return messages


client = AsyncOpenAI(
    base_url="https://api.studio.nebius.com/v1/", api_key=NEBIUS_API_KEY
)

with open("CHATBOT_PROMPT.txt", "r") as file:
    SYSTEM_PROMPT = file.read()


async def chatbot(query: str, uid: str, username: str):
    messages = fetch_context(limit=20)
    messages.insert(
        0, {"role": "system", "content": SYSTEM_PROMPT}
    )  # inserts system prompt to the beginning of the list
    messages.append({"role": "user", "content": query})

    save_to_db(query, uid, username, "user")

    response = await client.chat.completions.create(
        model="openai/gpt-oss-20b",
        response_format={"type": "json_object"},
        messages=messages,
    )

    reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": reply})
    save_to_db(query, CONFIG["bot_id"], "Bina", "assistant")

    parsed_response = json.loads(reply)

    return parsed_response.get("content")
