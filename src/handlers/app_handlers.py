from aiogram import F, Router, types
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.keyboards.reply_kbs import main_kb, get_keyboard_binds, get_keyboard_by_message
from src.utils.checkers import sanitize_string

router = Router()

@router.message(Command('menu'))
async def show_menu(message: types.Message):
    await message.answer(text='Главное меню', reply_markup=main_kb(message.from_user.id))

@router.message(lambda msg: any(substr in msg.text for substr in get_keyboard_binds().keys()))
async def show_keyboard(message: types.Message):
    response_text = sanitize_string(message.text).strip()
    keyboard = get_keyboard_by_message(response_text)

    add_args = [message.from_user.id] if 'главное меню' in response_text.lower() else []
    await message.answer(text=response_text, reply_markup=keyboard(*add_args))

@router.message(F.text.contains('Отмена'))
async def cancel_action(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Ввод информации отменён", reply_markup=ReplyKeyboardRemove())


@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji=DiceEmoji.BOWLING)
