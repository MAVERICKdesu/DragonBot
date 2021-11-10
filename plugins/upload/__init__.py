#!/usr/bin/env python
# encoding: utf-8

import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .photo_upload import upup,urlup


@on_command('upload', only_to_me=False, aliases=('上传图片',))
async def upload(session: CommandSession):
    ph = session.current_arg_text.strip()
    session.state[session.current_key] = ph
    ph = session.get('ph', prompt='发送要上传的图片')
    if not session.is_first_run:
        if session.current_arg != '结束':
            url = session.current_arg_images
            urlup(session.current_arg.split(',')[1][6:], url[0], 'dragon', session.ctx["group_id"])
            session.pause('继续')
    if not ph:
        session.pause('不能为空呢，重新输入')
    await session.send('就这？')



@on_command('uploadmotto', only_to_me=False, aliases=('上传语录',))
async def uploadmotto(session: CommandSession):
    ph = session.current_arg_text.strip()
    session.state[session.current_key] = ph
    ph = session.get('ph', prompt='发送要上传的图片')
    if not session.is_first_run:
        if session.current_arg != '结束':
            url = session.current_arg_images
            urlup(session.current_arg.split(',')[1][6:], url[0], 'motto', session.ctx["group_id"])
            session.pause('继续')
    if not ph:
        session.pause('不能为空呢，重新输入')
    await session.send('就这？')


