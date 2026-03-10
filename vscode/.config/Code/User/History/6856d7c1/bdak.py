from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(
    api_key="sk-beef09a69abd4d5e85645c77045d0d42",
    base_url="https://ai.tordjman-family.org/api",
)

class CalendarEvent(BaseModel):
    event_name: str
    date: str
    participants: list[str]
    ai_model_name: str

response = client.beta.chat.completions.parse(
    model="qwen3.5:9b",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday. you are qwen3.5:9b",
        },
    ],
    response_format=CalendarEvent,
)

message = response.choices[0].message
print(getattr(message, "reasoning_content", None))
print(message.parsed)
