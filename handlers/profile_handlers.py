from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from create_bot import bot
from create_scheduler import scheduler
from data_access_layer.repositories.notifications_repository import NotificationsRepository
from data_access_layer.repositories.user_repository import UserRepository
from keyboards.reply_kbs import cancel_kb
from models.notifications import NotificationDTO
from utils.app_states import AppStates
from utils.transformers import parse_time_hhmm

profile_router = Router()

async def notify_user(user_id):
    await bot.send_message(user_id, 'Пора бы померить давление...')

@profile_router.message(F.text.contains('Общая информация'))
async def show_profile_info(message: types.Message):
    await message.answer(f'Ты {message.from_user.first_name} {message.from_user.last_name}!')
    await message.answer(f'А еще твой id = {message.from_user.id}')

@profile_router.message(F.text.contains('Добавить оповещение'))
async def new_notification(message: types.Message, state: FSMContext):
    await state.update_data(trigger='cron')
    await state.set_state(AppStates.choice_notification_time)
    await message.answer(text='Укажите время ежедневных уведомлений в формате ЧЧ:ММ', reply_markup=cancel_kb())

@profile_router.message(AppStates.choice_notification_time, F.text)
async def handle_new_daily_notification(message: types.Message, state: FSMContext):
    try:
        time_ = parse_time_hhmm(message.text)

        data = await state.get_data()
        data['hour'] = time_.tm_hour
        data['minute'] = time_.tm_min

        await add_new_notification(data, message.from_user.id)
        await state.clear()
        await message.answer(text=f'Принято! Буду оповещать вас ежедневно в {message.text} МСК')

    except (ValueError, ValidationError) as exception:
        await message.answer(text='Введенное время не соответствует формату, введите еще раз.')

async def add_new_notification(parameters, user_id):
    user = await UserRepository.find(user_id)
    notification = NotificationDTO(
        user_id=user.id,
        parameters=parameters,
        apscheduler_job_id=f'notification_{parameters['hour']:02d}{parameters['minute']:02d}_{user.id}'
    )
    scheduler.add_job(
        notify_user,
        trigger=notification.parameters['trigger'],
        hour=notification.parameters['hour'],
        minute=notification.parameters['minute'],
        kwargs = {'user_id': user_id}
    )
    await NotificationsRepository.create(notification)
