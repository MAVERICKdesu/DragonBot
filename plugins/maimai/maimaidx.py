from nonebot import on_command, CommandSession
from src.libraries.tool import hash
from src.libraries.maimaidx_music import *
from src.libraries.image import *
from src.libraries.maimai_best_40 import generate,computeRa
from collections import defaultdict
from nonebot import on_natural_language, NLPSession, IntentCommand
import re


def song_txt(music: Music):
    return ([
        {
            "type": "text",
            "data": {
                "text": f"{music.id}. {music.title}\n"
            }
        },
        {
            "type": "image",
            "data": {
                "file": f"https://www.diving-fish.com/covers/{music.id}.jpg"
            }
        },
        {
            "type": "text",
            "data": {
                "text": f"\n{'/'.join(music.level)}"
            }
        }
    ])


def inner_level_q(ds1, ds2=None):
    result_set = []
    diff_label = ['Bas', 'Adv', 'Exp', 'Mst', 'ReM']
    if ds2 is not None:
        music_data = total_list.filter(ds=(ds1, ds2))
    else:
        music_data = total_list.filter(ds=ds1)
    for music in sorted(music_data, key = lambda i: int(i['id'])):
        for i in music.diff:
            result_set.append((music['id'], music['title'], music['ds'][i], diff_label[i], music['level'][i]))
    return result_set


@on_command('inner_level', only_to_me=False, aliases={'定数查歌'})
async def inner_level(session: CommandSession):
    argv = session.current_arg_text.split(" ")
    print(argv)
    print(session.current_arg_text)
    if len(argv) > 2 or len(argv) == 0:
        await session.send("命令格式为\n定数查歌 <定数>\n定数查歌 <定数下限> <定数上限>")
        return
    if len(argv) == 1:
        result_set = inner_level_q(float(argv[0]))
    else:
        result_set = inner_level_q(float(argv[0]), float(argv[1]))
    if len(result_set) > 50:
        await session.send(f"结果过多（{len(result_set)} 条），请缩小搜索范围。")
        return
    s = ""
    for elem in result_set:
        s += f"{elem[0]}. {elem[1]} {elem[3]} {elem[4]}({elem[2]})\n"
    await session.send(s)


@on_command('spec_rand', only_to_me=False, aliases={r"随个((?:dx|sd|标准))?([绿黄红紫白]?)([0-9]+\+?)"})
async def spec_rand(session: CommandSession):
    level_labels = ['绿', '黄', '红', '紫', '白']
    regex = "随个((?:dx|sd|标准))?([绿黄红紫白]?)([0-9]+\+?)"
    res = re.match(regex, str(session.current_arg_text).lower())
    try:
        if res.groups()[0] == "dx":
            tp = ["DX"]
        elif res.groups()[0] == "sd" or res.groups()[0] == "标准":
            tp = ["SD"]
        else:
            tp = ["SD", "DX"]
        level = res.groups()[2]
        if res.groups()[1] == "":
            music_data = total_list.filter(level=level, type=tp)
        else:
            music_data = total_list.filter(level=level, diff=['绿黄红紫白'.index(res.groups()[1])], type=tp)
        if len(music_data) == 0:
            rand_result = "没有这样的乐曲哦。"
        else:
            rand_result = song_txt(music_data.random())
        await session.send(rand_result)
    except Exception as e:
        print(e)
        await session.send("随机命令错误，请检查语法")


@on_command('query_chart', only_to_me=False, aliases={r"^([绿黄红紫白]?)id([0-9]+)"})
async def query_chart(session: CommandSession):
    regex = "([绿黄红紫白]?)id([0-9]+)"
    groups = re.match(regex, str(session.current_arg_text)).groups()
    level_labels = ['绿', '黄', '红', '紫', '白']
    if groups[0] != "":
        try:
            level_index = level_labels.index(groups[0])
            level_name = ['Basic', 'Advanced', 'Expert', 'Master', 'Re: MASTER']
            name = groups[1]
            music = total_list.by_id(name)
            chart = music['charts'][level_index]
            ds = music['ds'][level_index]
            level = music['level'][level_index]
            file = f"https://www.diving-fish.com/covers/{music['id']}.jpg"
            if len(chart['notes']) == 4:
                msg = f'''{level_name[level_index]} {level}({ds})
TAP: {chart['notes'][0]}
HOLD: {chart['notes'][1]}
SLIDE: {chart['notes'][2]}
BREAK: {chart['notes'][3]}
谱师: {chart['charter']}'''
            else:
                msg = f'''{level_name[level_index]} {level}({ds})
TAP: {chart['notes'][0]}
HOLD: {chart['notes'][1]}
SLIDE: {chart['notes'][2]}
TOUCH: {chart['notes'][3]}
BREAK: {chart['notes'][4]}
谱师: {chart['charter']}'''
            await session.send([
                {
                    "type": "text",
                    "data": {
                        "text": f"{music['id']}. {music['title']}\n"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": f"{file}"
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": msg
                    }
                }
            ])
        except Exception:
            await query_chart.send("未找到该谱面")
    else:
        name = groups[1]
        music = total_list.by_id(name)
        try:
            file = f"https://www.diving-fish.com/covers/{music['id']}.jpg"
            await session.send([
                {
                    "type": "text",
                    "data": {
                        "text": f"{music['id']}. {music['title']}\n"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": f"{file}"
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": f"艺术家: {music['basic_info']['artist']}\n分类: {music['basic_info']['genre']}\nBPM: {music['basic_info']['bpm']}\n版本: {music['basic_info']['from']}\n难度: {'/'.join(music['level'])}"
                    }
                }
            ])
        except Exception:
            await session.send("未找到该乐曲")

