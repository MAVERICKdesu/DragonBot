from nonebot import on_command, CommandSession
from .findlong import get_long
import random


@on_command('dragon', only_to_me=False, aliases=('龙来', '龙图来', '龙','龙图'))
async def dragon(session: CommandSession):
    file1 = 'dragon\\'
    long_path = 'E:\\MyFiles\\web\\gohttp\\data\\images\\bot\\'+file1
    things = await get_content(long_path)
    times = random.randint(0, len(things)-1)
    await session.send('[CQ:image,file='+things[times][33:]+']')


@on_command('dragon', only_to_me=False, aliases=('十连', '龙龙龙'))
async def dragon(session: CommandSession):
    file1 = 'dragon\\'
    long_path = 'E:\\MyFiles\\web\\gohttp\\data\\images\\bot\\'+file1
    things = await get_content(long_path)
    time1 = [ random.randint(0, len(things)-1) for i in range(10)]
    for times in time1:
        await session.send('[CQ:image,file='+things[times][33:]+']')


@on_command('dragon', only_to_me=False, aliases=('海伦娜',))
async def dragon(session: CommandSession):
    await session.send('[CQ:image,file=bot\\dragon\\1594571132.jpg]')

async def get_content(path):
    lists = get_long(path, [])
    return lists




