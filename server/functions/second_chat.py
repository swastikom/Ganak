

import google.generativeai as genai
from dotenv import load_dotenv
import os

from langchain_google_genai import HarmBlockThreshold, HarmCategory

# Load environment variables from .env file
load_dotenv()

genai.configure(api_key="AIzaSyDSgKtXIi2b7ZaW-nBRI-dL6Yz9zgNN4ok")


model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


def answer_question_gemini(question):
    prompt = "Your name is Ganak. You are a great mental health professional and therapist. You are good at listening and enthusiast about learning about the problems of the person you are chatting with and providing solution. Now the person is telling the following to you: "+question 
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
