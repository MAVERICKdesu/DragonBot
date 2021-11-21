from nonebot import on_command, CommandSession
import http.client
import random
import hashlib
import urllib
import json


@on_command('trans', only_to_me=False, aliases=('翻译',))
async def upload(session: CommandSession):
    ph = session.current_arg_text.strip()
    session.state[session.current_key] = ph
    ph = session.get('ph', prompt='在第一行加入翻译类型，如中译英为"zh en"')
    if not session.is_first_run:
        content = session.current_arg_text
        quest = {'q':content.split('\n')[1],
                 'from':content.split('\n')[0].split(' ')[0],
                 'to':content.split('\n')[0].split(' ')[1][:-1],
                 'appid':'20200702000511073',
                 'secretKey':'SultFhmzwQQfkCGLW3aW'}
        salt = str(random.randint(32768,65536))
        sign = quest['appid'] + quest['q'] + salt + quest['secretKey']
        sign = hashlib.md5(sign.encode()).hexdigest()
        url = '/api/trans/vip/translate'
        myurl = url + f"?appid={quest['appid']}&q={urllib.parse.quote(quest['q'])}&from={quest['from']}&to={quest['to']}&salt={salt}&sign={sign}"
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET',myurl)
        response = httpClient.getresponse()
        result_all=response.read().decode("utf-8")
        result=json.loads(result_all)
        print(quest)
        print(result)
        re = str(result['trans_result'][0]['dst'])
        await session.send(re)

    if not ph:
        session.pause('不能为空呢，重新输入')

