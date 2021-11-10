from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import nonebot
import requests
from typing import List,Dict
import time

@on_command('test', only_to_me=False, aliases=('test',))
async def test(session: CommandSession):
    parmas : List[dict] = []
    dic : Dict = {"user_id":714650324,"message":"1111"}
    id = await nonebot.get_bot().send_private_msg(user_id=714650324,message="1111")
    #await nonebot.get_bot().
    await session.send(str(id));
    #await nonebot.get_bot()
