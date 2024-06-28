from enum import Enum
import json
from typing import Annotated, List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from functions.auth import get_current_user, get_password_hash
from pydantic import BaseModel,EmailStr
from schemas.schemas import ChatData, Contexts, Inputs, Outputs, User
from datetime import datetime
from fastapi import status
from functions.auth import authenticate_user, create_access_token
from datetime import timedelta

from functions.password_reset import generate_otp, get_saved_otp_from_database, send_email


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.agents import load_tools, initialize_agent, Tool
from langchain_core.output_parsers import StrOutputParser




import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyDSgKtXIi2b7ZaW-nBRI-dL6Yz9zgNN4ok"
router = APIRouter()

memory = ConversationBufferMemory(return_messages=True)

class Tags(Enum):
    user = "User CRUD Routes"
    user_auth = "User Authentication Routes"
    password_reset = "Password Reset Routes"
    chatbot = "Chatbot Routes"



class CreateUserRequest(BaseModel):
    firstname: str
    secondname: str
    email: EmailStr
    password: str
    age: int
    address: str
    gender: str

class LoginData(BaseModel):
    email: EmailStr
    password: str

class UpdateUserRequest(BaseModel):
    firstname: str
    secondname: str
    email: EmailStr
    age: int
    address: str
    gender: str
    
    

@router.post("/users/create", tags=[Tags.user])
async def create_user(request_data: CreateUserRequest):
    try:
        # Check if a user with the same email already exists
        
        existing_user = User.objects(email=request_data.email).first()
        
        
        if existing_user:
            print("User with this email already exists")
            return HTTPException(status_code=400, detail="User with this email already exists")
        else:
            # Hash the user's password
            hashed_password = get_password_hash(request_data.password)

            # Create a new user
            new_user = User(
                firstname = request_data.firstname,
                secondname = request_data.secondname,
                email = request_data.email,
                password = hashed_password,  
                age = request_data.age,
                address = request_data.address,
                gender = request_data.gender,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )

            new_user.save()

            return {"message": "User created successfully", "user_id": str(new_user.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/users/me", tags=[Tags.user])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return json.loads(current_user.to_json())

    
@router.put("/users/me/update", tags=[Tags.user])
async def update_user_info(
    update_data: UpdateUserRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        

        # Update user information based on the provided data
        current_user.update(**update_data.model_dump(exclude_unset=True))
        current_user.updatedAt = datetime.now()
        current_user.save()

        

        return {"message": "User information updated successfully", "user_id": str(current_user.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.delete("/users/me/delete", tags=[Tags.user])
async def delete_current_user(current_user: User = Depends(get_current_user)):
    try:
        
        # Delete the current user from the database
        current_user.delete()
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token", tags=[Tags.user_auth])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




class RequestData(BaseModel):
    email: EmailStr
    

class otpVerifyData(BaseModel):
    email: EmailStr
    otp: str

 


class newPasswordSave(BaseModel):
    otp: str
    email: EmailStr
    newPassword: str

@router.post("/password_reset/request", tags=[Tags.password_reset])
def request_password_reset(request_data: RequestData):
    email = request_data.email
    print(f"Received request with email: {email}")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=404, detail="User with specified email not found")

    otp = generate_otp()
    user.otp = otp 
    user.save()  

    message = f"Your OTP for password reset is: {otp}"
    send_email(email, message)

    return json.loads(user.to_json())




@router.post("/password_reset/verify", tags=[Tags.password_reset])
def verify_otp(request_data: newPasswordSave):

    otp = request_data.otp

    # Retrieve the saved OTP from your database or cache for verification
    saved_otp = get_saved_otp_from_database(request_data.email)

    if otp == saved_otp:
        otp = "NULL"
        user = User.objects.get(email=request_data.email)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid User")
        user.otp = otp
        new_password = request_data.newPassword
        user.password = get_password_hash(new_password)
        user.save()
        newly_saved_user = json.loads(user.to_json())
        return {"Updated User": newly_saved_user,"Message": "OTP Verified"}

    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    


class ContextItem(BaseModel):
    input: str
    output: str

class SaveContextsRequest(BaseModel):
    contexts: List[ContextItem]

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
    

class AddContextItem(BaseModel):
    input: str
    output: str

@router.post("/users/me/chat/{chat_id}/add_context", tags=[Tags.chatbot])
async def add_context_to_chat(chat_id: str, context: AddContextItem, current_user: User = Depends(get_current_user)):
    try:
        # Find the specific chat by ID
        chat = next((chat for chat in current_user.chat_data if str(chat.id) == chat_id), None)
        
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        # Add the new context to the chat
        new_context = Contexts(inputs=Inputs(input=context.input), outputs=Outputs(output=context.output))
        chat.contexts.append(new_context)
        current_user.updatedAt = datetime.now()
        current_user.save()

        return {"message": "Context added successfully"}
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
    

class ChatInput(BaseModel):
    chat_input: str


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
    
    
 
@router.get("/users/report/{chat_id}", tags=[Tags.chatbot])
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

        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.8)
        
        # Convert the response to a string
        response_str = json.dumps(response)
        
        problem_prompt = ChatPromptTemplate.from_template('''Hallo. You are a mental health specialist and well versed to understand the problem. Now I had a recent conversation with a therapist. I was giving the input and therapist was output. Following are our full conversation: {conversation}
Now based on this conversation do you find any underlying mental health issues in me''')
        
        tools = load_tools(["wikipedia"])
        
        chain_place = problem_prompt | llm | StrOutputParser()
        
        problems = chain_place.invoke({"conversation": response_str})
        
        # Convert response to string for concatenation
        response_str_for_solution = json.dumps(response)
        solution_prompt = f"As a mental health specialist, what are some possible solutions for the following problems? {response_str_for_solution}"

        agent = initialize_agent(
            tools,
            llm,
            agent="zero-shot-react-description",
            verbose=True,
            handle_parsing_errors=True
        )
        
        solutions = agent.invoke({"input": solution_prompt})
        
        chat.digon = problems
        chat.improvements = solutions["output"]
        
        current_user.updatedAt = datetime.now()
        current_user.save()   

        response_to_return = {
            "problems_found": problems,
            "solutions_found": solutions["output"]
        }
        return response_to_return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))