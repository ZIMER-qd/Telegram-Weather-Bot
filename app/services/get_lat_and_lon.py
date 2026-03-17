from aiohttp import ClientError

from constants import URL
import app.services.sessions as session_module

import logging
import json
import asyncio

async def get_coordinates(location: str) -> dict:
    """
    Gets the coordinates for the location specified by the user from the API.

    Args:
        location (str): User's location.

    Returns:
        dict: A dictionary containing the latitude and longitude of the user's location.
    """

    params = {
        'format': 'json',
        'q': location
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    }
    try:
        async with session_module.session.get(URL, headers=headers, params=params, timeout=10) as response:
            data = await response.json()
            if data:
                if 'lat' in data[0] and 'lon' in data[0]:
                    coordinates = {
                        'lat': data[0]['lat'],
                        'lon': data[0]['lon']
                    }
                    return coordinates
            return {}
    except (ClientError, asyncio.TimeoutError, json.JSONDecodeError) as e:
        logging.warning(f"Request failed in file services/get_lan_and_lon.py: {e}")
        return {}