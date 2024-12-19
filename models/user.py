from models.base import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer

class UserDTO(BaseModel):
    id: int | None = None
    telegram_id: int

class UserEntity(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)