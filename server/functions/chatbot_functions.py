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
os.environ["GOOGLE_API_KEY"] = "AIzaSyDSgKtXIi2b7ZaW-nBRI-dL6Yz9zgNN4ok"

memory = ConversationBufferMemory(return_messages=True)

def delete_chat_memory():
   memory.clear()