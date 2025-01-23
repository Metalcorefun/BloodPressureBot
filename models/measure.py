from datetime import datetime

from pydantic import BaseModel, field_validator, Field, ValidationError
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped

from models.base import Base

class MeasureDTO(BaseModel):
    id: int | None = None
    user_id: int
    pressure_sys: int = Field(ge = 0, le = 250)
    pressure_dia: int = Field(ge = 0, le = 250)
    measure_dt: datetime = datetime.now()

    @field_validator('measure_dt')
    @classmethod
    def check_valid_time(cls, value):
        min_dt = datetime(2024, 1, 1, 0, 0, 0)
        current_dt = datetime.now()
        if not (min_dt < value < current_dt):
            raise ValidationError(f'Provided datetime is less than {min_dt.strftime('%d.%m.%Y')}')
        return value

class MeasureEntity(Base):
    __tablename__ = 'measures'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    pressure_sys: Mapped[int] = mapped_column(nullable=False)
    pressure_dia: Mapped[int] = mapped_column(nullable=False)
    measure_dt: Mapped[datetime] = mapped_column(server_default=func.now())