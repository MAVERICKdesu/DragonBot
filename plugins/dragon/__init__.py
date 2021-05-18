from nonebot import on_command, CommandSession
from .findlong import get_long
import random
import time


@on_command('dragon', only_to_me=False, aliases=('龙来', '龙图来', '龙','龙图'))
async def dragon(session: CommandSession):
    file1 = 'dragon\\'
    long_path = 'C:\\dragonbot\\gohttp\\data\\images\\bot\\'+file1
    things = await get_content(long_path)
    times = random.randint(0, len(things)-1)
    await session.send('[CQ:image,file='+things[times][32:]+']')


@on_command('dragon', only_to_me=False, aliases=('十连', '龙龙龙'))
async def dragon(session: CommandSession):
    file1 = 'dragon\\'
    tim =0
    with open("datadra.txt", 'r') as f:
        tim = f.readline()
    if int(time.time()) - int(tim) < 60 * 30:
        await session.send('十连CD尚未冷却！还剩' + str(60 * 30-int(time.time()) + int(tim)) + "s")
    else:
        with open("datadra.txt", 'w') as f:
            f.write(str(int(time.time())))
        long_path = 'C:\\dragonbot\\gohttp\\data\\images\\bot\\'+file1
        things = await get_content(long_path)
        time1 = [ random.randint(0, len(things)-1) for i in range(10)]
        for times in time1:
            await session.send('[CQ:image,file='+things[times][32:]+']')


@on_command('dragon', only_to_me=False, aliases=('海伦娜',))
async def dragon(session: CommandSession):
    await session.send('[CQ:image,file=bot\\dragon\\1594571132.jpg]')

async def get_content(path):
    lists = get_long(path, [])
    return lists




