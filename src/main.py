from dotenv import load_dotenv
load_dotenv(".env")
import socket

import os
import json
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from langchain_core.documents import Document

from type import *
from rag import VectorDatebase, LLMModel, RAG, Embedding
from web_search.example_magentic_one_helper import get_answer, DOWNLOAD_DIR

# Load environment variables from the .env file
app_state = {
    "vector_db": None,
    "rag": None,
}

# ------------------- FastAPI ----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    embedding = Embedding("google").get_emebedding()
    vector_db = VectorDatebase(embedding=embedding)
    llm = LLMModel("google").get_model()
    retriever = vector_db.get_retriever(search_kwargs={"k": 10, "score_threshold": 0.4})
    
    # Initialize RAG
    rag = RAG(llm=llm, retriever=retriever)
    
    # Store in app state
    app_state["vector_db"] = vector_db
    app_state["rag"] = rag
    
    print("Successfully initialized database and RAG system")
    yield
    print("Cleaning up...")
            
    # Clean up vector database connection if it exists
    if "vector_db" in app_state and hasattr(app_state["vector_db"], "client"):
        try:
            app_state["vector_db"].client.close()
            print("Successfully closed database connection")
        except Exception as e:
            print(f"Error closing database connection: {e}")
    # print("Setting up...")
    # llm = LLMModel("google").get_model()
    # embedding = Embedding("google").get_emebedding()
    # retriever = VectorDatebase(embedding=embedding).get_retriever()
    # RAG.initialize(llm=llm, retriever=retriever)
    # yield
    
    # print("Cleaning up...")


app = FastAPI(
    title=os.environ.get("APP_NAME", "RAG API"),
    version=os.environ.get("APP_VERSION", "0.1.0"),
    description=os.environ.get("APP_DESCRIPTION", "RAG API"),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ------------------- Routes ----------------------------

@app.post("/completion")
async def workflow_response(request: InputQA):    
    docs = app_state["rag"].retrieve_docs(request.query)
    print("docs: ", len(docs))
    print(docs)
    
    #logic
    if len(docs) == 0:
        # use web search
        
        
        note = f"""
        Please try to download the ComfyUI workflow file to do {request.query} on the website OpenArt or Civitai orComfyUIWorkflow (not access to the reddit). Then MUST click the download button to download to the {DOWNLOAD_DIR} folder.
        After download the file, please check the download file exists in local computer.
        If the model is not found, please stop and return the `Can not find the workflow` message. Otherwise, return the path to the downloaded workflow json file.
        If you file the path but it is the zip, please extract it to the {DOWNLOAD_DIR} folder, then countinue to find the path of workflow json file.
        If you think you are not able to find the workflow, please stop and return the `Can not find the workflow` message.
        """
        
    
    
        answer = await get_answer(note, start_page="https://www.google.com.vn/")
        
        llm = LLMModel("openai").get_model().with_structured_output(SearchWorkflow)
        s_w = llm.invoke([
            {
                "role": "system",
                "content": """
                    Given the context of a workflow download, extract the following details in JSON format:
                        name: The name of the downloaded workflow.
                        description: A detailed description of the workflow, including all its properties and features.
                        path: The file path where the downloaded workflow is stored.
                        
                    Ensure that the JSON output is complete and accurate based on the provided context.
                """
            },
            {
                "role": "user",
                "content": request.query + "\n" + answer
            }
        ])
        
        
        
        
        try:
            print("------@@@@@@-------")
            print(s_w)
            with open(s_w.path, 'r') as f:
                metadata = json.load(f)
                print("---------")
                print(metadata)
                
                # doc_metadata = {
                #     "name": metadata["name"],
                #     "description": metadata["description"],
                #     "workflow_json": json.dumps(metadata),
                #     "number_reviews": 1,
                #     "workflow_like": 100,
                #     "workflow_view": 10000,
                #     "workflow_download": 1000,
                #     "workflow_comment": 1,
                # }
                # doc = Document(
                #     page_content=metadata["description"],
                #     metadata=doc_metadata,
                # )
                # app_state["vector_db"].add_document(doc)
                return {"num": 1, "data": [Workflow(name=s_w.name, description=s_w.description, metadata=metadata)]}
        
        except FileNotFoundError:
            print(f"Error: File not found at {s_w.path}")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON content in {s_w.path}")
        except AttributeError:
            print("Error: 's_w' object has no attribute 'path'")
        except:
            return {"num": 0, "data": []}
  
        
    else:
        # refined_docs = app_state["rag"].refine(docs, limit=5)
        refined_docs = docs[:3]
        print(len(refined_docs))
        response = app_state["rag"].generation(refined_docs)
        print(len(response))
        print(response)
        if len(refined_docs) != len(response):
            raise ValueError("The number of refined documents and the number of responses do not match.")
        
        num = len(response)
        print("num: ", num)
        data = []

        for i in range(num):
            
            workflow = {
                "name": refined_docs[i].metadata["name"],
                "description": response[i],
                "metadata": json.loads(refined_docs[i].metadata["workflow_json"]),
            }
            data.append(workflow)

        return {"num": num, "data": data}

    return {"num": 0, "data": []}

@app.post("/test")
async def test(request: str):
    from web_search.example_magentic_one_helper import get_answer
    
    answer = await get_answer(request)
    
    return {"message": answer}
# # ------------------- Run the server ---------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
