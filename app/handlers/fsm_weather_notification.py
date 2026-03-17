from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.utils import validators

from app.keyboards import reply, inline

from app.states.weather_states import EditNotifyWeather, SetNotificationWeather
from app.services.get_lat_and_lon import get_coordinates
from app.services.request_weather import get_weather

import app.database.requests as rq

router = Router()

@router.message(F.text.casefold().in_(['✏️изменить', '🗑️удалить', 'изменить', 'удалить']), 
                EditNotifyWeather.edit_weather_settings)
async def edit_weather_settings(message: Message, state: FSMContext):
    edit = message.text.lower()

    if edit in ['✏️изменить', 'изменить']:
        await message.answer("Введите страну/город/адрес 🏙️", reply_markup=inline.cancel)
        await state.set_state(SetNotificationWeather.user_time)
    elif edit in ['🗑️удалить', 'удалить']:
        await rq.delete_weather_settings(message.from_user.id)
        await message.answer("Ваша локация была удалена.")
        await state.clear()


@router.message(SetNotificationWeather.user_time)
async def set_user_time(message: Message, state: FSMContext):
    user_time = message.text.strip()
    error = validators.validate_time(user_time)
    
    if error:
        await message.answer(error)
        return
    
    await state.update_data(user_time=user_time)
    await state.set_state(SetNotificationWeather.address)
    await message.answer("Введите страну/город/адрес 🏙️")


@router.message(SetNotificationWeather.address)
async def set_user_address(message: Message, state: FSMContext):
    address = message.text.strip()
    error = validators.validate_address(address)

    if error:
        await message.answer(error)
        return
    if not await get_coordinates(address):
        await message.answer("⛔Такой локации не существует.\nПроверьте коректность ввода.")
        return
    
    await state.update_data(address=address)
    await state.set_state(SetNotificationWeather.forecast)
    await message.answer("Выберите, какую погоду вывести.\nИспользуйте клавиатуру ниже. ⛅",
                         reply_markup=reply.weather_detail) 
    


@router.message(SetNotificationWeather.forecast)
async def set_user_forecast(message: Message, state: FSMContext):
    user_input = message.text.strip().lower()
    error = validators.validate_weather_type(user_input)

    if error:
        await message.answer(error)
        return

    await state.update_data(forecast=user_input)
    data = await state.get_data()
    
    coordinates = await get_coordinates(data['address'])
    _, user_tz = await get_weather(coordinates, timezone=True)

    await rq.save_weather_settings(
        message.from_user.id,
        data['address'],
        data['forecast'],
        data['user_time'],
        user_tz
    )

    await message.answer(f"Сохранение прошло успешно!🎉\nУказаная вами погода будет выводится каждый день в <b>\"{data['user_time']}\"</b>")
    await state.clear()