import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import warnings

warnings.filterwarnings("ignore")

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)