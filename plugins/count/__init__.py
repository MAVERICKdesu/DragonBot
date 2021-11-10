from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import requests


@on_command('count', only_to_me=False, aliases=('count',))
async def music(session: CommandSession):
    pos = session.current_arg_text
    print(pos)
    ans =0
    print(session.ctx['sender']['user_id'] == 714650324)
    if session.ctx['sender']['user_id'] == 714650324 or session.ctx['sender']['user_id']== 1421971518:
        with open("C:/dragonbot/Code/DragonBot/count.txt", 'r') as f:
            tim = f.readline()
        print(tim)
        if pos =="up":
            ans=eval(tim)+1
        elif pos =="down":
            ans=eval(tim)-1
        else:
            ans=tim
        with open("C:/dragonbot/Code/DragonBot/count.txt", 'w') as f:
            f.write(str(ans))
        await session.send("count: "+str(ans))
    else:
        with open("C:/dragonbot/Code/DragonBot/count.txt", 'r') as f:
            tim = f.readline()
        await session.send("count: "+tim)




@on_natural_language(only_to_me=False, keywords={'count',})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    pos = stripped_msg
    #pos = stripped_msg[3:]
    #print(pos)
    return IntentCommand(100.0, 'count', current_arg=pos)

