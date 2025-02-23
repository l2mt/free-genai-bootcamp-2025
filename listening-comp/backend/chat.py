from openai import OpenAI
import streamlit as st
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

MODEL_ID = "gpt-4o-mini"
DEFAULT_INFERENCE_CONFIG = {"temperature": 0.6}

class OpenAIChat:
    def __init__(self, model_id: str = MODEL_ID):
        """Inicializa el cliente de chat de OpenAI."""
        self.model_id = model_id
        self.client = OpenAI()


    def generate_response(self, message: str, inference_config: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Genera una respuesta usando el endpoint ChatCompletion."""
        config = inference_config if inference_config is not None else DEFAULT_INFERENCE_CONFIG

        try:
            response = self.client.chat.completions.create(

                model=self.model_id,
                messages=[{"role": "user", "content": message}],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"Error generating response: {e}")
            return None

def main():
    chat = OpenAIChat()
    while True:
        user_input = input("You: ")
        if user_input.lower() == '/exit':
            break
        response = chat.generate_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    main()
