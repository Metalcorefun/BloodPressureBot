from models.measure import MeasureDTO, MeasureEntity
from data_access_layer.database import get_db_session
from sqlalchemy import select, desc


class MeasureRepository:

    @staticmethod
    async def create(measure: MeasureDTO):
        new_measure = MeasureEntity(**measure.model_dump())
        async with get_db_session() as session:
            session.add(new_measure)
            await session.commit()

    @staticmethod
    def update(measure: MeasureDTO):
        raise NotImplementedError()

    @staticmethod
    def delete(measure: MeasureDTO):
        raise NotImplementedError()

    @staticmethod
    async def get_by_user_id(user_id: int):
        query = select(MeasureEntity).where(MeasureEntity.user_id == user_id).order_by(desc(MeasureEntity.measure_dt))
        async with get_db_session() as session:
            results = await session.execute(query)
            # print([measure.__dict__ for measure in results.scalars().all()])
            return [MeasureDTO.model_validate(measure, from_attributes=True) for measure in results.scalars().all()]
