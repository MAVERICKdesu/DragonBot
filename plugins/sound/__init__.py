#!/usr/bin/env python
# encoding: utf-8

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .sound_data import get_filelist
import random
import datetime
import os


@on_command('sound', only_to_me=False, aliases=('声音',))
async def sound(session: CommandSession):
    file1 = 'sound\\'
    long_path = 'C:\\dragonbot\\gohttp\\data\\voices\\' + file1
    things = await get_content(long_path)
    times = random.randint(0, len(things) - 1)
    await session.send('[CQ:record,file=' + things[times].replace(long_path, file1) + ']')


@on_command('clock', only_to_me=False, aliases=('报时','时间',))
async def sound(session: CommandSession):
    hour = str(int(datetime.datetime.now().strftime('%H')))
    if hour =='0':
        hour='24'
    hour+=".wav"
    file1 = os.path.join("clock",hour)
    #file1 = "1.wav"
    await session.send('[CQ:record,file=' + file1 + ']')


@on_command('ohy', only_to_me=False, aliases=('哦哈哟','早上好',))
async def sound(session: CommandSession):
    await session.send('[CQ:record,file=clock\ohy.wav]')


@on_command('oysm', only_to_me=False, aliases=('哦呀斯密', '欧亚斯密','晚上好',))
async def sound(session: CommandSession):
    await session.send('[CQ:record,file=clock\oysm.wav]')


async def get_content(path):
    lists = get_filelist(path, [])
    return lists


@on_natural_language(keywords={'声音','舰女人'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'sound')
