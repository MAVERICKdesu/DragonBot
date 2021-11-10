from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from Arcapi import AsyncApi,SyncApi
import random
import time
import asyncio
from . import query

@on_command('arcaea', only_to_me=False, aliases=('/arc',))
async def arcaea(session: CommandSession):
    pos = session.current_arg_text
    if pos == "":
        pos = session.get('pos', prompt='id')
    #api_ = SyncApi(user_code=pos,timeout=100)
    #api_ = AsyncApi(user_code=pos,timeout=200)
    songs=await query.call_action(action="scores",start=8,end=12,user_code=pos)
    #songs = eval(str(await api_.scores(start=8, end=12, timeout=200)))
    #songs = eval(str(api_.scores(start=8, end=12,timeout=100)))
    print(songs)
    #recent = songs[1]['recent_score'][0]
    #await session.send("recent play:"+ recent['song_id']+"\nscore:"+str(recent['score'])+"\nconstant:"+str(recent['constant'])+"\nrating:"+str(recent['rating']))


@on_natural_language(only_to_me=False,keywords={'/arc',})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    pos = stripped_msg.split(' ')[1]
    print(pos)
    return IntentCommand(100.0, 'arcaea', current_arg=pos)