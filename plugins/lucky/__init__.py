#!/usr/bin/env python
# encoding: utf-8

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .luckydata import get_lucky
import random


@on_command('lucky', only_to_me=False, aliases=('今日运势',))
async def sound(session: CommandSession):
    res = await get_content()
    await session.send(res)


async def get_content():
    lists = get_lucky()
    return lists

