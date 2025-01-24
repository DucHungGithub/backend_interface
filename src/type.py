from typing import Any, Dict, List
from pydantic import BaseModel, Field

class Workflow(BaseModel):
    name: str = Field(..., title="Workflow name")
    description: str = Field(..., title="Workflow description")
    metadata: Dict[str, Any] = Field(..., title="Workflow json metadata")
    
class SearchWorkflow(BaseModel):
    name: str = Field(..., title="Workflow name")
    description: str = Field(..., title="Workflow description")
    path: str = Field(..., title="Path to download file of workflow")

class InputQA(BaseModel):
    query: str = Field(..., title="Question to ask the model")

class OutputQA(BaseModel):
    num: int = Field(..., title="Number of workflows returned")
    data: List[Workflow] = Field(..., title="List of workflows")
    
    


# class WorkflowsReponse(BaseModel):
#     workflows: List[Workflow]
    