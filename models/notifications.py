from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, JSON

from models.base import Base

class NotificationDTO(BaseModel):
    id: int | None = None
    user_id: int
    parameters: dict
    apscheduler_job_id: str

class NotificationEntity(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    parameters = Column(JSON, nullable = False)
    apscheduler_job_id = Column(String, nullable=False)