music_aliases = defaultdict(list)
f = open('C:/dragonbot/Code/DragonBot/plugins/maimai/src/static/aliases.csv', 'r', encoding='utf-8')
tmp = f.readlines()
f.close()
for t in tmp:
    arr = t.strip().split('\t')
    for i in range(len(arr)):
        if arr[i] != "":
            music_aliases[arr[i].lower()].append(arr[0])


@on_command('find_song', only_to_me=False, aliases={r"(.+)是什么歌",})
async def find_song(session: CommandSession):
    regex = "(.+)是什么歌"
    name = re.match(regex, str(session.current_arg_text)).groups()[0].strip().lower()
    if name not in music_aliases:
        await session.send("未找到此歌曲\n舞萌 DX 歌曲别名收集计划：https://docs.qq.com/sheet/DQ0pvUHh6b1hjcGpl")
        return
    result_set = music_aliases[name]
    if len(result_set) == 1:
        music = total_list.by_title(result_set[0])
        await session.send("您要找的是不是")
        await session.send(song_txt(music))
    else:
        s = '\n'.join(result_set)
        await find_song.finish(f"您要找的可能是以下歌曲中的其中一首：\n{ s }")

wm_list = ['拼机', '推分', '越级', '下埋', '夜勤', '练底力', '练手法', '打旧框', '干饭', '抓绝赞', '收歌']


@on_command('maitoday', only_to_me=False, aliases={"今日舞萌",'今日mai'})
async def maitoday(session: CommandSession):
    qq = int(session.ctx.sender['user_id'])
    h = hash(qq)
    rp = h % 100
    wm_value = []
    for i in range(11):
        wm_value.append(h & 3)
        h >>= 2
    s = f"今日人品值：{rp}\n"
    for i in range(11):
        if wm_value[i] == 3:
            s += f'宜 {wm_list[i]}\n'
        elif wm_value[i] == 0:
            s += f'忌 {wm_list[i]}\n'
    s += "G11提醒您：打机时不要大力拍打或滑动哦\n今日推荐歌曲："
    music = total_list[h % len(total_list)]
    await session.send(s)
    await session.send(song_txt(music))

#https://www.diving-fish.com/api/maimaidxprober/player/records
@on_command('all_songs', only_to_me=False, aliases={})
async def all_songs(session: CommandSession):
    username = ""
    if session.current_arg_text[0:3] != "b40":
        return
    if len(session.current_arg_text) > 4:
        username = session.current_arg_text[4:]
    print(username, session.ctx.sender['user_id'])
    if username == "":
        payload = {'qq': session.ctx.sender['user_id']}
    else:
        payload = {'username': username}

@on_command('best_40_pic', only_to_me=False, aliases={})
async def best_40_pic(session: CommandSession):
    username = ""
    if session.current_arg_text[0:3] != "b40":
        return
    if len(session.current_arg_text) > 4:
        username = session.current_arg_text[4:]
    print(username, session.ctx.sender['user_id'])
    if username == "":
        payload = {'qq': session.ctx.sender['user_id']}
    else:
        payload = {'username': username}
    img, success = await generate(payload)
    if success == 400:
        await session.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。https://www.diving-fish.com/maimaidx/prober/")
    elif success == 403:
        await session.send("该用户禁止了其他人获取数据。")
    else:
        name = 'C:/dragonbot/gohttp/data/images/maiuser/'+str(session.ctx.sender['user_id'])+'.png'
        img.save(name)
        print("[CQ:image,file=maiuser/"+str(session.ctx.sender['user_id'])+".png]")
        await session.send("[CQ:image,file=maiuser/"+str(session.ctx.sender['user_id'])+".png]")


