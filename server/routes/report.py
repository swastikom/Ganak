
from enum import Enum
import json
from fastapi import APIRouter, Depends, HTTPException
from schemas.schemas import User
from datetime import datetime


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import load_tools, initialize_agent
from langchain_core.output_parsers import StrOutputParser
from functions.auth import get_current_user
    
 
router = APIRouter()

class Tags(Enum):
    report = "Report Routes"
 
@router.get("/users/report/{chat_id}", tags=[Tags.report])
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
        
        problem_prompt = ChatPromptTemplate.from_template('''Hallo. You are a mental health specialist and have speciality to make report about  Body-Focused Repetitive Behaviour Disorders like Trichotillomania, Dermatophagia, Onycophagia, and more and well versed to understand the problem. Now I had a recent conversation with a therapist. I was giving the input and therapist was output. Following are our full conversation: {conversation}''')
        
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