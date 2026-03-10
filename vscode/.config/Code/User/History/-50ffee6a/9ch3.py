import json
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key="sk-beef09a69abd4d5e85645c77045d0d42",
    base_url="https://ai.tordjman-family.org/api",
)

MODEL = "qwen3.5:9b"


class ChatRequest(BaseModel):
    messages: list
    thinking: bool = False


def generate_stream(messages: list, thinking: bool):
    system_msg = {"role": "system", "content": "/think" if thinking else "/no_think"}
    full_messages = [system_msg] + messages

    t_start = time.perf_counter()
    t_first = None

    stream = client.chat.completions.create(
        model=MODEL,
        messages=full_messages,
        stream=True,
    )

    buf = ""
    in_think = False
    think_done = False
    first_token = True

    for chunk in stream:
        token = chunk.choices[0].delta.content or ""
        if not token:
            continue

        if first_token:
            t_first = time.perf_counter()
            first_token = False

        buf += token

        while True:
            if not in_think and not think_done:
                idx = buf.find("<think>")
                if idx != -1:
                    before = buf[:idx]
                    if before:
                        yield f"data: {json.dumps({'type': 'token', 'content': before})}\n\n"
                    buf = buf[idx + len("<think>"):]
                    in_think = True
                    yield f"data: {json.dumps({'type': 'think_start'})}\n\n"
                    continue
                else:
                    safe = len(buf) - len("<think>") + 1
                    if safe > 0:
                        out = buf[:safe]
                        if out:
                            yield f"data: {json.dumps({'type': 'token', 'content': out})}\n\n"
                        buf = buf[safe:]
                    break

            elif in_think:
                idx = buf.find("</think>")
                if idx != -1:
                    buf = buf[idx + len("</think>"):]
                    in_think = False
                    think_done = True
                    yield f"data: {json.dumps({'type': 'think_end'})}\n\n"
                    continue
                else:
                    safe = len(buf) - len("</think>") + 1
                    buf = buf[max(0, safe):]
                    break

            else:
                if buf:
                    yield f"data: {json.dumps({'type': 'token', 'content': buf})}\n\n"
                    buf = ""
                break

    if buf and not in_think:
        yield f"data: {json.dumps({'type': 'token', 'content': buf})}\n\n"

    t_end = time.perf_counter()
    ttft = round(t_first - t_start, 2) if t_first else None
    total = round(t_end - t_start, 2)
    yield f"data: {json.dumps({'type': 'done', 'ttft': ttft, 'total': total})}\n\n"


@app.post("/api/chat")
async def chat(req: ChatRequest):
    return StreamingResponse(
        generate_stream(req.messages, req.thinking),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
