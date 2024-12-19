import asyncio
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from create_bot import bot, dp
from data_access_layer.database import initialize_db
from handlers import all_handlers

async def set_commands(bot: Bot):
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='menu', description='Главное меню')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def initialize_on_startup():
    await set_commands(bot)
    await initialize_db()


async def main():
    dp.include_router(all_handlers.router)
    dp.startup.register(initialize_on_startup)
    #dp.shutdown.register()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    # initialize db
    asyncio.run(main())