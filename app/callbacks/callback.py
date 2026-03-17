from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data == 'close_')
async def interrupt_command(query: CallbackQuery, state: FSMContext):
    await query.answer("Просмотр погоды завершён ✅")
    await query.message.delete()
    await state.clear()


@router.callback_query(F.data == 'cancel_')
async def cancel_action(query: CallbackQuery, state: FSMContext):
    await query.answer("Операция отменена")
    await query.message.delete()
    await state.clear()