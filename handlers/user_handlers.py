from aiogram import Router, types
from aiogram.filters.command import Command

from data_access_layer.repositories.user_repository import UserRepository
from models.user import UserDTO
from keyboards.reply_kbs import main_kb
from utils.config_reader import config

router = Router()

async def register_user(user_id):
    user = UserDTO(telegram_id=user_id)
    await UserRepository.create(user)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id != config.admin_id:
        await message.answer("Бот на данный момент доступен только для админа.")
        await message.answer("Другим анонимусам придется подождать🤷‍♂️")
    else:
        user_id = message.from_user.id
        if await UserRepository.is_user_exists(user_id):
            message_text = 'Вы уже зарегистрированы и ваши данные уже есть в хранилище бота.'
        else:
            await register_user(user_id)
            message_text = 'Отлично! Теперь вы зарегистрированы в боте'

        await message.answer(text=message_text, reply_markup=main_kb(message.from_user.id))