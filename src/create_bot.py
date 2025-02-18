import logging
from aiogram import Bot, Dispatcher
from src.utils.config_reader import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()