from os import path
import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

from tools.fileTools import download_img_and_save
from tools.ctxTools import get_all_img_url, is_group


@on_command('upload', only_to_me=False, aliases=('上传图片', '上传语录'))
async def upload(session: CommandSession):
    if session.is_first_run:
        group, id = is_group(session.ctx)
        upload_folder = ''
        if "图片" in session.event.raw_message:
            upload_folder = "dragon"
        elif "语录" in session.event.raw_message:
            upload_folder = "motto"
        session.state['folder'] = upload_folder
        session.state['id'] = str(id)
        session.state['group'] = group
    session.get('', prompt='发送要上传的图片')
    if session.current_arg != '结束':
        all_img_url = get_all_img_url(session.ctx)
        for url in all_img_url:
            download_img_and_save(session.bot.config.SCORCE_IMG_PATH, session.state['folder'], url, session.state['id'], session.state['group'])
        session.pause('继续')
    await session.send('就这？')
