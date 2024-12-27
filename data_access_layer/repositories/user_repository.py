from models.user import UserEntity, UserDTO
from data_access_layer.database import get_db_session
from sqlalchemy import select

class UserRepository:

    @staticmethod
    async def create(user: UserDTO):
        new_user = UserEntity(**user.model_dump())
        async with get_db_session() as session:
            session.add(new_user)
            await session.commit()

    @staticmethod
    def update(user: UserDTO):
        raise NotImplementedError()

    @staticmethod
    def delete(user: UserDTO):
        raise NotImplementedError()

    @staticmethod
    async def find(tg_id: int):
        query = select(UserEntity).where(UserEntity.telegram_id == tg_id)
        async with get_db_session() as session:
            result = await session.execute(query)
            result = result.scalar()
            if result is not None:
                return UserDTO.model_validate(result, from_attributes=True)
            else:
                return None

    @staticmethod
    async def is_user_exists(tg_id: int) -> bool:
        is_exists = False if not await UserRepository.find(tg_id) else True
        return is_exists
