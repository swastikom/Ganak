from enum import Enum
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from schemas.schemas import ChatData, Contexts, Inputs, Outputs, User
from datetime import datetime


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


from functions.auth import get_current_user
from models.chats_model import ChatInput

import os
api_key = os.environ.get("GEMINI_API_KEY")

memory = ConversationBufferMemory(return_messages=True)

def delete_chat_memory():
   memory.clear()