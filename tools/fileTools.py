from os import path, listdir, makedirs
import time
import requests

def create_dir(base_path):
    if not path.exists(base_path):
        makedirs(base_path)


async def get_content(base_path):
    create_dir(base_path)
    lists = get_all_file(base_path, [])

    return lists


def get_all_file(base_path, file_list, add_path = ''):
    crr_path = path.join(base_path, add_path)

    if path.isfile(crr_path):
        file_list.append(add_path)
    elif path.isdir(crr_path):
        for s in listdir(crr_path):
            get_all_file(base_path, file_list, path.join(add_path, s))

    return file_list


def download_img_and_save(base_path, folder, url, id, is_group):
    save_path = path.join(base_path, folder,"group" if is_group else "user", id)
    if folder == "dragon":
        save_path = path.join(base_path, folder)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    cont = requests.get(url=url,headers=headers)
    t = str(int(time.time())) + "." + cont.headers["Content-Type"].split("/")[1]
    print(path.join(save_path, t))
    with open(path.join(save_path, t),'wb+') as f2:
        f2.write(cont.content)
