from typing import List
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_core.documents import Document
import os
from weaviate.embedded import EmbeddedOptions


class VectorDatebase:
    def __init__(self, embedding) -> None:
        self.index_name = "weaviate_comfyui_workflow"
        self.text_key = "embedded_description"
        self.embedding = embedding


        client = weaviate.WeaviateClient(
            embedded_options=EmbeddedOptions(
                additional_env_vars={
                    "ENABLE_MODULES": "backup-filesystem,text2vec-openai,text2vec-cohere,text2vec-huggingface,ref2vec-centroid,generative-openai,qna-openai",
                    "BACKUP_FILESYSTEM_PATH": "./backups"
                }
            )
            # Add additional options here (see Python client docs for syntax)
        )

        client.connect() 
        
        # client = weaviate.connect_to_local(
        #     host=os.environ["WEAVIATE_HOST"],
        # )            
        
        self.vector_store=WeaviateVectorStore(
            client=client,
            index_name=self.index_name,
            text_key=self.text_key,
            embedding=self.embedding,
        )
        
    
    def add_documents(self, documents: List[Document]):
        self.vector_store.add_documents(documents)
        
    
    # def update_documents(self, documents: List[Document]):
    #     self.vector_store.get_by_ids(ids = [])
    #     self.vector_store
    #     ids_to_delete = []
    #     for document in documents:
    #         for idx, doc_id in self.vector_store.():
    #             if self.vector_store.docstore.search(doc_id).page_content == document.page_content:
    #                 ids_to_delete.append(doc_id)
    #                 break
    #     self.vector_store.update_documents(documents)
        
    
    
    def get_retriever(self, search_type: str = "similarity_score_threshold", search_kwargs: dict = {"k": 10, "score_threshold": 0.0}):
        retriever = self.vector_store.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
        return retriever