from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def main_menu():
    inline_markup: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    buttons.append(InlineKeyboardButton(
            text='🔍Спарсить открытый чат',
            callback_data='parsing_open_start'
        ))
    buttons.append(types.InlineKeyboardButton(
            text='🔒Premium функции',
            callback_data='premium_menu'
        ))
    inline_markup.row(*buttons, width=1)
    return inline_markup.as_markup()


async def premium_parsing_menu():
    inline_markup: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    inline_markup.add(types.InlineKeyboardButton(
            text='📆По дате последнего посещения',
            callback_data='parsing_activity'
    ))
    buttons.append(types.InlineKeyboardButton(
        text='📱Моб. телефоны',
        callback_data='phones'
    ))
    buttons.append(types.InlineKeyboardButton(
        text='🔙Назад',
        callback_data='main_menu'
    ))
    inline_markup.row(*buttons, width=1)
    return inline_markup.as_markup()



async def last_active_menu():
    inline_markup: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    buttons.append(types.InlineKeyboardButton(
            text='Был(а) недавно',
            callback_data='online_recently'
    ))
    buttons.append(types.InlineKeyboardButton(
            text='Был(а) на этой неделе',
            callback_data='online_week'
    ))
    inline_markup.row(*buttons, width=1)
    return inline_markup.as_markup()


async def admin_menu():
    inline_markup: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    buttons.append(types.InlineKeyboardButton(
            text='Создать рассылку',
            callback_data='create_mailing'
    ))
    buttons.append(types.InlineKeyboardButton(
            text='Статистика',
            callback_data='stat'
    ))
    buttons.append(types.InlineKeyboardButton(
            text='Дать права админа',
            callback_data='set_admin_previlegies'
    ))
    buttons.append(types.InlineKeyboardButton(
        text='Дать премиум статус',
        callback_data='set_premium'
    ))
    inline_markup.row(*buttons, width=1)
    return inline_markup.as_markup()