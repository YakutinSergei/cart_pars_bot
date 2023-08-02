from telethon import TelegramClient, events, sync, connection
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import asyncio

r_api = 28867506 #данные скрыты в целях безопасности
r_hash = '0e7a9bc55d6218dabd16610e397f67b5' #данные скрыты в целях безопасности

client = TelegramClient('session_name2', r_api, r_hash)
client.start()

def pars():
    async def p():
        channel = await client.get_entity('t.me/Parsinger_Telethon_Test')
        print(channel)
    # chat_id = 1795821154
    # participants = await client(GetParticipantsRequest(
    #                 channel = channel,
    #                 filter=ChannelParticipantsSearch(''),
    #                 offset=0,
    #                 limit=100,
    #                 hash=0))
    #
    # print(participants.users)

