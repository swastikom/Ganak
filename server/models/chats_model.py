
from typing import  List
from pydantic import BaseModel



class ContextItem(BaseModel):
    input: str
    output: str

class SaveContextsRequest(BaseModel):
    contexts: List[ContextItem]
    
class AddContextItem(BaseModel):
    input: str
    output: str
    
class ChatInput(BaseModel):
    chat_input: str