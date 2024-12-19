# As the number of handlers increases, the list will be split into different files


from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from pydantic_core import ValidationError

from data_access_layer.daos.user import UserDAO
from data_access_layer.daos.measure import MeasureDAO
from models.measure import MeasureDTO
from models.user import UserDTO

from handlers.keyboards import main_kb, get_keyboard_binds, get_keyboard_by_message

from utils.config_reader import config
from utils.checkers import sanitize_string, parse_measure

router = Router()

class States(StatesGroup):
    adds_new_measure = State()

async def is_user_exists(tg_id: int) -> bool:
    is_exists = False if not await UserDAO.find_by_tg_id(tg_id) else True
    return is_exists

async def register_user(user_id):
    user = UserDTO(telegram_id=user_id)
    await UserDAO.create(user)

async def add_new_measure(measure, user_id):
    user = await UserDAO.find_by_tg_id(user_id)
    measure = MeasureDTO(user_id=user.id, pressure_sys=measure[0], pressure_dia=measure[1])
    await MeasureDAO.create(measure)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id != config.admin_id:
        await message.answer("Бот на данный момент доступен только для админа.")
        await message.answer("Другим анонимусам придется подождать🤷‍♂️")
    else:
        user_id = message.from_user.id
        if await is_user_exists(user_id):
            message_text = 'Вы уже зарегистрированы и ваши данные уже есть в хранилище бота.'
        else:
            await register_user(user_id)
            message_text = 'Отлично! Теперь вы зарегистрированы в боте'

        await message.answer(text=message_text, reply_markup=main_kb(message.from_user.id))

@router.message(Command('menu'))
async def show_menu(message: types.Message):
    await message.answer(text='Главное меню', reply_markup=main_kb(message.from_user.id))

@router.message(lambda msg: any(substr in msg.text for substr in get_keyboard_binds().keys()))
async def show_keyboard(message: types.Message):
    response_text = sanitize_string(message.text).strip()
    keyboard = get_keyboard_by_message(response_text)

    add_args = [message.from_user.id] if 'главное меню' in response_text.lower() else []
    await message.answer(text=response_text, reply_markup=keyboard(*add_args))

@router.message(F.text.contains('Общая информация'))
async def show_profile_info(message: types.Message):
    await message.answer(f'Ты {message.from_user.first_name} {message.from_user.last_name}!')
    await message.answer(f'А еще твой id = {message.from_user.id}')

@router.message(F.text.contains('Добавить измерение'))
async def activate_new_measure(message: types.Message, state: FSMContext):
    await state.set_state(States.adds_new_measure)
    await message.answer(text='Введите данные в формате {SYS}:{DIA}')

@router.message(States.adds_new_measure, F.text)
async def handle_new_measure(message: types.Message, state: FSMContext):
    try:
        measure = parse_measure(message.text)
        await add_new_measure(measure, message.from_user.id)
        await state.clear()
        await message.answer(text=f'Ваше давление - {measure[0]} на {measure[1]}')
    except (ValueError, ValidationError) as error:
        await message.answer(text='Упс, кажется, что-то пошло не так. Попробуйте ещё.')


@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji=DiceEmoji.BOWLING)
