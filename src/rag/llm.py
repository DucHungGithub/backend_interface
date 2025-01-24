from typing import List
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

class LLMModel:
    def __init__(self, provider) -> None:
        provider = provider.lower()
        if provider not in ['openai', 'google']:
            raise ValueError("Provider must be either 'openai' or 'google'")
        self.provider = provider
    
    def get_model(self):
        if self.provider == 'openai':
            llm_model = ChatOpenAI(
                model_name="gpt-4o-mini", 
                temperature=0.3
            )
        elif self.provider == 'google':
            llm_model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0,
            )
        else:
            llm_model = None    
            
        return llm_model
    
    
