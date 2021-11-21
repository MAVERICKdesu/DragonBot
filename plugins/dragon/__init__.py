from nonebot import NoneBot, on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from os import path

from nonebot.permission import GROUP
from tools.accessTools import get_switch_value
from tools.fileTools import get_content

import random
import time


@on_command('dragon', only_to_me = False, aliases = ('龙来','龍', '龙图来', '龙', '龙图', "十连", "龙龙龙"))
async def dragon(session: CommandSession):
    if not get_switch_value(session.ctx, 'dragon'):
        return
    dragon_path = path.join(session.bot.config.SCORCE_IMG_PATH, "dragon")
    things = await get_content(dragon_path)

    if len(things):
        loop_number = 1
        if '十连' in session.event.raw_message or '龙龙龙' in session.event.raw_message:
            loop_number = 10
            cd_data_path = path.join(session.bot.config.PLUGINS_PATH, "dragon", "datadra.txt")
            with open(cd_data_path, 'r') as f:
                last_call_time = f.readline()
                if int(time.time()) - int(last_call_time) < 1800:
                    await session.send('十连CD尚未冷却！')

                    return
                else:
                    with open(path.join(session.bot.config.PLUGINS_PATH, "dragon", "datadra.txt"), 'w') as f:
                        f.write(str(int(time.time())))

        for i in range(loop_number):
            index = random.randint(0, len(things) - 1)
            await session.send('[CQ:image,file=' + path.join("dragon", things[index]) + ']')
    else:
        await session.send('图库空空如也')


@on_command('hlndragon', only_to_me=False, aliases=('海伦娜',))
async def hlndragon(session: CommandSession):
    await session.send('[CQ:image,file=dragon/1594571132.jpg]')