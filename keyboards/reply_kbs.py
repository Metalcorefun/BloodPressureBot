from collections import namedtuple


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.config_reader import config

# FUTURE: Rewrite all navigation to callbacks

# В каждом кейборде завести параметр ancestor и занести в коллбэк
# from aiogram.filters.callback_data import CallbackData
# class MenuCallbackData(CallbackData, prefix = 'menu_nav'):
#     action: str = 'back'
#     navigate_to: str
# KeyboardMetadata = namedtuple('KeyboardMetadata', ['message_text', 'func'])
# ..[InlineKeyboardButton(text='Назад', callback_data = MenuCallbackData(navigate_to=ancestor).pack())]

def main_kb(user_telegram_id: int):
    ancestor = '-'
    kb_list = [
        [KeyboardButton(text="📈 Измерения и статистика")],
        [KeyboardButton(text="👤 Мой профиль")]
    ]
    if user_telegram_id == config.admin_id:
        kb_list.append([KeyboardButton(text="⚙️ Админка")])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )

def measures_kb(**kwargs):
    ancestor = 'main_menu'
    kb_list = [
        [KeyboardButton(text="➕ Добавить измерение")],
        [KeyboardButton(text="(TBD) Выгрузить историю")],
        [KeyboardButton(text='↩️ Главное меню')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )

def profile_kb(**kwargs):
    ancestor = 'main_menu'
    kb_list = [
        [KeyboardButton(text="ℹ️ Общая информация")],
        [KeyboardButton(text="(TBD) Оповещения (TBD)")],
        [KeyboardButton(text='↩️ Главное меню')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )

def cancel_kb():
    kb_list = [
        [KeyboardButton(text='❌ Отмена')]
    ]
    return ReplyKeyboardMarkup(
            keyboard=kb_list,
            resize_keyboard=True,
            one_time_keyboard=True
        )

def get_keyboard_binds():
    keyboard_binds = {
        'Главное меню': main_kb,
        'Измерения и статистика': measures_kb,
        'Мой профиль': profile_kb
    }
    return keyboard_binds

def get_keyboard_by_message(key):
    return get_keyboard_binds().get(key)
