from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.utils import validators

from app.data.weather_data_process import format_weather

from app.services.get_lat_and_lon import get_coordinates
from app.services.request_weather import get_weather

from app.states.weather_states import (EditUserLoc, SetUserLoc, 
                                       UserData, WeatherPagination)

from app.keyboards import reply, fabrics, inline

import app.database.requests as rq


router = Router()


@router.message(F.text == '❌Закрыть')
async def close_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ввод отменён", reply_markup=reply.rmk) 


@router.message(UserData.address)
async def set_address(message: Message, state: FSMContext):
    address = message.text.strip()
    error = validators.validate_address(address)

    if error:
        await message.answer(error)
        return 
    
    await state.update_data(address=message.text)
    await state.set_state(UserData.forecast)
    await message.answer("Выберите, какую погоду вывести.\nИспользуйте клавиатуру ниже. ⛅", 
                         reply_markup=reply.weather_full)


@router.message(UserData.forecast)
async def set_forecast(message: Message, state: FSMContext):
    user_input = message.text.strip().lower()
    error = validators.validate_weather_type(user_input)

    if error:
        await message.answer(error)
        return 

    await state.update_data(forecast=user_input)

    if user_input in ['текущая', '🟢текущая']:
        data = await state.get_data()
        await state.clear()

        coordinates = await get_coordinates(data['address'])
        weather_data = await get_weather(coordinates)
        weather_text = format_weather(weather_data, data['forecast'])
        await message.answer(weather_text, reply_markup=reply.rmk)

    else:
        await state.set_state(UserData.days)
        await message.answer("Последний шаг: укажите, на сколько дней нужен прогноз (максимум 7).", 
                             reply_markup=reply.amount_days)  


@router.message(UserData.days)
async def set_time(message: Message, state: FSMContext):
    user_days = message.text.strip()
    error = validators.validate_days(user_days)

    if error:
        await message.answer(error)
        return

    await state.update_data(days=int(user_days))
    data = await state.get_data()
    await state.clear()

    coordinates = await get_coordinates(data['address'])
    weather_data = await get_weather(coordinates, days=data['days'])
    weather_text = format_weather(weather_data, data['forecast'], data['days']) 
    
    if isinstance(weather_text, str):
        await message.answer(weather_text, reply_markup=reply.rmk)
    else:
        if data['days'] == 1:
            await message.answer(weather_text[0], reply_markup=inline.interrupt)
            return
        await state.set_state(WeatherPagination.viewing)
        await state.set_data({'pages': weather_text})
        await message.answer(weather_text[0], reply_markup=fabrics.paginator(page=0))


@router.message(F.text.casefold().in_(['✏️изменить', '🗑️удалить', 'изменить', 'удалить']), EditUserLoc.edit_loc)
async def edit_location(message: Message, state: FSMContext):
    edit = message.text.lower()

    if edit in ['✏️изменить', 'изменить']:
        await message.answer("Введите страну/город/адрес 🏙️", reply_markup=inline.cancel)
        await state.set_state(SetUserLoc.location)
    elif edit in ['🗑️удалить', 'удалить']:
        await rq.delete_location(message.from_user.id)
        await message.answer("Ваша локация была удалена.")
        await state.clear()


@router.message(SetUserLoc.location)
async def set_location(message: Message, state: FSMContext):
    location = message.text.strip()
    error = validators.validate_address(location)

    if error:
        await message.answer(error)
        return
    
    await state.update_data(location=location)
    data = await state.get_data()
    await state.clear()

    await rq.save_location(message.from_user.id, data['location'])
    await message.answer("Ваша локация была сохранена.✅")


@router.message()
async def interrupt_pagination(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == WeatherPagination.viewing.state:
        await state.clear()