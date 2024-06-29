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

router = APIRouter()

class Tags(Enum):
    chatbot = "Chatbot Routes"

memory = ConversationBufferMemory(return_messages=True)




@router.post("/users/me/save_contexts", tags=[Tags.chatbot])
async def save_contexts( current_user: User = Depends(get_current_user)):
    memory.clear()
    try:
        prompt = f''' You are a great mental healht therapist. Here's an example of a conversation between a mental health therapist and a student:

Conversation Example
Introduction and Rapport Building
Therapist: Hi, I'm Dr. Smith. How are you feeling today?

Student: Hi, Dr. Smith. I'm okay, I guess. Just a bit overwhelmed.

Therapist: Thank you for coming in today. I understand things can be challenging sometimes. Can you tell me a bit about what's been going on that's making you feel overwhelmed?

Gathering Information
Student: Well, it's just everything piling up. Schoolwork, my part-time job, and things at home aren't great either.

Therapist: That sounds like a lot to handle. Let's break it down a bit. Can you tell me more about the schoolwork and how it's affecting you?

Student: I have so many assignments and exams coming up. I feel like I can't keep up, no matter how hard I try.

Therapist: It sounds very stressful. Have you always felt this way about your schoolwork, or is this a recent development?

Student: It's gotten worse this semester. I used to be able to manage, but now it feels impossible.

Therapist: I see. And you mentioned a part-time job. How is that affecting you?

Student: I work about 20 hours a week. I need the money, but it's exhausting, and I barely have time for anything else.

Identifying Symptoms
Therapist: That does sound exhausting. How are you sleeping?

Student: Not well. I stay up late trying to finish assignments, and even when I do get to bed, I can't fall asleep right away.

Therapist: How about your mood? Have you noticed any changes in how you feel throughout the day?

Student: I've been feeling really down and anxious. Sometimes I feel like I'm on the verge of tears, and I get irritated easily.

Therapist: That must be very difficult for you. Have you been able to talk to anyone about how you're feeling?

Student: Not really. I don't want to burden my friends or family with my problems.

Understanding Context
Therapist: It's understandable to feel that way, but it's important to have support. Can you tell me a bit more about what's going on at home?

Student: My parents are going through a rough patch. They're arguing a lot, and it's really tense at home. I try to stay out of it, but it's hard to ignore.

Therapist: I'm sorry to hear that. It sounds like you're dealing with a lot on multiple fronts. No wonder you're feeling overwhelmed.

Student: Yeah, it's just too much sometimes.

Assessing Severity and Impact
Therapist: Given everything you're dealing with, it’s important to look at how this is impacting you. Have you lost interest in things you used to enjoy?

Student: Definitely. I used to love playing basketball and hanging out with friends, but now I just don't have the energy or desire.

Therapist: Have you had any thoughts about hurting yourself or feeling like you can't go on?

Student: I've had some pretty dark thoughts, especially when things feel really overwhelming. But I haven't acted on them.

Therapist: I'm really glad you shared that with me. It's important we address those feelings. You're not alone in this, and there are ways we can work together to help you feel better.

Developing a Treatment Plan
Therapist: I think it would be helpful for us to meet regularly to talk through these issues. We can work on strategies to manage your stress and improve your mood. How does that sound?

Student: That sounds good. I could use some help figuring all this out.

Therapist: Great. We'll also look into resources that can support you, like academic counseling and possibly adjusting your work schedule if that's feasible. And if you're comfortable, we can involve your family in some sessions to help improve the situation at home.

Student: I think that would be helpful. Thank you.

Therapist: You're welcome. Remember, you're not alone in this, and we're going to work through it together. Let's schedule our next session and take it from there.

This conversation illustrates how a mental health therapist might engage with a person who is in this case a student to understand their issues, gather detailed information, and start developing a plan for support and treatment. 

Now here is a little information about the user you are going to talk with :

Name : {current_user.firstname}
surname : {current_user.secondname}
age: {current_user.age}
gender: {current_user.gender}

'''
        output = "Understood"

        # Convert the request data into embedded documents
        contexts_list = [
            Contexts(inputs=Inputs(input=prompt), outputs=Outputs(output=output))
        ]

        # Create new ChatData with the provided digon and contexts
        new_chat_data = ChatData(id=ObjectId(), contexts=contexts_list)

        # Append the new ChatData to the user's chat_data
        current_user.chat_data.append(new_chat_data)
        current_user.updatedAt = datetime.now()
        current_user.save()

        return {"message": "Contexts saved successfully", "chat_id": str(new_chat_data.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/users/new/chat/{chat_id}", tags=[Tags.chatbot])
async def get_chat_response(
    chat_id: str,
    req_body: ChatInput,
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

        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

        conversation = ConversationChain(
            llm=llm,
            verbose=True,
            memory=memory
        )

        chat_res = conversation.predict(input=req_body.chat_input)

        chat = next((chat for chat in current_user.chat_data if str(chat.id) == chat_id), None)
        
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        # Add the new context to the chat
        new_context = Contexts(inputs=Inputs(input=req_body.chat_input), outputs=Outputs(output=chat_res))
        chat.contexts.append(new_context)
        current_user.updatedAt = datetime.now()
        current_user.save()

        return chat_res
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
    
