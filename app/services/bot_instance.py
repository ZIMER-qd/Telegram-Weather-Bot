from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from config import config

bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))