#!/usr/bin/env python
# encoding: utf-8

from nonebot import on_command, CommandSession


@on_command('touzi', only_to_me=False, aliases=('骰子','头子','赌博','赌狗'))
async def touzi(session: CommandSession):
    await session.send('[CQ:dice,type={1}]')


@on_command('quan', only_to_me=False, aliases=('打拳','猜拳'))
async def quan(session: CommandSession):
    await session.send('[CQ:rps,type={1}]')
