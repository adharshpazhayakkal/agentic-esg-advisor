import os
import requests
import google.generativeai as genai

LLM_MODE = os.getenv("LLM_MODE", "gemini")

# -------- Gemini --------
def call_gemini(prompt):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

# -------- Mistral (Hugging Face) --------
def call_mistral(prompt):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]["generated_text"]

# -------- Unified interface --------
def call_llm(prompt):
    if LLM_MODE == "gemini":
        return call_gemini(prompt)
    elif LLM_MODE == "mistral":
        return call_mistral(prompt)
    else:
        raise ValueError("Invalid LLM_MODE")
