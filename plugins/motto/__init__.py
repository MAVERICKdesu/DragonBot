from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .mottodata import get_lon
import random
import time


@on_command('motto', only_to_me=False, aliases=('语录','名言警句',))
async def motto(session: CommandSession):
    file1 = 'motto\\'
    print(session.ctx["group_id"])
    if (session.ctx["group_id"] == 135720324) | (session.ctx["group_id"] == 715620136):
        file1+="main\\"
    else:
        file1 += str(session.ctx["group_id"]) +"\\"
    long_path = 'C:\\dragonbot\\gohttp\\data\\images\\bot\\'+file1
    print(long_path)
    things = await get_content(long_path)
    times = random.randint(0, len(things)-1)
    await session.send('[CQ:image,file='+things[times][32:]+']')


@on_command('moremotto', only_to_me=False, aliases=('语录十连',))
async def moremotto(session: CommandSession):
    file1 = 'motto\\'
    tim = 0
    if (session.ctx["group_id"] == 135720324) | (session.ctx["group_id"] == 715620136):
        file1 += "main\\"
    else:
        file1 += str(session.ctx["group_id"]) + "\\"
    with open("datamotto.txt", 'r') as f:
        tim = f.readline()
    if int(time.time())-int(tim)<60*30:
        await session.send('十连CD尚未冷却！还剩'+str(60 * 30-int(time.time()) + int(tim))+"s")
    else:
        with open("C:/dragonbot/Code/DragonBot/datamotto.txt", 'w') as f:
            f.write(str(int(time.time())))
        long_path = 'C:\\dragonbot\\gohttp\\data\\images\\bot\\'+file1
        things = await get_content(long_path)
        time1 = [ random.randint(0, len(things)-1) for i in range(10)]
        for times in time1:
            await session.send('[CQ:image,file='+things[times][32:]+']')


async def get_content(path):
    lists = get_lon(path, [])
    return lists


@on_natural_language(only_to_me=False,keywords={'治国理政','批话'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'motto')



