# import weaviate
# from langchain_weaviate.vectorstores import WeaviateVectorStore

# weaviate_client = weaviate.connect_to_local(
#     host="weaviate",  # Use a string to specify the host
#     port=8080,
#     grpc_port=50051,
# )
# # db = WeaviateVectorStore.from_documents(docs, embeddings, client=weaviate_client)
# if weaviate_client.is_ready():
#     print("Successfully connected to local Weaviate!")
# else:
#     print("Failed to connect to local Weaviate.")

# # Optional: Print the Weaviate version
# print(f"Weaviate version: {weaviate_client.get_meta()['version']}")



# import json

# with open("data/workflow_json/(flux)Turn your photo to clay style(照片转黏土风格flux版）.json", 'r', encoding='utf-8') as file:
#     mock_json = json.load(file)

# from langchain.schema import Document

# doc = Document(
#         page_content=mock_json["description"],
#         metadata=mock_json,
#     )

# db = WeaviateVectorStore.from_documents([doc], client=weaviate_client)





# weaviate_client.close()
import os
# from dotenv import load_dotenv


# load_dotenv(".env")

from rag.vector_store import VectorDatebase
from rag.embedding import Embedding
from rag.loader import Loader

embedding = Embedding("google").get_emebedding()
db = VectorDatebase(embedding=embedding)

data = [os.path.join("local_workflows", p) for p in os.listdir("local_workflows")]
print(data)



l = Loader()

docs = l.load(data)
    

# for doc in docs:
#     print(doc.metadata["name"], "\n\n")
db.add_documents(docs)