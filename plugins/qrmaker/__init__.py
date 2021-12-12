import os, asyncio, requests
from .qrcode_maker import qrcode
from PIL import Image
from io import BytesIO
import nonebot
from nonebot import on_command
from nonebot import CommandSession
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "zh-cn"
           }
 
    
def get_set(arrs):
    result = []
    for i in range(4):
        try:
            result.append(arrs[i])
        except:
            result.append(None)
    
    re_result = ['', False, None, None]
    re_result[0] = result[0]
    index = 0
    for re in result:
        if index == 0:
            index += 1
            continue
        if result[index] == 'c':
            re_result[1] = True
            index += 1
            continue
        if result[index]:
            try:
                if not re_result[2]:
                    re_result[2] = float(result[index])
                else:
                    re_result[3] = float(result[index])
            except:
                if not re_result[2]:
                    re_result[2] = 1.0
                else:
                    re_result[3] = 1.0
            index += 1
            continue
        else:
            index += 1
            continue
    if not re_result[2] or (re_result[2] * 10) not in range(0, 11):
        re_result[2] = 1.0
    if not re_result[3] or (re_result[3] * 10) not in range(0, 11):
        re_result[3] = 1.0
        
    return re_result



def save_img(url):
    response = requests.get(url, headers=headers)
    image = Image.open(BytesIO(response.content))
    try:
        image_type = 'gif' if image.n_frames >= 1 and image.n_frames <= 200 else 'png'  #帧数过多处理过满
    except:
        image_type = 'png'
    image.save(os.path.join(os.path.dirname(__file__), f'temp.{image_type}'))
    picture = os.path.join(os.path.dirname(__file__), f'temp.{image_type}')
    return picture, image_type

@on_command('qrmaker', only_to_me=False, aliases=('!qr'))
async def qrcode_maker(session: CommandSession):
    #msg = session.current_arg.strip()
    picture, text, image_type = [None, '', 'png']
    for i in session.ctx["message"]:
        if i["type"] == 'image':
            try:
                picture, image_type = save_img(i['data']['url'])
            except Exception as e:
                print(repr(e))
                await session.finish('图片读取发生错误，您可能是转发的含图消息，请不要转发')
        elif i["type"] == 'text':
            arrs = str(i).split()
            text, colorized, contrast, brightness = get_set(arrs)
        if picture and text:
            break
    try:
        qr = qrcode(text, picture = picture, colorized = colorized, contrast = contrast, brightness = brightness, image_type = image_type)
    except Exception as e:
        print(repr(e))
        await session.finish('二维码生成发生错误，暂不支持生成中文二维码哦')

    if picture:
        os.remove(picture)
    await session.finish(f'[CQ:image,file={qr.base64_str}]')
    
