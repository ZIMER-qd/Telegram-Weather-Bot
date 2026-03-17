from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from app.keyboards import fabrics


router = Router()


@router.callback_query(fabrics.Pagination.filter(F.action.in_(['prev', 'next'])))
async def weather_pagination(query: CallbackQuery, callback_data: fabrics.Pagination, state: FSMContext):
    
    try:
        data = await state.get_data()
        prompts = data['pages']
    
        page_num = int(callback_data.page)

        if callback_data.action == 'prev':
            page = page_num - 1 if page_num > 0 else 0
        elif callback_data.action == 'next':
            page = page_num + 1 if page_num < (len(prompts) - 1) else page_num

        with suppress(TelegramBadRequest):
            await query.message.edit_text(
                f"{prompts[page]}",
                reply_markup=fabrics.paginator(page)
            )
        await query.answer()
    except KeyError:
        await query.answer("Действие не может быть выполнено, запросите погоду заново")


@router.callback_query(F.data == "pag_close")
async def close_pagination(query: CallbackQuery, state: FSMContext):
    await query.answer("Просмотр погоды завершён ✅")
    await query.message.delete()
    await state.clear()