@on_command('query_score', only_to_me=False, aliases={'分数线'})
async def query_score(session: CommandSession):
    r = "([绿黄红紫白])(id)?([0-9]+)"
    argv = session.current_arg_text.split(" ")
    print(argv)
    if len(argv) == 1 and argv[0] == '帮助':
        s = '''此功能为查找某首歌分数线设计。
命令格式：分数线 <难度+歌曲id> <分数线>
例如：分数线 紫799 100
命令将返回分数线允许的 TAP GREAT 容错以及 BREAK 50落等价的 TAP GREAT 数。
以下为 TAP GREAT 的对应表：
GREAT/GOOD/MISS
TAP\t1/2.5/5
HOLD\t2/5/10
SLIDE\t3/7.5/15
TOUCH\t1/2.5/5
BREAK\t5/12.5/25(外加200落)'''
        await session.send([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(text_to_image(s)), encoding='utf-8')}"
            }
        }])
    elif len(argv) == 2:
        try:
            grp = re.match(r, argv[0]).groups()
            level_labels = ['绿', '黄', '红', '紫', '白']
            level_labels2 = ['Basic', 'Advanced', 'Expert', 'Master', 'Re:MASTER']
            level_index = level_labels.index(grp[0])
            chart_id = grp[2]
            line = float(argv[1])
            music = total_list.by_id(chart_id)
            chart: Dict[Any] = music['charts'][level_index]
            tap = int(chart['notes'][0])
            slide = int(chart['notes'][2])
            hold = int(chart['notes'][1])
            touch = int(chart['notes'][3]) if len(chart['notes']) == 5 else 0
            brk = int(chart['notes'][-1])
            total_score = 500 * tap + slide * 1500 + hold * 1000 + touch * 500 + brk * 2500
            break_bonus = 0.01 / brk
            break_50_reduce = total_score * break_bonus / 4
            reduce = 101 - line
            if reduce <= 0 or reduce >= 101:
                raise ValueError
            await session.send(f'''{music['title']} {level_labels2[level_index]}
分数线 {line}% 允许的最多 TAP GREAT 数量为 {(total_score * reduce / 10000):.2f}(每个-{10000 / total_score:.4f}%),
BREAK 50落(一共{brk}个)等价于 {(break_50_reduce / 100):.3f} 个 TAP GREAT(-{break_50_reduce / total_score * 100:.4f}%)''')
        except Exception:
            await session.send("格式错误，输入“分数线 帮助”以查看帮助信息")


@on_command('search_music', only_to_me=False, aliases={"查歌"})
async def search_music(session: CommandSession):
    name = str(session.current_arg_text)
    if name == "":
        return
    res = total_list.filter(title_search=name)
    if len(res) == 0:
        await session.send("没有找到这样的乐曲。")
    elif len(res) < 50:
        search_result = ""
        for music in sorted(res, key = lambda i: int(i['id'])):
            search_result += f"{music['id']}. {music['title']}\n"
        await session.send([
            {"type": "text",
                "data": {
                    "text": search_result.strip()
                }}])
    else:
        await session.send(f"结果过多（{len(res)} 条），请缩小查询范围。")


@on_command('calc_rating', only_to_me=False, aliases={"rating"})
async def calc_rating(session: CommandSession):
    ds = eval(session.current_arg_text)
    await session.send(f"SSS+:{computeRa(ds,100.5)}\nSSS MAX:{computeRa(ds,100.49)}, MIN:{computeRa(ds,100)}\nSS+ MAX:{computeRa(ds,99.99)}, MIN:{computeRa(ds,99.5)}\nSS MAX:{computeRa(ds,99.49)}, MIN:{computeRa(ds,99)}\nS+ MAX:{computeRa(ds,98.99)}, MIN:{computeRa(ds,98)}\nS MAX:{computeRa(ds,97.99)}, MIN:{computeRa(ds,97)}")


@on_natural_language(only_to_me=False, keywords={'b40',})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    pos = stripped_msg
    return IntentCommand(100.0, 'best_40_pic', current_arg=pos)

@on_natural_language(only_to_me=False, keywords={'游玩记录',})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    pos = stripped_msg
    return IntentCommand(100.0, 'all_songs', current_arg=pos)


@on_natural_language(only_to_me=False, keywords={'是什么歌',})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    pos = stripped_msg
    return IntentCommand(100.0, 'find_song', current_arg=pos)


@on_natural_language(only_to_me=False, keywords={'随个',})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    pos = stripped_msg
    return IntentCommand(100.0, 'spec_rand', current_arg=pos)


@on_natural_language(only_to_me=False, keywords={'id',})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    pos = stripped_msg
    return IntentCommand(100.0, 'query_chart', current_arg=pos)
