from aiogram import Bot

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz

import app.database.requests as rq

from app.services.get_lat_and_lon import get_coordinates
from app.services.request_weather import get_weather
from app.data.weather_data_process import format_weather


scheduler = AsyncIOScheduler()

async def check_weather(bot: Bot) -> None:
    """
    Check if the user should receive a weather notification.

    Args:
        bot (Bot): Instance of the Telegram bot used to send messages.
    
    Returns:
        None: This function does not return anything.
    """
    users = await rq.get_all_weather_settings()
    now_utc = datetime.now(pytz.UTC)

    for user in users:
        if not user.address or not user.forecast_type or not user.user_timezone or not user.notify_time:
            continue

        user_tz = pytz.timezone(user.user_timezone)
        now_user = now_utc.astimezone(user_tz)
        if now_user.strftime('%H:%M') == user.notify_time:
            coordinates = await get_coordinates(user.address)
            weather_data = await get_weather(coordinates)
            weather_text = format_weather(weather_data, user.forecast_type)
            await bot.send_message(user.tg_id, weather_text if isinstance(weather_text, str) else weather_text[0])


def start_scheduler(bot: Bot) -> None:
    """
    Starts the weather notification scheduler.

    This function sets up an interval job that runs every minute to check
    whether users should receive a weather notification, and then starts
    the scheduler.

    Args:
        bot (Bot): Instance of the Telegram bot used to send messages.

    Returns:
        None: This function does not return any value.
    """
    scheduler.add_job(check_weather, 'interval', minutes=1, args=[bot])
    scheduler.start()