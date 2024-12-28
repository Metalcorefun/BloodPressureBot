from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, JSON

from models.base import Base

class NotificationDTO(BaseModel):
    id: int | None = None
    user_id: int
    parameters: dict
    description: str
    apscheduler_job_id: str

    def __str__(self):
        return f'id: {self.apscheduler_job_id} - {self.description}'

class NotificationEntity(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    parameters = Column(JSON, nullable = False)
    description = Column(String, nullable = False)
    apscheduler_job_id = Column(String, nullable=False)