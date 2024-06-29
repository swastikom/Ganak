import google.generativeai as gena
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()
from langchain_community.llms import Ollama
llm = Ollama(model="gemma2")
llm.invoke("Why is the sky blue?")