import requests
import time

def get_lucky():
    time_str = str(time.time())[:10]
    url = 'http://api.tianapi.com/txapi/lunar/index?key=b0eee04601ff8583d70aeb1418a57451&date=' + time_str
    res = requests.get(url)
    dic1 = res.content.decode("utf-8")
    dic = eval(dic1)
    ans = '农历:' + dic['newslist'][0]['lunardate']+'\n节假日:'+dic['newslist'][0]['festival']+'\n宜:'+dic['newslist'][0]['fitness']+'\n忌:'+dic['newslist'][0]['taboo']
    return ans
