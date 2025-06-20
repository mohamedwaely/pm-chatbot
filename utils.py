import os
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()
messages = []

# Configure Gemini API
def setup_openai():
    """
    Setup the Gemini API with the API key from environment variables
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("Gemini API key not found. Please check your .env file.")
    
    genai.configure(api_key=api_key)

def get_openai_response(prompt, system_prompt=SYSTEM_PROMPT):
    try:
        # Create the generation config with safety settings
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Format the prompt with system prompt and current query
        full_prompt = f"{system_prompt}\n\nالمستخدم: {prompt}\n\nالمساعد:"
        
        # Generate the response
        response = model.generate_content(full_prompt)
        return response.text
    
    except Exception as e:
        return f"عذراً، حدث خطأ في الاتصال بنموذج الذكاء الاصطناعي: {str(e)}. يرجى المحاولة مرة أخرى."

def process_direct_question(question):
    """
    Process a direct question from the user, relying on the LLM to infer project type
    
    Args:
        question (str): The user's question
        
    Returns:
        str: The model's response
    """
    return get_openai_response(question)