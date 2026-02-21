import os
import google.generativeai as genai

# Use your actual key
os.environ["GOOGLE_API_KEY"] = "Your_key_here" 
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("--- Available Models for your API Key ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"ID: {m.name} | Display Name: {m.display_name}")