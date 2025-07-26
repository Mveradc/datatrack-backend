from sqlalchemy import Column, Numeric, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.models import Base
from sqlalchemy import ForeignKey
from sqlalchemy import text
import uuid


class Movement(Base):
    __tablename__ = "movements"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    user_id = Column(UUID, ForeignKey("users.id"), index=True)
    concept = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(DateTime, nullable=False)
    balance = Column(Numeric(10, 2), nullable=True)
    agg_concept = Column(String, nullable=True)
    extraordinary = Column(Boolean, default=False)
