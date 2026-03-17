from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


interrupt = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='❌Закрыть', callback_data='close_')]
    ]
)


cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='❌Отменить', callback_data='cancel_')]
    ]
)