from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum

class MovementCreate(BaseModel):
    concept: str
    amount: float
    date: datetime
    balance: float
    agg_concept: Optional[str]
    extraordinary: Optional[bool] = False

class MovementOut(MovementCreate):
    id: UUID
    user_id: UUID
    
    class Config:
        from_attributes = True

class Headers(BaseModel):
    date: str = "fecha"
    concept: str = "concepto"
    amount: str = "importe"
    balance: str = "saldo"
