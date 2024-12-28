from aiogram.fsm.state import StatesGroup, State

class AppStates(StatesGroup):
    adds_new_measure = State()
    delete_notification = State()
    choice_notification_type = State()
    choice_notification_time = State()
    choice_notification_interval = State()