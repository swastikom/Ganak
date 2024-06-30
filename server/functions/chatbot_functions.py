
from langchain.memory import ConversationBufferMemory


from functions.auth import get_current_user
from models.chats_model import ChatInput

import os
api_key = os.environ.get("GEMINI_API_KEY")

memory = ConversationBufferMemory(return_messages=True)

def delete_chat_memory():
   memory.clear()