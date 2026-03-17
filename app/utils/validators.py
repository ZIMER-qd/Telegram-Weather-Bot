def validate_address(location: str) -> str | None:
    """
    Validates the user's location input.

    Args:
        location (str): Location entered by user.

    Returns:
        str | None: Returns an error message if the input is invalid,
                    otherwise None if the input is valid.
    """
    if len(location) > 100:
        return "⛔ Адрес слишком длинный.\nПожалуйста, введите короче (до 100 символов)."
    if location.startswith('/'):
        return "⛔ Адрес не может начинатся с '/'.\nПопробуйте еще раз."
    return None


def validate_weather_type(weather_type: str) -> str | None:
    """
    Validates the user's weather type input.

    Args:
        weather_type (str): Weather type selected by the user.

    Returns:
        str | None: Returns an error message if the input is invalid,
                    otherwise None if the input is valid.
    """
    if weather_type not in ['текущая', 'подробная', 'краткая', '🟢текущая', '📖подробная', '⚡краткая']:
        return "⛔ Вы ввели не коректный тип погоды. 🤔\n" \
               "Попробуйте еще раз.\n" \
               "Используйте клавиатуру ниже. ⛅"
    return None


def validate_days(days: str) -> str | None:
    """
    Validates the user's days input.

    Args:
        days (str): Days selected by the user.

    Returns:
        str | None: Returns an error message if the input is invalid,
                    otherwise None if the input is valid.
    """
    if not days.isdigit() or not (1 <= int(days) <= 7):
        return "Дни должны быть числами от 1 до 7"
    return None


def validate_time(user_time: str) -> str | None:
    """
    Validates the user's time input.

    Args:
        user_time (str): Time selected by user.

    Returns:
        str | None: Returns an error message if the input is invalid,
                    otherwise None if the input is valid.
    """
    user_time_split = user_time.split(':')

    if len(user_time) > 5:
        return"⛔️ Вы ввели некорректное время. Попробуйте ещё раз."
    if len(user_time_split) != 2 or (len(user_time_split[0]) > 2 or len(user_time_split[1]) > 2):
        return "⛔️ Вы ввели некорректное время. Попробуйте ещё раз."
    if not ''.join(user_time_split).isnumeric(): 
        return "⛔️ Вы ввели некорректное время. Попробуйте ещё раз."
    
    try:
        int(''.join(user_time_split))
    except ValueError:
        return "⛔️ Вы ввели некорректное время. Попробуйте ещё раз."
    return None