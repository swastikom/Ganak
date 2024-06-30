from enum import Enum
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from schemas.schemas import ChatData, Contexts, Inputs, Outputs, User
from datetime import datetime



from functions.auth import get_current_user
from functions.chatbot_functions import delete_chat_memory, memory
from models.chats_model import ChatInput





router = APIRouter()

class Tags(Enum):
    chatbot = "Chatbot Routes"






@router.post("/users/me/save_contexts", tags=[Tags.chatbot])
async def save_contexts( prompt: ChatInput,current_user: User = Depends(get_current_user)):
        delete_chat_memory()
    
    # try:
        
        output = answer_question_gemini(prompt.chat_input)  # Access the chat_input attribute

        # Convert the request data into embedded documents
        contexts_list = [
            Contexts(inputs=Inputs(input=prompt.chat_input), outputs=Outputs(output=output))
        ]

        # Create new ChatData with the provided digon and contexts
        new_chat_data = ChatData(id=ObjectId(), contexts=contexts_list)

        # Append the new ChatData to the user's chat_data
        current_user.chat_data.append(new_chat_data)
        current_user.updatedAt = datetime.now()
        current_user.save()

        return {"response": output,"message": "Contexts saved successfully", "chat_id": str(new_chat_data.id)}    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/users/new/chat/{chat_id}", tags=[Tags.chatbot])
async def get_chat_response(
    chat_id: str,
    req_body: ChatInput,  # Make sure this is the correct type for request body
    current_user: User = Depends(get_current_user)
):
    try:
        # Find the specific chat by ID
        chat = next((chat for chat in current_user.chat_data if str(chat.id) == chat_id), None)
        
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        # Loop through each context and save it
        for context in chat.contexts:
            memory.save_context({"input": context.inputs.input}, {"output": context.outputs.output})

        # Pass the chat_input attribute to the answer_question_gemini function
        chat_res = answer_question_gemini(req_body.chat_input, str(current_user.age), current_user.gender)  

        # Add the new context to the chat
        new_context = Contexts(inputs=Inputs(input=req_body.chat_input), outputs=Outputs(output=chat_res))
        chat.contexts.append(new_context)
        current_user.updatedAt = datetime.now()
        current_user.save()

        return {"response": chat_res}  # Return response in a dictionary for consistency
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

   


@router.get("/users/me/chats", tags=[Tags.chatbot])
async def get_all_chats(current_user: User = Depends(get_current_user)):
    try:
        # Fetch all chats associated with the current user
        all_chats = [
            {
                "contexts": [
                    {"input": context.inputs.input, "output": context.outputs.output}
                    for context in chat.contexts
                ]
            }
            for chat in current_user.chat_data
        ]

        return all_chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/users/me/chat/{chat_id}", tags=[Tags.chatbot])
async def get_chat_response(chat_id: str, current_user: User = Depends(get_current_user)):
    try:
        # Find the specific chat by ID
        chat = next((chat for chat in current_user.chat_data if str(chat.id) == chat_id), None)
        
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        # Prepare the response in the required format
        response = {
            "contexts": [
                {"input": context.inputs.input, "output": context.outputs.output}
                for context in chat.contexts
            ]
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.delete("/users/me/chat/{chat_id}", tags=[Tags.chatbot])
async def delete_chat(chat_id: str, current_user: User = Depends(get_current_user)):
    try:
        # Find the chat by ID
        chat_to_delete = None
        for chat in current_user.chat_data:
            if str(chat.id) == chat_id:
                chat_to_delete = chat
                break
        
        if not chat_to_delete:
            raise HTTPException(status_code=404, detail="Chat not found")

        # Remove the chat from user's chat_data list and save
        current_user.chat_data.remove(chat_to_delete)
        current_user.save()

        return {"message": f"Chat with ID {chat_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
from functions.second_chat import answer_question_gemini, delete_chat_memory

    


    

