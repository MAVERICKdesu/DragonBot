from os import path
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import random
import datetime

from tools.fileTools import get_content


@on_command('sound', only_to_me=False, aliases=('声音',))
async def sound(session: CommandSession):
    base_path = path.join(session.bot.config.SCORCE_VOICE_PATH, 'sound')
    sound_list = await get_content(base_path)
    index = random.randint(0, len(sound_list) - 1)
    await session.send('[CQ:record, file=' + path.join('sound', sound_list[index]) + ']')


@on_command('clock', only_to_me=False, aliases=('报时','时间',))
async def sound(session: CommandSession):
    hour = str(int(datetime.datetime.now().strftime('%H')))
    if hour =='0':
        hour='24'
    await session.send('[CQ:record, file=' + path.join("clock", hour + ".wav") + ']')


@on_command('ohy', only_to_me=False, aliases=('哦哈哟','早上好',))
async def sound(session: CommandSession):
    await session.send('[CQ:record, file=clock\ohy.wav]')


@on_command('oysm', only_to_me=False, aliases=('哦呀斯密', '欧亚斯密','晚上好',))
async def sound(session: CommandSession):
    await session.send('[CQ:record,file=clock\oysm.wav]')


@on_natural_language(keywords={'声音','舰女人'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'sound')
