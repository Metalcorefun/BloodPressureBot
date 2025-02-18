from typing import Any

from pydantic import BaseModel, Field
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.models.base import Base

class NotificationDTO(BaseModel):
    id: int | None = None
    user_id: int
    parameters: dict
    description: str = Field(max_length=140)
    apscheduler_job_id: str = Field(max_length=50)

    def __str__(self):
        return f'id: {self.apscheduler_job_id} - {self.description}'

class NotificationEntity(Base):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    parameters: Mapped[dict[str, Any]] = mapped_column(nullable = False)
    description: Mapped[str] = mapped_column(String(140), nullable = False)
    apscheduler_job_id: Mapped[str] = mapped_column(String(50), nullable=False)