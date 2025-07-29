from pydantic import BaseModel
from typing import Dict, List
from uuid import UUID

class FilterCreate(BaseModel):
    filters: Dict[str, List[str]]
    
class FilterOut(FilterCreate):
    user_id: UUID
    
    class Config:
        from_attributes = True