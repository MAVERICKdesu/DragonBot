from os import path
import aiohttp
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import requests
import time

from tools.accessTools import get_switch_value

## 来张***的setu / 多来点***的setu / 来张
@on_command('setu', only_to_me=False, aliases=('setu',))
async def setu(session: CommandSession):
    if not get_switch_value(session.ctx, "setu"):
        return
    parmas = {'r18':'0','keyword':'','num':'1','proxy':'i.pixiv.cat','size1200':'false'}
    if 'r18' in session.current_arg_text:
        parmas['r18'] = '1'
    if '多来' in session.current_arg_text:
        parmas['num'] = '3'
    if '高清' in session.current_arg_text:
        parmas['size1200'] = 'false'
    if '的' in session.current_arg_text:
        end = session.current_arg_text.find('的')
        begin=-1
        if '点' in session.current_arg_text:
            begin = session.current_arg_text.find('点')
        if '张' in session.current_arg_text:
            begin = session.current_arg_text.find('张')
        if begin!=-1:
            parmas['keyword'] = session.current_arg_text[begin + 1:end]
    url = "https://api.lolicon.app/setu/v1?"
    for key, value in parmas.items():
        url = url+key+"="+value+"&"
    url = url[:-1]
    res = requests.get(url)
    dic1 = res.content.decode("utf-8").replace('null', '"null"').replace("false","0").replace("true","0")
    dic = eval(dic1)
    if dic['code'] == 404:
        await session.send("没有找到相应的setu哟")
        return
    data = dic["data"][0]
    t = str(int(time.time())) + data['url'][-4:]
    cont = 0
    async with aiohttp.ClientSession() as sess:
        async with sess.get(data['url']) as resp:
            if resp.status == 200:
                with open(path.join(session.bot.config.SCORCE_IMG_PATH, 'dragon', t), 'wb+') as f2:
                    cont = await resp.content.read()
                    f2.write(cont)
            else:
                await session.send("图片获取失败，请稍后重试")
                return

    ret = f"[CQ:at,qq={str(session.ctx.sender['user_id'])}]\npid:{str(data['pid'])}\nuid:{str(data['uid'])}\ntitle:{data['title']}\nauthor:{data['author']}\nurl:{data['url']}[CQ:image,file=dragon/{t}]"
    await session.send(ret)



@on_natural_language(only_to_me=False, keywords={'色图','setu','r18'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'setu', current_arg=session.msg_text.strip())




#https://api.lolicon.app/setu/v1