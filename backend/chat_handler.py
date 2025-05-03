import os
import openai

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
from backend.model_handler import predict_diabetes


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_chat_response(chat_history):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        temperature=0.7
    )
    return response.choices[0].message.content