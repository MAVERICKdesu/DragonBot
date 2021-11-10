import time
import requests


def upup(address, n, id):
    list1 = ['dragon','motto']
    path = 'C:\\dragonbot\\gohttp\\data\\images\\'+address
    path2 = 'C:\\dragonbot\\gohttp\\data\\images\\bot\\'+list1[n]+'\\'
    if (id == 135720324) | (id == 715620136):
        path2 += "main\\"
    else:
        path2  += str(id) + "\\"
    url = ''
    with open(path,'r') as f:
        line = f.readline()  # 调用文件的 readline()方法
        while line:
            if line[:4] == 'url=':
                url = line[4:]
                if len(url)<5:
                    return 'None'
                break
            line = f.readline()
    if not url:
        return
    t = str(int(time.time()))+address[-4:]
    with open(path2+t,'wb+') as f2:
        cont = requests.get(url)
        f2.write(cont.content)
    return url


def urlup(address,url,text, id):
    path2 = 'C:\\dragonbot\\gohttp\\data\\images\\bot\\'+text+'\\'
    if text=="motto":
        if (id == 135720324) | (id == 715620136):
            path2 += "main\\"
        else:
            path2  += str(id) + "\\"
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    cont=requests.get(url=url,headers=headers)
    print(cont.headers["Content-Type"])
    t = str(int(time.time()))+"."+cont.headers["Content-Type"].split("/")[1]
    with open(path2+t,'wb+') as f2:
        f2.write(cont.content)