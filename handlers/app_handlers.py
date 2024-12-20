from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji

from keyboards.reply_kbs import main_kb, get_keyboard_binds, get_keyboard_by_message
from utils.checkers import sanitize_string, parse_measure

app_router = Router()

@app_router.message(Command('menu'))
async def show_menu(message: types.Message):
    await message.answer(text='Главное меню', reply_markup=main_kb(message.from_user.id))

@app_router.message(lambda msg: any(substr in msg.text for substr in get_keyboard_binds().keys()))
async def show_keyboard(message: types.Message):
    response_text = sanitize_string(message.text).strip()
    keyboard = get_keyboard_by_message(response_text)

    add_args = [message.from_user.id] if 'главное меню' in response_text.lower() else []
    await message.answer(text=response_text, reply_markup=keyboard(*add_args))

@app_router.message(F.text.contains('Общая информация'))
async def show_profile_info(message: types.Message):
    await message.answer(f'Ты {message.from_user.first_name} {message.from_user.last_name}!')
    await message.answer(f'А еще твой id = {message.from_user.id}')


@app_router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji=DiceEmoji.BOWLING)
