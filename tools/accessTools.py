from typing import Dict, List
from nonebot import CommandSession
from aiocqhttp.event import Event

from tools.ctxTools import is_group


FUNCTION_SWITCH = {}


def get_switch_value(event:Event, funName: str) -> bool:
    if FUNCTION_SWITCH[funName]["allon"]:
        return True

    group, id = is_group(event)
    
    if group:
        return id in FUNCTION_SWITCH[funName]["on"]["group"]
    else:
        return id in FUNCTION_SWITCH[funName]["on"]["users"]
