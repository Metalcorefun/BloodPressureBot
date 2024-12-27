from models.notifications import NotificationEntity, NotificationDTO
from data_access_layer.database import get_db_session

class NotificationsRepository:

    @staticmethod
    async def create(notification: NotificationDTO):
        new_notification = NotificationEntity(**notification.model_dump())
        async with get_db_session() as session:
            session.add(new_notification)
            session.commit()

    @staticmethod
    async def update():
        raise NotImplementedError()

    @staticmethod
    async def find():
        raise NotImplementedError()

    @staticmethod
    async def delete():
        raise NotImplementedError()