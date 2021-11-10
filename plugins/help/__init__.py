from nonebot import on_command, CommandSession


@on_command('gameres', only_to_me=False, aliases=('help',))
async def gameres(session: CommandSession):
    '''res = '龙图bot 精英人形G11，堂堂复活！\n' \
          'bot结构:go-cqhttp+nonebot\n' \
          '此bot仅供小团体娱乐，请勿将bot发送的任何图片外传，尤其是涉及到聊天内容的图片！\n' \
          '图片：分为语录和图片(混有龙图，，，),直接在群内发送"语录"或者"龙图"即可获取单张图片\n' \
          '上传功能：输入"上传图片"或者"上传语录"，然后依次发送单张图片，结束时发送"结束"即可\n' \
          '吃什么：输入"XXX吃什么"，便可以由精英人形帮你选择去哪吃饭！\n' \
          '网易云点歌：输入"点歌 XXX"即可\n' \'
          '\n作者github页面 https://github.com/MAVERICKdesu\n有任何疑问请联系7146540324\n'
    res=res+'[CQ:image,file=bot\\dragon\\1620636942.jpeg]
    await session.send(res)'''
