from pydantic import BaseModel
from typing import Dict, List

class FilterCreate(BaseModel):
    filters: Dict[str, List[str]]
    
class FilterOut(FilterCreate):
    user_id: str
    
    class Config:
        from_attributes = True