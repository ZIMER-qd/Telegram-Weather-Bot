from app.database.models import async_session
from app.database.models import UserLocation
from sqlalchemy import select

from typing import List


async def set_user(tg_id: int) -> None:
    """
    Adds a user to the database if it does not exist.
    
    Args:
        tg_id (int): User's Telegram ID.
    
    Returns:
        None: This function does not return anything.
    """
    async with async_session() as session:
        user = await session.scalar(select(UserLocation).where(UserLocation.tg_id == tg_id))

        if not user:
            session.add(UserLocation(tg_id=tg_id))
            await session.commit()


async def get_location(tg_id: int) -> str | None:
    """
    Retrieves the user's saved location by their Telegram ID.

    Args:
        tg_id (int): User's Telegram ID.

    Returns:
        str | None: 
            String representation of the user's location if set, otherwise None.
    """
    async with async_session() as session:
        return await session.scalar(select(UserLocation.location).where(UserLocation.tg_id == tg_id))
    

async def save_location(tg_id: int, location: str) -> None:
    """
    Saves the location specified by the user.

    Args:
        tg_id (int): User's Telegram ID.
        location (str): User's location.

    Returns:
        None: This function does not return anything.
    """
    async with async_session() as session:
        async with session.begin():
            result = await session.scalar(select(UserLocation).where(UserLocation.tg_id == tg_id))

            if result:
                result.location = location


async def save_weather_settings(tg_id: int, 
                                location: str, 
                                forecast: str, 
                                notify_time: str, 
                                user_timezone: str) -> None:
    """
    Stores user data for sending weather forecasts
    at the time specified by the user.

    Args:
        tg_id (int): User's Telegram ID.
        location (str): User's location.
        forecast (str): Type of forecast selected by the user.
        notify_time (str): Time to notify the user about the weather, in HH:MM format.
        user_timezone (str): Timezone based on the user's location.

    Returns:
        None: This function does not return anything.
    """
    async with async_session() as session:
        async with session.begin():
            result = await session.scalar(select(UserLocation).where(UserLocation.tg_id == tg_id))
            if result:
                result.address = location
                result.forecast_type = forecast
                result.notify_time = notify_time
                result.user_timezone = user_timezone


async def check_weather_settings(tg_id: int) -> True | False:
    """
    Checks if the user has saved weather settings.

    Args:
        tg_id (int): User's Telegram ID.

    Returns:
        True | False: True if the settings exist, otherwise False.
    """
    async with async_session() as session:
        result = await session.scalar(select(UserLocation.address).where(UserLocation.tg_id == tg_id))
        return True if result else False


async def get_all_weather_settings() -> List[UserLocation]:
    """
    Retrieves all saved settings for all users.

    Args:
        Does not accept arguments.

    Returns:
        List[UserLocation]: A list of UserLocation objects containing
        user data and their weather settings. 
    """
    async with async_session() as session:
        result = await session.execute(select(UserLocation))
        return result.scalars().all()


async def delete_weather_settings(tg_id: int) -> None:
    """
    Deletes user weather settings.

    Args:
        tg_id (int): User's Telegram ID.

    Returns:
        None: This function does not return anything.
    """
    async with async_session() as session:
        async with session.begin():
            result = await session.scalar(select(UserLocation).where(UserLocation.tg_id == tg_id))
            if result:
                result.address = None
                result.forecast_type = None
                result.notify_time = None
                result.user_timezone = None


async def delete_location(tg_id: int) -> None:
    """
    Deleting the specified location by the user.

    Args:
        tg_id (int): User's Telegram ID.
    
    Returns:
        None: This function does not return anything.
    """
    async with async_session() as session:
        async with session.begin():
            result = await session.scalar(select(UserLocation).where(UserLocation.tg_id == tg_id))

            if result:
                await session.delete(result)