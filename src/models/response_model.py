from pydantic import BaseModel
from typing import List, Any, Dict, Optional

class ResponseModel(BaseModel):
    is_success: bool
    message: Optional[str]
    data: Optional[Any]