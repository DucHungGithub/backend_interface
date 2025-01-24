from typing import Union, List, Literal
import glob
from tqdm import tqdm
import multiprocessing
import json
from langchain.schema import Document


from utils.text_processing import TextProcessing


def load_json(json_file):
    # Check if the input is a file path
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Ensure that the 'description' key exists in the data
    if "description" not in data:
        raise KeyError("The key 'description' is missing in the JSON data.")
    data["workflow_json"] = json.dumps(data["workflow_json"])
    # Create the Document object
    content = TextProcessing().clean(data["description"])
    doc = Document(
        page_content=content,
        metadata=data,
    )
    return doc

def get_num_cpu():
    return multiprocessing.cpu_count()

class BaseLoader:
    def __init__(self) -> None:
        self.num_workers = get_num_cpu()
    def __call__(self, files: List[str], **kwargs):
        pass
    
class JSONFileLoader(BaseLoader):
    def __init__(self) -> None:
        super().__init__()
    def __call__(self, json_files: List[str], **kwargs):
        num_process_workers = min(kwargs.get("workers", self.num_workers), self.num_workers)
        with multiprocessing.Pool(processes=num_process_workers) as pool:
            doc_loaded = []
            total_files = len(json_files)
            with tqdm(total=total_files, desc="Loading JSONs", unit="file") as pbar:
                for doc in pool.imap_unordered(load_json, json_files):
                    doc_loaded.append(doc)  # append single doc
                    pbar.update(1)
        return doc_loaded
    
class Loader:
    def __init__(self,
                 file_type: str = "json",  # Literal["json"] is not necessary here
                 ) -> None:
        assert file_type in ["json"], f"file_type must be json, not {file_type}"
        self.file_type = file_type
        if self.file_type == "json":
            self.doc_loader = JSONFileLoader()
        else:
            raise ValueError("file_type must be json")
    def load(self, json_files: Union[str, List[str]], workers: int = 1):
        if isinstance(json_files, str):
            json_files = [json_files]
        doc_loaded = self.doc_loader(json_files, workers=workers)
        return doc_loaded
    def load_dir(self, dir_path: str, workers: int = 1):
        if self.file_type == "json":
            files = glob.glob(f"{dir_path}/*.json")
            assert len(files) > 0, f"No {self.file_type} files found in {dir_path}"
        else:
            raise ValueError("file_type must be json")
        return self.load(files, workers=workers)