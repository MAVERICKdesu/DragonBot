from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import random
import datetime
import pytz
import time


@on_command('watch', only_to_me=False, aliases=())
async def watch(session: CommandSession):
    await session.send('北京时间 ' + datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d_%H:%M")+'\n'
                       +'西雅图时间 ' + datetime.datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%Y-%m-%d_%H:%M")+'\n'
                       + '纽约时间 ' + datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%Y-%m-%d_%H:%M") + '\n'
                       +'东京时间 ' + datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d_%H:%M")+'\n'
                       +'斯德哥尔摩时间 ' + datetime.datetime.now(pytz.timezone('Europe/Stockholm')).strftime("%Y-%m-%d_%H:%M"))


@on_natural_language(only_to_me=False,keywords={'手表','看表','表来','表呢','有表'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'watch')



