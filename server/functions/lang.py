import requests

import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("Write 3 ways to control body focused repititive behaviors.")
print(response.text)
