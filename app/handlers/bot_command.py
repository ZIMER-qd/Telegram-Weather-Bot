from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from app.states.weather_states import (EditNotifyWeather, EditUserLoc, SetNotificationWeather, 
                                       SetUserLoc, UserData)

from app.keyboards import reply, inline

import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await rq.set_user(message.from_user.id)
    
    await state.clear()
    await message.answer("""Здравствуйте! 👋
Это бот, который показывает погоду по любой локации 🌤️
Что он умеет:
- Показывать текущую погоду
- Почасовой прогноз
- Прогноз на неделю
Для справки используйте команду /help""")

@router.message(Command('help'))
async def help(message: Message):
    await message.answer("""Данный бот имеет команды:
- /weather (Можете узнать погоду в введённой вами локации)
- /myloc (Выводит погоду по установленой вами локации. Если локация до этого указана не была попросит установить её)
- /setloc (Может установить или изменить вашу локацию)
- /setime (Команда для установки вывода погоды по задоному вами временем)""")


@router.message(Command('weather'))
async def get_user_address(message: Message, state: FSMContext):
    await state.set_state(UserData.address)
    await message.answer("Введите страну/город/адрес 🏙️", reply_markup=reply.rmk)


@router.message(Command('myloc'))
async def user_location(message: Message, state: FSMContext):
    location = await rq.get_location(message.from_user.id)
    
    if not location:
        await message.answer("Вы пока-что не указали свою локацию.\nВведите команду /setloc")
    else:
        await state.set_state(UserData.address)
        await state.update_data(address=location)
        await state.set_state(UserData.forecast)
        await message.answer("Выберите, какую погоду вывести.\nИспользуйте клавиатуру ниже. ⛅", 
                         reply_markup=reply.weather_full)


@router.message(Command('setloc'))
async def set_or_change_location(message: Message, state: FSMContext):
    location = await rq.get_location(message.from_user.id)

    if location:
        await message.answer("У вас уже указана локация. Вы можете изменить её или удалить.\nВыберите действие ниже.", reply_markup=reply.change)
        await state.set_state(EditUserLoc.edit_loc)
    else:
        await message.answer("Введите страну/город/адрес 🏙️")
        await state.set_state(SetUserLoc.location)


@router.message(Command('setime'))
async def set_notification_weather(message: Message, state: FSMContext):

    if await rq.check_weather_settings(message.from_user.id):
        await state.set_state(EditNotifyWeather.edit_weather_settings)
        await message.answer("У вас уже установлено время.", reply_markup=reply.change)
    else:
        await state.set_state(SetNotificationWeather.user_time)
        await message.answer("""Начнём настройку оповещения.
Введите в какое время вам выводить погоду.
Пример: 8:30""", reply_markup=inline.cancel) 