from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from apscheduler.jobstores.base import JobLookupError
from pydantic import ValidationError

from src.create_bot import bot
from src.create_scheduler import scheduler
from src.data_access_layer.repositories.notifications_repository import NotificationsRepository
from src.data_access_layer.repositories.user_repository import UserRepository
from src.keyboards.reply_kbs import cancel_kb
from src.models.notifications import NotificationDTO
from src.utils.app_states import AppStates
from src.utils.transformers import parse_time_hhmm

router = Router()

async def notify_user(user_id):
    await bot.send_message(user_id, 'Пора бы померить давление...')

async def add_new_notification(parameters, user_id):
    user = await UserRepository.find(user_id)
    description = f'Ежедневно в {parameters['hour']}:{parameters['minute']} МСК'
    notification = NotificationDTO(
        user_id=user.id,
        parameters=parameters,
        description=description,
        apscheduler_job_id=f'notification_{parameters['hour']:02d}{parameters['minute']:02d}_{user.id}'
    )
    scheduler.add_job(
        notify_user,
        trigger=notification.parameters['trigger'],
        hour=notification.parameters['hour'],
        minute=notification.parameters['minute'],
        id = notification.apscheduler_job_id,
        kwargs = {'user_id': user_id}
    )
    await NotificationsRepository.create(notification)

@router.message(F.text.contains('Общая информация'))
async def show_profile_info(message: types.Message):
    await message.answer(f'Ты {message.from_user.first_name} {message.from_user.last_name}!')
    await message.answer(f'А еще твой id = {message.from_user.id}')

@router.message(F.text.contains('Добавить оповещение'))
async def new_notification(message: types.Message, state: FSMContext):
    await state.update_data(trigger='cron')
    await state.set_state(AppStates.choice_notification_time)
    await message.answer(text='Укажите время ежедневных уведомлений в формате ЧЧ:ММ', reply_markup=cancel_kb())

#TODO: add timedelta notifications
@router.message(AppStates.choice_notification_time, F.text)
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

@router.message(F.text.contains('Посмотреть текущие оповещения'))
async def show_notifications(message: types.Message):
    user = await UserRepository.find(message.from_user.id)
    results = await NotificationsRepository.get_all_by_user_id(user.id)
    response = (
        f'{'\n'.join([str(result) for result in results])}'
        if len(results) > 0
        else 'На текущий момент у вас не настроено ни одного оповещения'
    )
    await message.answer(text=response)

@router.message(F.text.contains('Убрать оповещение'))
async def initiate_notification_delete(message: types.Message, state: FSMContext):
    await state.set_state(AppStates.delete_notification)
    await message.answer(text='Введите ID оповещения, которое вы хотите удалить.\n'
                              'Его можно посмотреть в списке оповещений', reply_markup=cancel_kb())

@router.message(AppStates.delete_notification, F.text)
async def handle_notification_delete(message: types.Message, state: FSMContext):
    try:
        await NotificationsRepository.delete(message.text)
        scheduler.remove_job(message.text)
        await state.clear()
        await message.answer(text='Оповещение удалено')
    except (JobLookupError, ValueError):
        await message.answer(text='ID оповещения не валиден, попробуйте еще раз.')