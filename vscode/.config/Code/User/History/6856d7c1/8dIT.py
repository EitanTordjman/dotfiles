from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(
    api_key="sk-beef09a69abd4d5e85645c77045d0d42",
    base_url="https://ai.tordjman-family.org/api",
    model="qwen3.5:9b"
)

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

response = client.responses.parse(
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text_format=CalendarEvent,
)

event = response.output_parsed