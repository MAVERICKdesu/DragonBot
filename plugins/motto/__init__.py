from nonebot import NoneBot, on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from os import path

from nonebot.permission import GROUP
from tools.ctxTools import is_group
from tools.fileTools import get_content

import random
import time


@on_command('motto', only_to_me = False, aliases = ('语录', '名言警句', '语录十连'))
async def motto(session: CommandSession):
    group, id = is_group(session.ctx)
    folder = path.join("motto", "group" if group else "user", str(id))
    if group and id in [135720324, 715620136]:
        folder = path.join("motto", "group", "main")

    motto_path = path.join(session.bot.config.SCORCE_IMG_PATH, folder)
    things = await get_content(motto_path)

    if len(things):
        loop_number = 1
        if '十连' in session.event.raw_message:
            loop_number = 10
            cd_data_path = path.join(session.bot.config.PLUGINS_PATH, "motto", "datamotto.txt")
            with open(cd_data_path, 'r') as f:
                last_call_time = f.readline()
                if int(time.time()) - int(last_call_time) < 1800:
                    await session.send('十连CD尚未冷却！')
                    
                    return
                else:
                    with open(path.join(session.bot.config.PLUGINS_PATH, "motto", "datamotto.txt"), 'w') as f:
                        f.write(str(int(time.time())))

        for i in range(loop_number):
            index = random.randint(0, len(things) - 1)
            await session.send('[CQ:image,file=' + path.join(folder, things[index]) + ']')
    else:
        await session.send('图库空空如也')


@on_natural_language(only_to_me=False,keywords={'治国理政', '批话'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'motto')
