def select_direction(wind_direction: float) -> str:
    """
    Determines the direction of wind in the atmosphere.

    Args:
        wind_direction (float): wind direction in degrees (0-360).

    Returns:
        str: wind direction verbally.
    """
    
    directions = [
        "Северный", "Северо-восточный", "Восточный", "Юго-восточный",
        "Южный", "Юго-западный", "Западный", "Северо-западный"
    ]
    
    index = round(wind_direction / 45) % 8 
    return directions[index]