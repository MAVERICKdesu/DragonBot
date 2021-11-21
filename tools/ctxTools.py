from aiocqhttp import message
from aiocqhttp.event import Event

def is_group(event:Event):
    is_group = "group_id" in event
    id = event["group_id"] if is_group else event["sender"]["user_id"]

    return  is_group, id

def get_all_img_url(event:Event):
    all_url = []
    for i in event["message"]:
        if i["type"] == "image":
            all_url.append(i["data"]["url"])
    
    return all_url
