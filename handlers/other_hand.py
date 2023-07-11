from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
#from lexicon.lexicon_ru import LEXICON_RU

router: Router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])
    await state.set_state(FSMorder.name)