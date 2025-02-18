from src.models.base import Base
from pydantic import BaseModel
from sqlalchemy.orm import mapped_column, Mapped

class UserDTO(BaseModel):
    id: int | None = None
    telegram_id: int

class UserEntity(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column()