from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class Embedding:
    def __init__(self, provider) -> None:
        provider = provider.lower()
        if provider not in ['openai', 'google']:
            raise ValueError("Provider must be either 'openai' or 'google'")
        self.provider = provider
    
    def get_emebedding(self):
        if self.provider == 'openai':
            return OpenAIEmbeddings(model="text-embedding-3-small")
        if self.provider == 'google':
            return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        return None
