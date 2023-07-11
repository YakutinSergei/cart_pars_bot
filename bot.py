import asyncio
import logging

from aiogram.filters import CommandStart
from aiogram.types import BotCommand, Message, CallbackQuery

from bot_menu import menu
# from handlers import other_handlers, user_handlers, admin_handlers, promo_handkers, arena_handlers, pvp_handlers
from create_bot import bot, dp
# from data_base import postreSQL_bd

# Инициализируем логгер
logger = logging.getLogger(__name__)


# async def set_default_commands(dp):
#     await dp.bot.set_my_commands(
#         [
#             BotCommand('start', 'Перезапустить бота'),
#         ]
#     )

async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    @dp.message(CommandStart())
    async def start_message(message: Message):
        text = f'Привет *{message.from_user.first_name}*!\nВаш ID: {message.from_user.id}\nЯ могу спарсить любой чат\n' \
               f'Выбери необходимое действие👇'
        inline_markup = await menu.main_menu()
        await message.answer(text=text, reply_markup=inline_markup, parse_mode='Markdown')
        #await set_default_commands(dp)

    @dp.callback_query(lambda call: 'main_menu' in call.data)
    async def get_main_menu(callback_query: CallbackQuery):
        text = f'Привет *{callback_query.from_user.first_name}*!\nВаш ID: {callback_query.from_user.id}\nЯ могу спарсить любой чат\n' \
               f'Выбери необходимое действие👇'
        inline_markup = await menu.main_menu()
        await callback_query.message.edit_text(text=text, reply_markup=inline_markup, parse_mode='Markdown')

    # Регистриуем роутеры в диспетчере


    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())