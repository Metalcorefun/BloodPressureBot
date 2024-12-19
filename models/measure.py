from datetime import datetime
from pydantic import BaseModel, field_validator
from sqlalchemy import Column, Integer, ForeignKey, DateTime

from models.base import Base

class MeasureDTO(BaseModel):
    id: int | None = None
    user_id: int
    pressure_sys: int
    pressure_dia: int
    measure_dt: datetime = datetime.now()

    @field_validator('pressure_sys', 'pressure_dia')
    @classmethod
    def check_in_bounds(cls, value):
        lower_bound = 0
        upper_bound = 250
        if not (lower_bound < value < upper_bound):
            raise ValueError(f'Blood pressure values must be in bound [{lower_bound}:{upper_bound}]')
        return value

    @field_validator('measure_dt')
    @classmethod
    def check_valid_time(cls, value):
        min_dt = datetime(2024, 1, 1, 0, 0, 0)
        current_dt = datetime.now()
        if not (min_dt < value < current_dt):
            raise ValueError('Provided datetime is not valid')
        return value

class MeasureEntity(Base):
    __tablename__ = 'measures'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    pressure_sys = Column(Integer, nullable=False)
    pressure_dia = Column(Integer, nullable=False)
    measure_dt = Column(DateTime, nullable=False)