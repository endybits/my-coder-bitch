import os

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")



app = FastAPI()

@app.get("/")
def read_root():
    print(api_key)
    return {"Hello": "World"}