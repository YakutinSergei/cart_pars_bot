from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from bot_menu import menu
from create_bot import bot
from database.orm import check_premium



router: Router = Router()

'''FSM для Парсинг по последней активновти'''
class ParsingActive(StatesGroup):
    waiting_link = State()
    last_activity = State()

'''FSM для парсинга телефонов'''
class ParsingPhones(StatesGroup):
    waiting_link = State()


'''Парсинг по активности'''
@router.callback_query(Text(text='parsing_activity'))
async def parsing_activity_start(callback_query: CallbackQuery, state: FSMContext):
    text = 'Отправьте ссылку на чат'
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
    await state.set_state(ParsingActive.waiting_link)


'''Парсинг по активности. Выбор времени'''
@router.message(StateFilter(ParsingActive.waiting_link))
async def get_private_report(message: Message, state: FSMContext):
    await state.update_data(waiting_link=message.text)
    inline_markup = await menu.last_active_menu()
    text = 'За какой промежуток времени пользователи должны были быть онлайн?'
    await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')
    await state.set_state(ParsingActive.last_activity)


'''Парсинг номеров телефонов'''
@router.callback_query(Text(text='phones'))
async def parsing_phones(callback_query: CallbackQuery, state: FSMContext):
    text = 'Отправьте ссылку на чат'
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
    await state.set_state(ParsingPhones.waiting_link)


'''Премиум меню'''
@router.callback_query(Text(text='premium_menu'))
async def get_premium_menu(callback_query:CallbackQuery):
    premium_status = await check_premium(callback_query.from_user.id)
    if premium_status == 1:
        text = 'Выберите необходимый вариант из списка'
        inline_markup = await menu.premium_parsing_menu()
        await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')
    else:
        text = 'Данная функция доступна только премиум пользователям'
        await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
