import re
import os
import json
from typing import List
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from rag.prompt import Prompt


class Str_OutputParser(StrOutputParser):
    def __init__(self) -> None:
        super().__init__()
    def parse(self, text: str) -> str:
        return self.extract_answer(text)
    def extract_answer(self, 
                       text_response: str, 
                       pattern: str = r"Answer:\s*(.*)"
                      ) -> str:
        match = re.search(pattern, text_response, re.DOTALL)
        if match:
            text_response = match.group(1).strip()
        text_response = text_response.split("<SEP>")
        
        return text_response
        

    
class RAG:
    def __init__(self, llm, retriever: VectorStoreRetriever) -> None:
        self.llm = llm
        self.retriever = retriever
        self.str_parser = Str_OutputParser()

    def retrieve_docs(self, query) -> List[Document]:
        return self.retriever.invoke(query)
    
    def generation(self, docs: List[Document]):
        summarize_prompt = PromptTemplate(template=Prompt.SUMMARIZE_RESULTS_PROMPT)

        if not self.llm:
            raise ValueError("The LLM has not been initialized.")
        
        if not self.str_parser:
            raise ValueError("The Str_OutputParser has not been initialized.")

        rag_chain = (
            summarize_prompt |
            self.llm |
            self.str_parser
        )
        response = rag_chain.invoke({"context": self.format_docs(docs)})
        return response

    def format_docs(self, docs):
        formatted_docs = []
        for doc in docs:
            record = f'Workflow name: {doc.metadata["name"]}, description: {doc.metadata["description"]}'
            formatted_docs.append(record)
        return "<SEP>".join(formatted_docs)
    
    def refine(self, docs, limit=5):
        # Sort docs based on the sum of workflow_like and stars * number_reviews in descending order
        sorted_docs = sorted(docs, key=lambda doc: float(doc.metadata['workflow_like']) + float(doc.metadata['stars']) * float(doc.metadata['number_reviews']), reverse=True)
        
        return sorted_docs[:limit]
