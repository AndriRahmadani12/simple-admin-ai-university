from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from openai import OpenAI

API_KEY = "lm-studio"
BASE_URL = "http://localhost:1234/v1"

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    user_messages: str

@app.post("/process_message")
async def process_message(payload: UserMessage):
    try:
        client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
        # Generate completion using OpenAI
        completion = client.chat.completions.create(
            model="model-identifier",
            messages=[
                {"role": "system", "content": "Kamu adalah AI Admin Assistant Universitas Lambung Mangkurat, tolong jawab seramah mungkin"},
                {"role": "user", "content": payload.user_messages},
            ],
            temperature=0.7,
        )
        # Extract response
        response_message = completion.choices[0].message.content
        return {"response": response_message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Run using: uvicorn filename:app --reload
