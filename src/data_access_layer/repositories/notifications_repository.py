from sqlalchemy import select, delete

from src.models.notifications import NotificationEntity, NotificationDTO
from src.data_access_layer.database import get_db_session

class NotificationsRepository:

    @staticmethod
    async def create(notification: NotificationDTO):
        new_notification = NotificationEntity(**notification.model_dump())
        async with get_db_session() as session:
            session.add(new_notification)
            await session.commit()

    @staticmethod
    async def get_all_by_user_id(user_id: int):
        query = (
            select(NotificationEntity)
            .where(NotificationEntity.user_id == user_id)
            .order_by(NotificationEntity.apscheduler_job_id)
            )
        async with get_db_session() as session:
            results = await session.execute(query)
            return [
                NotificationDTO.model_validate(notification, from_attributes=True)
                for notification in results.scalars().all()
            ]

    @staticmethod
    async def update():
        raise NotImplementedError()

    @staticmethod
    async def find():
        raise NotImplementedError()

    @staticmethod
    async def delete(id: str):
        query = (
            delete(NotificationEntity)
            .where(NotificationEntity.apscheduler_job_id == id)
            .returning(NotificationEntity.apscheduler_job_id)
        )
        async with get_db_session() as session:
            result = await session.execute(query)
            if len(result.fetchall()) != 1:
                raise ValueError('Nothing was deleted by provided id')
            await session.commit()