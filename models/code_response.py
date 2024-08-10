from typing import Any, Dict
from langchain_core.pydantic_v1 import BaseModel,Field


class CodeResponseResult():
    code: str = Field(default=None, description="All the code")
    path: str = Field(default=None, description="The name of path with this format (Views|Controllers|sql)/Name_path.extension")