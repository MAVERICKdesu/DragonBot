from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import requests


@on_command('music', only_to_me=False, aliases=('点歌',))
async def music(session: CommandSession):
    pos = session.current_arg_text
    if pos=="":
        pos = session.get('pos', prompt='输入音乐')
    turl="http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s="+pos+"&type=1&offset=0&total=true&limit=1"
    ret = requests.get(url=turl)
    print(ret.text)
    j = eval(ret.text.replace("null","0").replace("true","1").replace("false","0"))
    #print(j)
    id = j["result"]["songs"][0]["id"]
    id=j["result"]["songs"][0]["id"]
    await session.send("[CQ:music,type=163,id="+str(id)+']')


@on_natural_language(only_to_me=False, keywords={'点歌',})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    pos = stripped_msg[3:]
    print(pos)
    return IntentCommand(100.0, 'music', current_arg=pos)

