import nonebot
from nonebot import on_command, CommandSession
import os
from nonebot import on_natural_language, NLPSession, IntentCommand

@on_command('video', only_to_me=False, aliases=())
async def music(session: CommandSession):
    dir = os.path.join(session.bot.config.SCORCE_VIDEO_PATH, "upload")
    pos = session.current_arg_text
    text = "输入视频名称进行点播：\n"
    if pos == "":
        for s in os.listdir(dir):
            if s[-3:]!="jpg":
                text = text + s + "\n"
        pos = session.get('pos', prompt=text)
    await session.send("[CQ:video,file=upload/" + pos + ']')

@on_natural_language(only_to_me=False, keywords={'点播',})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    pos = stripped_msg[3:]
    print(pos)
    return IntentCommand(100.0, 'video', current_arg=pos)