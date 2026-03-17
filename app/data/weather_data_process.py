from datetime import datetime
from app.data.select_direction_name import select_direction

import locale
from platform import system


system_name = system()

if system_name == 'Windows':
    locale.setlocale(locale.LC_TIME, "Russian_Russia")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


def format_weather(data: dict, forecast: str, days: int=0) -> str | list[str]:
    """
    Formats weather data from JSON into text for the user.

    Args:
        data (dict): JSON containing weather data.
        forecast (str): Type of forecast selected by the user.
        days (int, optional): Number of days for the forecast. Defaults to 0.

    Returns:
        str | list[str]:
            A string with weather information for the current or brief forecast,
            or a list of strings for hourly/detailed forecasts.
    """
    if not data:
        prompt =  "⛔ Погода по вашей локации не была найдена.\n" \
                  "Проверьте корректно ли вы ввели данные и попробуйте еще раз."

        return prompt
    
    if forecast.lower() in ['текущая', '🟢текущая']:
        return format_current(data)
    elif forecast.lower() in ['краткая', '⚡краткая']:
        return format_daily(data)
    elif forecast.lower() in ['подробная', '📖подробная']:
        return format_hourly(data, days)

def format_current(data: dict) -> str:
    current_weather = data['current']
    
    dt = datetime.strptime(current_weather['time'], "%Y-%m-%dT%H:%M")
    time = dt.strftime("%A, %d %B %Y %H:%M")
    wind_direction = select_direction(current_weather['wind_direction_10m'])
    
    prompt = f"<b>{time}</b> 🗓\n\n" \
             f"🌡️ Температура: {current_weather['temperature_2m']} °C\n" \
             f"☔ Осадки: {current_weather['precipitation']} мм\n" \
             f"☁️ Облачность: {current_weather['cloud_cover']} %\n" \
             f"💨 Ветер: {current_weather['wind_speed_10m']} км/ч, {wind_direction}"

    return prompt


def format_daily(data: dict) -> str:
    prompt = ''
    daily_weather = data['daily']
    times = daily_weather['time']
    max_temp = daily_weather['temperature_2m_max']
    min_temp = daily_weather['temperature_2m_min']
    precipitation = daily_weather['precipitation_sum']
    wind_speed_max = daily_weather['wind_speed_10m_max']
    wind_direction = daily_weather['wind_direction_10m_dominant']

    for i in range(len(times)):
        dt = datetime.strptime(times[i], "%Y-%m-%d").strftime("%A, %d %B %Y")

        prompt += f"<b>{dt}</b> 🗓\n" \
                  "🌡️ Температура:\n" \
                  f"↓ Мин: {min_temp[i]}°C, ↑ Макс: {max_temp[i]}°C\n" \
                  f"☔ Осадки: {precipitation[i]} мм\n" \
                  f"💨 Ветер: {wind_speed_max[i]} км/ч, {select_direction(wind_direction[i])}\n\n"
        
    return prompt

def format_hourly(data: dict, days: int) -> list[str]:
    time_emojis = ['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕',
                   '🕖', '🕗', '🕘', '🕙', '🕚', '🕛', '🕐', 
                   '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', 
                   '🕘', '🕙', '🕚', '🕛']
    hourly_weather = data['hourly']
    times = hourly_weather['time']
    temperature = hourly_weather['temperature_2m']
    precipitation = hourly_weather['precipitation']
    cloud_cover = hourly_weather['cloud_cover']
    wind_speed = hourly_weather['wind_speed_10m']
    wind_direction = hourly_weather['wind_direction_10m']

    prompts = []
    prompt = '' 
    for i in range(len(times)):
        dt = datetime.strptime(times[i], "%Y-%m-%dT%H:%M")

        hour = dt.hour
        emoji = time_emojis[hour]

        date_time = dt.strftime("%H:%M")
        date_line = f"<b>{dt.strftime("%A, %d %B %Y")}</b> 🗓\n" if date_time == '00:00' else ''
        date_line_closing = f"<b>{dt.strftime("%A, %d %B %Y")}</b> 🗓\n" if date_time == '23:00' else ''

        if i != 0 and date_line:
            prompts.append(prompt)
            prompt = ''

        prompt += f"{date_line}<b>- {date_time}</b> {emoji}\n" \
                    f"🌡️ Температура: {temperature[i]} °C\n" \
                    f"☔ Осадки: {precipitation[i]} мм, ☁️ Облачность: {cloud_cover[i]} %\n" \
                    f"💨 Ветер: {wind_speed[i]} км/ч, {select_direction(wind_direction[i])}\n\n" \
                    f"{date_line_closing}"
    
    prompts.append(prompt)

    return prompts