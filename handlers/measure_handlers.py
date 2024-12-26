from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from pydantic_core import ValidationError

from data_access_layer.repositories.user_repository import UserRepository
from data_access_layer.repositories.measure_repository import MeasureRepository
from keyboards.reply_kbs import cancel_kb
from handlers.app_states import AppStates
from models.measure import MeasureDTO

from utils.checkers import parse_measure
from utils.serializers import to_csv_bytes

measure_router = Router()

async def add_new_measure(measure, user_id):
    user = await UserRepository.find_by_tg_id(user_id)
    measure = MeasureDTO(user_id=user.id, pressure_sys=measure[0], pressure_dia=measure[1])
    await MeasureRepository.create(measure)

@measure_router.message(F.text.contains('Добавить измерение'))
async def activate_new_measure(message: types.Message, state: FSMContext):
    await state.set_state(AppStates.adds_new_measure)
    await message.answer(text='Введите данные в формате {SYS}:{DIA}', reply_markup=cancel_kb())

@measure_router.message(AppStates.adds_new_measure, F.text)
async def handle_new_measure(message: types.Message, state: FSMContext):
    try:
        measure = parse_measure(message.text)
        await add_new_measure(measure, message.from_user.id)
        await state.clear()
        await message.answer(text=f'Ваше давление - {measure[0]} на {measure[1]}')
    except (ValueError, ValidationError) as error:
        await message.answer(text='Упс, кажется, что-то пошло не так. Попробуйте ещё.')

@measure_router.message(F.text.contains('Выгрузить историю'))
async def download_measures(message: types.Message):
    user_id = message.from_user.id
    user = await UserRepository.find_by_tg_id(user_id)

    results = await MeasureRepository.get_by_user_id(user.id)
    results_as_dicts = [item.model_dump(exclude={'id', 'user_id'}) for item in results]
    csv_bytes = to_csv_bytes(results_as_dicts)

    await message.answer(text='Выгружена история измерений на текущий момент:')
    await message.answer_document(BufferedInputFile(file=csv_bytes, filename='measures.csv'))