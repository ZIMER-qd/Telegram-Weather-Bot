from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton)

weather_full = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🟢Текущая')], 
        [KeyboardButton(text='📖Подробная'), KeyboardButton(text='⚡Краткая')],
        [KeyboardButton(text='❌Закрыть')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите значение из клавиатуры"
)

weather_detail = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📖Подробная')],
        [KeyboardButton(text='⚡Краткая')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите значение из клавиатуры"
)

mylocation_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🟢Текущая')], 
        [KeyboardButton(text='📖Подробная'), KeyboardButton(text='⚡Краткая')],
        [KeyboardButton(text='✏️Изменить')],
        [KeyboardButton(text='❌Закрыть')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите значение из клавиатуры"
)

amount_days = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='1'), KeyboardButton(text='2'), KeyboardButton(text='3')],
        [KeyboardButton(text='4'), KeyboardButton(text='5'), KeyboardButton(text='6'), KeyboardButton(text='7')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите значение из клавиатуры"
)

change = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✏️Изменить"), KeyboardButton(text="🗑️Удалить")],
        [KeyboardButton(text='❌Закрыть')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите значение из клавиатуры"
)

rmk = ReplyKeyboardRemove()