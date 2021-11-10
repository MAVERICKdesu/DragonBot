import re
import json
from typing import List, Dict, Any
import websockets
import brotli


async def call_action(action: str, **params):
    ws_endpoint = 'wss://arc.estertion.win:616'
    user_code = params['user_code']
    _start = params['start']
    _end = params['end']
    container: List[Dict] = []  # The result list for request objects
    async with websockets.connect(ws_endpoint, timeout=5) as conn:
        await conn.send(f'{user_code} {_start} {_end}')
        _recv = await conn.recv()
        print("start get")
        if _recv == 'invalid id':
            raise ArcInvaidUserCodeException
        elif _recv == 'queried':
            while True:
                _r = await conn.recv()
                if isinstance(_r, str) and _r == 'bye':
                    break
                elif isinstance(_r, (bytes, bytearray)):
                    _data = json.loads(brotli.decompress(_r))
                    if _data['cmd'] == action:
                        if type(_data['data']) is list:
                            for _item in _data['data']:
                                container.append(_item)
                                print(_item)
                    else:
                        container.append(_data['data'])
        else:
            raise ArcUnknownException(_recv)
    return container


class ArcBaseException(BaseException):
    pass


class ArcInvaidUserCodeException(ArcBaseException):
    pass


class ArcUnknownException(ArcBaseException):
    def __init__(self, details: str):
        self.details = details

    def __str__(self):
        return f'<ArcUnknownException, error={self.details}>'

    def __repr__(self):
        return self
