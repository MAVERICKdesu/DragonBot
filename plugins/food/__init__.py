#!/usr/bin/env python
# encoding: utf-8

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .get_food import get_pos


@on_command('food', only_to_me=False, aliases=('吃',))
async def food(session: CommandSession):
    pos = session.get('pos', prompt='输入校区')
    res = await get_pos(pos)
    await session.send(res)


@food.args_parser
async def _(session: CommandSession):
    pos = session.current_arg_text.strip()
    if session.is_first_run:
        if pos:
            session.state['pos'] = pos
        return
    if not pos:
        session.pause('重新输入')
    session.state[session.current_key] = pos


@on_natural_language(only_to_me=False, keywords={'吃什么','吃啥','去哪吃'})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    if '津南'in stripped_msg:
        pos = '津南'
    elif '八里台'in stripped_msg:
        pos = '八里台'
    else:
        pos = '其他'
    return IntentCommand(100.0, 'food', current_arg=pos)

