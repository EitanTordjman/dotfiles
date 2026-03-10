from openai import OpenAI

# Configure to point at any OpenAI-compatible endpoint
client = OpenAI(
    api_key="sk-beef09a69abd4d5e85645c77045d0d42",       # replace with your key (or set OPENAI_API_KEY env var)
    base_url="https://ai.tordjman-family.org/api",  # replace with your endpoint
)

def chat(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    reply = chat("Say hello in one sentence.")
    print(reply)
