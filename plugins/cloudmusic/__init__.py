from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import requests


@on_command('music', only_to_me=False, aliases=('点歌',))
async def music(session: CommandSession):
    para = session.current_arg.strip()
    if para == "":
        para = session.get('pos', prompt='输入音乐')
    music_api = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=" + para + "&type=1&offset=0&total=true&limit=1"
    ret = requests.get(url = music_api)
    music_data = eval(ret.text.replace("null", "0").replace("true", "1").replace("false", "0"))
    music_id = music_data["result"]["songs"][0]["id"]
    await session.send("[CQ:music,type=163,id=" + str(music_id) + ']')
