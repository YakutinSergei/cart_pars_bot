import glob
from aiogram import Router
from aiogram.filters import CommandStart, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

from cart_pars import set_default_commands
from bot_menu import menu
from config_data import config
from create_bot import bot
from database.orm import add_user, get_admin
from environs import Env

router: Router = Router()

env = Env()
env.read_env()

client = TelegramClient(env('SESSION_NAME'), env('API_ID'), env('API_HASH'))
client.start()

'''FSM для парсинга открытых групп'''
class ChatOpenLink(StatesGroup):
    waiting_link = State()

'''Получение ссылки на парсинг открытых групп'''
@router.callback_query(Text(startswith='parsing_open_start'))
async def parsing_open_start(callback_query: CallbackQuery, state: FSMContext):
    text = 'Отправьте ссылку на ваш чат в формате *t.mе/durоv* или *@durоv*'
    await bot.send_message(callback_query.from_user.id, text, parse_mode='Markdown')
    await state.set_state(ChatOpenLink.waiting_link)


'''Парсинг открытых групп'''
@router.message(StateFilter(ChatOpenLink.waiting_link))
async def get_open_report(message: Message, state: FSMContext):
    await state.update_data(waiting_link=message.text)
    state_data = await state.get_data()
    link = state_data.get('waiting_link')
    await bot.send_message(message.chat.id, text='Начинаю парсинг, это может занять от 10 до 15 минут⏱')
    upload_message = await bot.send_message(message.chat.id, text='Идёт парсинг: 0% [..........]')
    channel = await client.get_entity(link)
    ALL_PARTICIPANTS: list = []
    for key in config.QUERY:
        progress = (config.QUERY.index(key)+1)*100/len(config.QUERY)
        completion_percentage = float('{:.2f}'.format(progress))
        await upload_message.edit_text(text=f'Идёт парсинг: {completion_percentage}% [{"*"*(int(progress)//10)}{"."*(10-int(progress)//10)}]')
        OFFSET_USER = 0
        while True:
            participants = await client(
                GetParticipantsRequest(channel, ChannelParticipantsSearch(key), OFFSET_USER, config.LIMIT_USER,
                                       hash=0))
            if not participants.users:
                break
            ALL_PARTICIPANTS.extend(participants.users)
            OFFSET_USER += len(participants.users)
        target = '*.txt'
        file = glob.glob(target)[0]
    with open(file, "w", encoding="utf-8") as write_file:
        for participant in ALL_PARTICIPANTS:
            if participant.username != None and participant.bot == False and participant.fake == False:
                write_file.writelines(f"@{participant.username}\n")
    uniqlines = set(open(file, 'r', encoding='utf-8').readlines())
    open(file, 'w', encoding='utf-8').writelines(set(uniqlines))
    await state.finish()
    text = 'Для парсинга следующего чата выберите необходимое действие👇'
    inline_markup = await menu.main_menu()
    await message.reply_document(open(file, 'rb'))
    await message.answer(text, reply_markup=inline_markup, parse_mode='Markdown')

'''Кнопка назад'''
@router.callback_query(Text(startswith='main_menu'))
async def get_main_menu(callback_query: CallbackQuery):
    text = f'Привет *{callback_query.from_user.first_name}*!\n' \
           f'Ваш ID: {callback_query.from_user.id}\n' \
           f'Я могу спарсить любой чат\n' \
           f'Выбери необходимое действие👇'
    inline_markup = await menu.main_menu()
    await callback_query.message.edit_text(text, reply_markup=inline_markup, parse_mode='Markdown')


'''Команда start'''
@router.message(CommandStart())
async def start_message(message: Message):
    text = f'Привет *{message.from_user.first_name}*!\nВаш ID: {message.from_user.id}\nЯ могу спарсить любой чат\n' \
           f'Выбери необходимое действие👇'
    inline_markup = await menu.main_menu()
    username = message.from_user.username
    response = await add_user(message.from_user.id, username) # Доабвляем пользователя
    if response == 1:  # Рассылка уведомления админам о вступление в бот
        admins = await get_admin()
        for admin in admins:
            if username == None:
                await bot.send_message(chat_id=admin['tg_id'],
                                           text=f'Пользователь <a href="tg://user?id={message.from_user.id}">@{message.from_user.first_name}</a> присоединился',
                                           parse_mode='HTML')
            elif message.from_user.username != None:
                await bot.send_message(chat_id=admin['tg_id'],
                                       text=f'Пользователь <a href="tg://user?id={message.from_user.id}">@{username}</a> присоединился',
                                       parse_mode='HTML')
            else:
                await bot.send_message(chat_id=admin['tg_id'],
                                       text=f'Пользователь <a href="tg://user?id={message.from_user.id}">@{username}</a> присоединился',
                                       parse_mode='HTML')
    await message.answer(text=text, reply_markup=inline_markup, parse_mode='Markdown')
    await set_default_commands()

