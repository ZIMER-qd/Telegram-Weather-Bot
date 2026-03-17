from aiohttp import ClientError

from constants import API_URL
import app.services.sessions as session_module

import logging
import json
import asyncio

async def get_weather(coordinates: dict, timezone: bool = None, days: int = 1) -> dict | tuple[dict, str]:
    """
    Retrieves weather data from the API for the given coordinates.

    Args:
        coordinates (dict): A dictionary with coordinates {'lat': float, 'lon': float}.
        timezone (bool, optional): If True, returns a tuple (weather data, timezone string). 
                                   Defaults to None.
        days (int, optional): Number of days for the forecast. Defaults to 1.

    Returns:
        dict | tuple[dict, str]:
            - dict: If timezone=None, returns a dictionary with weather data.
            - tuple[dict, str]: If timezone=True, returns a tuple
              (dictionary with weather data, timezone string).
            Returns an empty dictionary or tuple if the request fails or no data is available.
    """
    if not coordinates:
        return {}
    
    params = {
        'latitude': coordinates['lat'],
        'longitude': coordinates['lon'],
        'current': 'temperature_2m,precipitation,cloud_cover,wind_speed_10m,wind_direction_10m',
        'hourly': 'temperature_2m,precipitation,cloud_cover,wind_speed_10m,wind_direction_10m',
        'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,wind_direction_10m_dominant',
        'timezone': 'auto',
        'forecast_days': days,
    }
    try:
        async with session_module.session.get(API_URL, params=params, timeout=10) as response:
            if 200 <= response.status < 300:
                data = await response.json()
                if timezone:
                    data_timezone = data['timezone']
                    return (data, data_timezone) if data else ()
                return data if data else {}
            else:
                logging.warning(f"Request failed with status {response.status}")
                return {}
    except (ClientError, asyncio.TimeoutError, json.JSONDecodeError) as e:
        logging.warning(f"Request failed in file services/request_weather.py: {e}")
        return {}