from os import path
from aiocqhttp import message
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

import json
import random

@on_command('food', only_to_me=False, aliases=('',))
async def food(session: CommandSession):
    message = session.event.raw_message.strip()
    food = "外卖"
    food_data = {}
    with open(path.join(session.bot.config.PLUGINS_PATH, "food", "food.json"), 'r', encoding='utf-8')as fp:
        food_data = json.load(fp)
    for place in food_data.keys():
        if place in message:
            food_of_place = food_data[place]
            food = food_of_place[random.randint(0, len(food_data[place]) - 1)]
            break
    await session.send(food)


@on_command('uploadfood', only_to_me=False, aliases=('上传食物', '上传食谱',))
async def uploadfood(session: CommandSession):
    para = session.current_arg.split()
    if len(para) == 2:
        place, food = para[0], para[1]
    else:
        new_place = (await session.get('new_place', prompt='输入地点和食物，空格隔开')).split()
        if len(new_place) != 2:
            await session.send("格式错误")
            return
        else:
            place, food = new_place.split()[0], new_place.split()[1]

    if "吃什么" in place or "嘉然" in place or "嘉然" in food:
        await session.send("不准传了") 
        return    
    with open(path.join(session.bot.config.PLUGINS_PATH, "food", "food.json"), 'r', encoding='utf-8')as fp:
        food_data = json.load(fp) 
    if place in food_data.keys():
        food_data[place].append(food)
    else:
        food_data[place] = [food]
    with open(path.join(session.bot.config.PLUGINS_PATH, "food", "food.json"), 'w', encoding='utf-8')as fp:
        json.dump(food_data, fp, ensure_ascii=False)
    await session.send("添加成功！")


@on_natural_language(only_to_me=False, keywords={'吃什么', '吃啥', '去哪吃'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'food')

