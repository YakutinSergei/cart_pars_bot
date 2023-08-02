import asyncio
import logging

from aiogram.types import BotCommand

from create_bot import bot, dp
from database import models
from handlers import user_handlers, premium_handlers
from environs import Env

env = Env()
env.read_env()
# Инициализируем логгер
logger = logging.getLogger(__name__)


async def set_default_commands():
    await bot.set_my_commands(
        [
            BotCommand(command='/start', description='Перезапустить бота'),
        ]
    )

async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        filename="botlog.log",
        filemode='a',
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%H:%M:%S',
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    '''Подключаем базу данных'''
    await models.db_connect()


    # Регистриуем роутеры в диспетчере
    dp.include_router(premium_handlers.router)
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

