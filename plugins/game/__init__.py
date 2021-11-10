#!/usr/bin/env python
# encoding: utf-8

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .gamedata import get_gamedata


@on_command('gameres', only_to_me=False, aliases=('战绩',))
async def gameres(session: CommandSession):
    name = session.get('name', prompt='输入用户id')
    res = await get_gamedata(name)
    await session.send(res)


@gameres.args_parser
async def _(session: CommandSession):
    name = session.current_arg_text.strip()
    if session.is_first_run:
        if name:
            session.state['name'] = name
        return
    if not name:
        session.pause('名称不能为空呢，重新输入')
    session.state[session.current_key] = name


@on_natural_language(only_to_me=False, keywords={'r6战绩'})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    name = stripped_msg[5:]
    return IntentCommand(100.0, 'gameres', current_arg=name)
