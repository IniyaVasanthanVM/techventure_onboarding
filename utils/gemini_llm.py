import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gemini_prompt(prompt_text):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt_text)
    return response.text