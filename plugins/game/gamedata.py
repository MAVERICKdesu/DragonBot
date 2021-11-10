import requests


async def get_gamedata(name: str):
    url = 'https://www.r6s.cn/Stats?username='+name+'&platform='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'referer': 'https: // www.r6s.cn / stats.jsp?username = Taskforce_404'
    }
    res = requests.get(url, headers=headers)
    dic1 = res.content.decode("utf-8").replace('null', '"null"')
    dic = eval(dic1)
    ans = "等级:"+str(dic["Basicstat"][0]["level"])+"\nmmr分数:"+str(dic["Basicstat"][0]["mmr"])
    ans += ""
    return ans
