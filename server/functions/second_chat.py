

import google.generativeai as genai
from dotenv import load_dotenv
import os

from langchain_google_genai import HarmBlockThreshold, HarmCategory

# Load environment variables from .env file
load_dotenv()


api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(model_name='gemini-1.5-pro',generation_config=generation_config,system_instruction="You are Ganak, an AI Assistant built to support individuals suffering Body-Focused Repetitive Behaviour Disorders like Trichotillomania, Dermatophagia, Onycophagia, and more. Your mission is to help those individuals control and reduce their urges gradually in a safe manner, while also helping them get a perspective towards the underlying causes based on their day-to-day schedule, activities and the conversations they have with you. Finally, based on the user's need, you need tomatch users with a suitable medical practioner.")
chat = model.start_chat(history=[])


def answer_question_gemini(question):
    prompt = question
    response = chat.send_message(prompt, stream=True, safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    })
    answer=""
    for chunk in response:
      answer+=chunk.text
      answer = answer.replace('*', '')
    return answer

def delete_chat_memory():
   chat.history.clear()
