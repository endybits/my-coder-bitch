import os

from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.utils.ui_html import htmlUI
from app.utils.ai_utils import thread_coder_assistant
# api_key = os.getenv("OPENAI_API_KEY")

class UserMessage(BaseModel):
    message: str


app = FastAPI()

@app.get("/")
def read_root():
    # print(api_key)
    return HTMLResponse(content=htmlUI(), status_code=200)

@app.post("/api/v1/assistant")
async def coder_assistant(
    user_message: UserMessage
):
    coder_assistant_response: dict = await thread_coder_assistant(user_message=user_message.message)
    print(coder_assistant_response)
    return {
        "user": user_message.message,
        "assistant": coder_assistant_response
        }