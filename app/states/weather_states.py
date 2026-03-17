from aiogram.fsm.state import State, StatesGroup


class UserData(StatesGroup):
    address = State()
    forecast = State()
    days = State()


class WeatherPagination(StatesGroup):
    viewing = State()


class SetUserLoc(StatesGroup):
    location = State()


class EditUserLoc(StatesGroup):
    edit_loc = State()


class SetNotificationWeather(StatesGroup):
    user_time = State()
    address = State()
    forecast = State()
    user_timezone = State()


class EditNotifyWeather(StatesGroup):
    edit_weather_settings = State()