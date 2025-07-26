from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .movement import Movement