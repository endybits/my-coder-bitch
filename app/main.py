import json
import os

from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.middleware.cors import CORSMiddleware

from app.utils.ui_html import htmlUI
from app.utils.ai_utils import thread_coder_assistant
# api_key = os.getenv("OPENAI_API_KEY")

class UserMessage(BaseModel):
    message: str


app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    # return {
    #     "user": user_message.message,
    #     "assistant": coder_assistant_response
    #     }
    return JSONResponse(content=coder_assistant_response, status_code=200)


@app.websocket("/api/v1/assistant/thread")
async def websocket_thread_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            json_payload: dict = json.loads(data)
            print(json_payload)
            thread_id = json_payload.get("thread_id") if json_payload.get("thread_id") else None
            assistant_id = json_payload.get("assistant_id") if json_payload.get("assistant_id") else None
            user_message = json_payload.get("message") if json_payload.get("message") else None
            thread_ai_response = await thread_coder_assistant(
                thread_id=thread_id,
                assistant_id=assistant_id,
                user_message=user_message
            )
            await websocket.send_text(json.dumps(thread_ai_response))
    except WebSocketDisconnect:
        await websocket.close()
    except WebSocketException:
        await websocket.close()
    finally:
        await websocket.close()