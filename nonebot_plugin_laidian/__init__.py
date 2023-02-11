from nonebot.plugin import on_command, on_regex
from nonebot.exception import ActionFailed
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (Message, 
    MessageSegment, 
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PRIVATE_FRIEND,
    GROUP)
from .withdraw import add_withdraw_job
from nonebot.matcher import Matcher
from nonebot import require
from nonebot.params import Arg, CommandArg
from asyncio import sleep
from typing import List
from re import sub, I
require("nonebot_plugin_imageutils")
from nonebot_plugin_imageutils import Text2Image
from io import BytesIO
import nonebot
import httpx
import requests
import json
import random

#获取配置
config = nonebot.get_driver().config
#机器人名字，请在.env中配置bot_nickname,不配置默认"脑积水"
Bot_NICKNAME: str = getattr(config, "bot_nickname", "脑积水")

miao = on_command("来点猫猫", aliases={"随机猫猫", "来点喵咪", "来个猫咪", "随机猫咪", "来个猫猫"}, block=True)
erciyuan = on_command("来点二次元", aliases={'来张二次元', '二次元'}, block=True)
bizhi = on_command("来点壁纸", aliases={'来张壁纸', '壁纸'}, block=True)
help = on_command('来点帮助', aliases={'来点help'}, block=True)
maijia = on_regex(r"^(来点买家秀)\s?([x|✖️|×|X|*]?\d+[张|个|份]?)?", flags=I)
bing = on_command('来点bing', aliases={'来张bing', '随机bing图', '随机必应图'}, block=True)
bizhi_er = on_command('来点二次元壁纸', aliases={'来张二次元壁纸', '二次元壁纸'}, block=True)
setu = on_regex(r"^(来点p图)\s?([x|*]?\d+[张|个|份]?)?", flags=I)
cos = on_command('来点cos', aliases={'cos', 'cos图', 'cosplay', '来张cos'}, block=False, priority=5)
douyin = on_command('来点抖音', aliases={'抖音', '随机抖音', '小姐姐'}, priority=5)
douyin2 = on_command('来点小姐姐', aliases={'woc'}, block=False, priority=5)
touxiang = on_command('来点女头', aliases={'女生头像', '随机女头'}, block=False, priority=5)
yuanshen = on_command('原神壁纸', aliases={'来点原神壁纸'}, block=False, priority=5)
meizi = on_command('来点妹子', aliases={'来点腿子', '美腿'}, block=False, priority=5)
suangua = on_command('算卦', aliases={'算一卦', '来一卦'}, block=False, priority=5)
hushuo = on_command('胡说八道', aliases={'胡言乱语', '写文章'}, block=False, priority=5)
heji = on_command('壁纸合集', aliases={'合集图片', '图片合集'}, block=False, priority=5)
yuyin = on_command('语音点歌', block=False, priority=5)
suijivideo = on_command('随机视频', block=False, priority=5)
zcos = on_command('cos正片', block=False, priority=5)
history = on_command('历史上的今天', aliases={'历史上的今日'}, block=False, priority=5)
suijierci = on_command('随机二次元', aliases={'ecy'}, block=False, priority=5)
r18 = on_regex(r"^(秘密森林)\s?([x|✖️|×|X|*]?\d+[张|个|份]?)?", flags=I, permission=PRIVATE_FRIEND | GROUP)
soutu = on_command('p搜图', aliases={'p站搜图'}, block=False, priority=6)
shua_vedio = on_command('刷视频', block=False, priority=6)
tts = on_regex(r"^(tts)+(\s)?(.*)",flags=I)#tts文字转语音
handsome = on_regex(r"^来点(帅哥|(小)?哥哥)(短)?(视频)?$",flags=I,priority=5)
beauty = on_regex(r"^来点(美女|姐姐)(短)?(视频)?$",flags=I,priority=5)
@beauty.handle()
async def _():
    vedio = requests.get(url="https://zj.v.api.aa1.cn/api/video_dyv2").text
    if not vedio:
        await beauty.finish("接口寄了")
    vedio_url= json.loads(vedio)['url']
    await beauty.send("稍等片刻，请勿重复指令")
    await handsome.finish(MessageSegment.video(vedio_url))

@handsome.handle()
async def _():
    vedio = requests.get(url="https://zj.v.api.aa1.cn/api/video_dyv1").text
    if not vedio:
        await handsome.finish("接口寄了")
    vedio_url = json.loads(vedio)['url']
    await handsome.send("稍等片刻，请勿重复指令")
    await handsome.finish(MessageSegment.video(vedio_url))




@tts.handle()
async def _(bot:Bot,state:T_State,event:MessageEvent):
    args = list(state["_matched_groups"])
    text = args[2]
    msg = f"[CQ:tts,text={text}]" if len(text) <= 50 else await tts.finish("超出50字符，默认取消")
    if msg:
        try:
            await tts.send(Message(msg))
        except Exception:
            await tts.finish("tts转换出错了")

@shua_vedio.handle()
async def _():
    await shua_vedio.send(message=f'{Bot_NICKNAME}正在刷视频……', at_sender=True)
    try:
        get_json = requests.get(url='http://ovooa.com/API/nowKuai/?type=json').text
    except:
        await shua_vedio.finish(message=f'{Bot_NICKNAME}请求超时了', at_sender=True)
    get_json = json.loads(get_json)['data']
    all_ifm = random.choice(get_json)
    author = all_ifm['author']['name']
    caption = all_ifm['data']['caption']
    mp4 = all_ifm['data']['photoUrl']
    try:
        await shua_vedio.send(message=f"⭐作者:{author}\n⭐标题:{caption}")
        await shua_vedio.send(MessageSegment.video(file=mp4))
    except:
        await shua_vedio.finish(message=f'{Bot_NICKNAME}出错了，格式不正确', at_sender=True)


@soutu.handle()
async def _(match: Matcher, args: Message = CommandArg()):
    args = str(args)  # 去除命令文字
    if args:
        match.set_arg('keyword', args)
    else:
        await soutu.send(message='本搜索图源来自p站', at_sender=True)


@soutu.got('keyword', prompt=f"请告诉{Bot_NICKNAME}关键词吧")
async def got_keyword(bot: Bot, event: MessageEvent, keyword: Message = Arg()):
    msg_list: List[Message] = []
    msg_list.insert(0, f'{Bot_NICKNAME}找到图片如下')
    async with httpx.AsyncClient(follow_redirects=True) as c:
        url = 'https://image.anosu.top/pixiv/direct?keyword=' + str(keyword).replace(r"amp;amp;", '')
        try:
            image = await c.get(url=url)
            msg_list.append(MessageSegment.image(image.content))
        except:
            await soutu.send(message=f'请求超时了，或者你输入的关键词不符合规范:{keyword}', at_sender=True)
        try:
            await send_forward_msg(bot, event, f'搜图{Bot_NICKNAME}', 2854196306, msg_list)
        except ActionFailed as e:
            await soutu.finish(message=f'账户风控了或者图片格式错误:{e.__context__}')


@r18.handle()
async def _(state: T_State, bot: Bot, event: MessageEvent):
    await r18.send(message='触发神秘空间……', at_sender=True)
    msg_list: List[Message] = []
    msg_list.insert(0, f'{Bot_NICKNAME}提醒你，请不要随便告诉他人这个神秘空间')
    args = list(state["_matched_groups"])
    num = args[1]
    num = int(sub(r"[张|个|份|x|✖️|×|X|*]", "", num)) if num else 1
    num = 7 if num >= 7 else num
    json_get = requests.get(url=f"https://moe.jitsu.top/img/?sort=r18&size=original&type=json&num={num}").text
    json_get = json.loads(json_get)['pics']
    for key in json_get:
        msg_list.append(MessageSegment.image(key))
    try:
        msg_info = await send_forward_msg(bot, event, "未知领域", 2854196306, msg_list)
        add_withdraw_job(bot, **msg_info)
    except:
        await r18.finish(message='出错了或者账户风控了', at_sender=True)


@suijierci.handle()
async def _(bot: Bot, event: MessageEvent):
    await suijierci.send(message=f'{Bot_NICKNAME}正在寻找二次元中……', at_sender=True)
    msg_list: List[Message] = []
    msg_list.insert(0, f'客官，{Bot_NICKNAME}找到二次元如下')
    json_get = requests.get(url='https://moe.anosu.top/img/?num=5').text
    json_get = json.loads(json_get)['pics']
    for key in json_get:
        msg_list.append(MessageSegment.image(key))
    try:
        await send_forward_msg(bot, event, f"二次元{Bot_NICKNAME}", 2854196306, msg_list)
    except:
        await suijierci.finish(message='出错了或者账户风控了', at_sender=True)


@history.handle()
async def _():
    await history.send(message=f'{Bot_NICKNAME}正在查询历史上的今天……', at_sender=True)
    try:
        await history.send(MessageSegment.image(file='https://xiaoapi.cn/API/lssdjt_pic.php'))
    except ActionFailed:
        await history.finish(message=f'{Bot_NICKNAME}请求超时了，请及时联系管理员', at_sender=True)


@zcos.handle()
async def _(bot: Bot, event: MessageEvent):
    await zcos.send(message=f'诶？诶{Bot_NICKNAME}马上找找……,可能很慢，请稍等哦~', at_sender=True)
    get_json = json.loads(requests.get(url='http://ovooa.com/API/cosplay/api.php').text)['data']
    title = get_json['Title']
    data = get_json['data']
    msg_list: List[Message] = []
    msg_list.insert(0, title)
    try:
        for num in range(1, 11):
            msg_list.append(MessageSegment.image(file=data[num]))
    except:
        await zcos.send(message='超出数据范围，请重新发送')
    try:
        await send_forward_msg(bot, event, f"{Bot_NICKNAME}", 2854196306, msg_list)
    except ActionFailed as e:
        await zcos.finish(message='出错了或者账户风控了', at_sender=True)


@suijivideo.handle()
async def sui(match: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text()  # 去除命令文字
    if args:
        match.set_arg('type', args)
    else:
        await suijivideo.send(message='明星/热舞/风景/游戏/动物/动漫。默认动漫', at_sender=True)


@suijivideo.got('type', prompt=f"请告诉{Bot_NICKNAME}视频类型吧~")
async def get_type(event: MessageEvent, type: Message = Arg()):
    if str(type) in ['明星', '热舞', '风景', '游戏', '动漫', '动物']:
        url = 'http://ovooa.com/API/sjsp/api.php?msg=' + str(type)
        await suijivideo.send(message=f'{Bot_NICKNAME}正在寻找中……')
    else:
        await suijivideo.finish("没有你所说的类型,请重新说“随机视频”", at_sender=True)
    mp4 = json.loads(requests.get(url=url).text)['data']['url']
    try:
        await suijivideo.send(MessageSegment.video(mp4))
    except ActionFailed as e:
        await suijivideo.finish(message='出错了,未知情况', at_sender=True)


@yuyin.handle()
async def gta(match: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text()  # 去除命令文字
    if args:
        match.set_arg('name', args)  # 如命令后有文字赋值加入


@yuyin.got("name", prompt=f'请把歌名交给{Bot_NICKNAME}吧~')
async def handle_music(state: T_State, name: Message = Arg()):
    state['name'] = str(name)
    if not state['name']:
        await yuyin.reject('歌名格式错误，或者没有找到歌名，请重新输入歌名', at_sender=True)
    state['url'] = 'http://ovooa.com/API/yydg/api.php?msg=' + str(state['name'])
    await yuyin.send(requests.get(state['url']).text, at_sender=True)


@yuyin.got("n", prompt=f'请发送歌名的序号给{Bot_NICKNAME}')
async def getmusic(state: T_State, event: MessageEvent):
    state['url'] = state['url'] + "&n=" + str(event.get_message())
    try:
        state['music'] = json.loads(requests.get(url=state['url']).text)['data']['url']
    except:
        await yuyin.reject('出错了，没有找到对应的歌曲或者你输入的数字不正确，请重新输入序号', at_sender=True)


@yuyin.handle()
async def _(state: T_State):
    await yuyin.send(message=f'{Bot_NICKNAME}正在寻找歌曲中……', at_sender=True)
    async with httpx.AsyncClient() as client:
        mp3 = await client.get(url=state['music'])
    try:
        await yuyin.send(MessageSegment.record(mp3.content))
    except:
        await yuyin.finish(message='出错了，语音格式不正确', at_sender=True)


@heji.handle()
async def ll(match: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text()  # 去除命令文字
    if args:
        match.set_arg('type', args)
    else:
        await heji.send(message='1是美女壁纸  2是动漫壁纸  3是风景壁纸  4是游戏壁纸  5是文字壁纸  6是视觉壁纸  7是情感壁纸  8是设计壁纸  9是明星壁纸  10是物语壁纸',
                        at_sender=True)


@heji.got("type", prompt=f"请发送类型数字给{Bot_NICKNAME}吧")
async def get_type(state: T_State, event: MessageEvent, type: Message = Arg()):
    if str(type) in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        state['url'] = 'http://ovooa.com/API/bizhi/api.php?msg=' + str(type)
    else:
        await heji.reject(f'数字不正确，请输入1-10的数字给{Bot_NICKNAME}吧~', at_sender=True)
    try:
        await heji.send(message=f'{Bot_NICKNAME}正在寻找壁纸中……', at_sender=True)
        imge = requests.get(url=state['url']).text
    except:
        await heji.finish(message='请求超时了，请重试吧', at_sender=True)
    try:
        await heji.send(MessageSegment.image(json.loads(imge)['url']))
    except ActionFailed as e:
        await heji.finish(message=f"出错了，可能是消息格式出错或者账户风控了{e}", at_sender=True)


@hushuo.handle()
async def hu(match: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text()  # 去除命令文字
    if args:
        match.set_arg('name', args)  # 如命令后有文字赋值加入


@hushuo.got("name", prompt=f"请发送主角名字给{Bot_NICKNAME}吧")
async def got_name(state: T_State, name: Message = Arg()):
    if str(name):
        url = 'http://ovooa.com/API/dog/api.php?msg=' + name
    else:
        await hushuo.reject('主角名字错误，请从新输入吧~', at_sender=True)
    params = {
        'num': '200',
        'type': 'text'
    }
    try:
        state['message'] = requests.get(url=url, params=params).text
    except:
        await hushuo.finish(message=f'{Bot_NICKNAME}请求出错了，请联系管理员', at_sender=True)


@hushuo.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    try:
        await hushuo.send(state['message'], at_sender=True)
    except:
        await hushuo.finish(message='出错了，可能是消息格式出错或者账户风控了', at_sender=True)


@suangua.handle()
async def _():
    await suangua.send(message=f'{Bot_NICKNAME}为你算一卦~', at_sender=True)
    try:
        json_get = requests.get(url='http://ovooa.com/API/chouq/api.php').text
    except:
        await suangua.finish(message='请求出错了，请及时联系管理员', at_sender=True)
    title = json.loads(json_get)['data']['draw']
    messgae = ('⭐' + json.loads(json_get)['data']['annotate'] + '⭐\n⭐'
               + json.loads(json_get)['data']['explain'] + '\n⭐'
               + json.loads(json_get)['data']['explain'] + '\n⭐'
               + json.loads(json_get)['data']['details'])
    image = json.loads(json_get)['data']['image']
    await suangua.send(messgae)
    await suangua.finish(MessageSegment.image(image))


@meizi.handle()
async def _():
    await meizi.send(message=f'{Bot_NICKNAME}正在寻找妹子')
    try:
        img = json.loads(requests.get(url='http://ovooa.com/API/meizi/api.php').text)['text']
        await meizi.send(MessageSegment.image(img))
        await meizi.send(message="你要的美腿~（弱弱一句）：lsp！", at_sender=True)
    except:
        await meizi.finish(message='出错了，可能是消息格式出错或者账户风控了')


@yuanshen.handle()
async def _(bot: Bot, event: MessageEvent):
    await yuanshen.send(message=f'{Bot_NICKNAME}正在寻找派蒙中……')
    try:
        get_json = requests.get(url='http://ovooa.com/API/yuan/api?type=text').text
    except:
        await yuanshen.finish(message='请求超时了，请及时联系管理员', at_sender=True)
    try:
        await yuanshen.send(MessageSegment.image(get_json))
        await yuanshen.send(message=f"喏~", at_sender=True)
    except:
        await yuanshen.finish(message='出错了，可能是消息格式出错或者账户风控了')


@touxiang.handle()
async def _(bot: Bot, event: MessageEvent):
    await touxiang.send(message=f'{Bot_NICKNAME}正在寻找头像中……')
    try:
        get_ifm = requests.get(url='https://v.api.aa1.cn/api/api-tx/index.php?wpon=json').text
    except:
        await touxiang.finish(message=f'请求超时了，{Bot_NICKNAME}没有找到头像。', at_sender=True)
    get_json = get_ifm[get_ifm.rfind('{'):]
    url = 'https:' + json.loads(get_json)['img']
    async with httpx.AsyncClient(follow_redirects=True) as client:
        img = await client.get(url=url)
    try:
        await touxiang.send(MessageSegment.image(img.content))
        await touxiang.finish(message='客官，你要的头像', at_sender=True)
    except ActionFailed as e:
        await touxiang.finish(message=f"{Bot_NICKNAME}出错了！{e}")


@douyin2.handle()
async def _(bot: Bot, event: MessageEvent):
    await douyin2.send(message=f'{Bot_NICKNAME}正在刷视频……')
    try:
        img = requests.get(url='https://tucdn.wpon.cn/api-girl/index.php?wpon=json').text
    except:
        await douyin2.finish(message="请求超时了，没有找到神秘东西。", at_sender=True)
    img = json.loads(img)['mp4']
    img = 'https:' + str(img)
    try:
        await douyin.send(MessageSegment.video(img))
        await douyin.finish(message='喏~', at_sender=True)
    except ActionFailed as e:
        await douyin.finish(message=f"出错了,{e}", at_sender=True)


@douyin.handle()
async def _(bot: Bot, event: MessageEvent):
    await douyin.send(message=f'{Bot_NICKNAME}正在寻找小姐姐……')
    try:
        url = 'https://v.api.aa1.cn/api/api-dy-girl/index.php?aa1=json'
        get_img = requests.get(url=url, timeout=30).text
    except:
        await douyin.finish(message=f'请求失败了，{Bot_NICKNAME}没有找到视频qwq', at_sender=True)
    img = json.loads(get_img)['mp4']
    img = img.replace(" ", "%20")
    img = 'https:' + img
    try:
        await douyin.send(MessageSegment.video(img))
        await douyin.finish(message='喏~', at_sender=True)
    except ActionFailed as e:
        await douyin.finish(message=f"{e}", at_sender=True)


@cos.handle()
async def _(bot: Bot, event: MessageEvent, i=1):
    await cos.send(message=f'{Bot_NICKNAME}正在寻找cosplayer中……')
    msg_list: List[Message] = []
    msg_list.insert(0, f'客官,{Bot_NICKNAME}找到coser如下')
    heads = {
        'uer-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    while i <= 5:
        i += 1
        img = requests.get(url='http://121.40.95.21/api/cos.php', headers=heads).text
        msg_list.append(MessageSegment.image(file=(img.replace('\n', ''))))
        await sleep(0.5)
    try:
        await send_forward_msg(bot, event, f"cos{Bot_NICKNAME}", 2854196306, msg_list)
    except ActionFailed as e:
        await cos.finish(message='账户风控了，或格式出错了', at_sender=True)


@help.handle()
async def hp(bot: Bot, event: MessageEvent, state: T_State):

    image = f"⭐{Bot_NICKNAME}一些来点图片的帮助⭐\n\
🚪来点壁纸      🚪\n\
🚪来点二次元    🚪\n\
🚪来点猫猫      🚪\n\
🚪来点买家秀    🚪\n\
🚪来点bing      🚪\n\
🚪来点二次元壁纸 🚪\n\
🚪来点p图       🚪\n\
🚪来点cos       🚪\n\
🚪来点抖音      🚪\n\
🚪来点小姐姐    🚪\n\
🚪来点女头      🚪\n\
🚪来点原神壁纸  🚪\n\
🚪来点妹子      🚪\n\
🚪胡言乱语      🚪\n\
🚪算一卦        🚪\n\
🚪壁纸合集      🚪\n\
🚪语音点歌      🚪\n\
🚪随机视频      🚪\n\
🚪cos正片       🚪\n\
🚪历史上的今天  🚪\n\
🚪随机二次元    🚪\n\
🚪p搜图         🚪\n\
🚪刷视频        🚪\n\
🚪tts          🚪\n\
🚪来点帅哥          🚪\n\
🚪来点美女          🚪\n\
⭐更多功能还待完善⭐\n"
    image = Text2Image.from_text(image,30).to_image(bg_color="white")
    output = BytesIO()
    image.save(output,format="png")
    await help.send(MessageSegment.image(output))


async def get_ercibizhi():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        img_get = await client.get(url='https://api.yimian.xyz/img?type=moe&size=1920x1080', timeout=120)
    return img_get


@setu.handle()
async def p(state: T_State, bot: Bot, event: MessageEvent):
    await setu.send(message=f'{Bot_NICKNAME}正在寻找p图……')
    args = list(state["_matched_groups"])
    num = args[1]
    num = int(sub(r"^[x|*]", "", num)) if num else 2
    num = 5 if num >= 5 else num
    msg_list: List[Message] = []
    get_json = requests.get(url=f"http://sex.nyan.xyz/api/v2/?num={num}", timeout=60).text
    get_json = json.loads(get_json)
    date = get_json['data']
    if date:
        for key in date:
            url = key['url']
            tags = key['tags'][0] + ' ' + key['tags'][1] + ' ' + key['tags'][2] + ' ' + key['tags'][3]
            msg = tags + MessageSegment.image(url)
            msg_list.append(msg)
        try:
            await send_forward_msg(bot, event, f"{Bot_NICKNAME}", 2854196306, msg_list)
        except Exception: await setu.send("消息图片被风控了！")
    else:
        await setu.send("API寄了，正在切换API")
        get_ = requests.get(url=f"https://moe.jitsu.top/img/?sort=pixiv&num={num}", timeout=60).text
        get_ = json.loads(get_)
        dat = get_['pics']
        for key in dat:
            msg_list.append(MessageSegment.image(key))
        try:
            await send_forward_msg(bot, event, f"{event.sender.nickname or event.sender.card}", 2854196306, msg_list)
        except ActionFailed as e:
            await setu.finish(
            message=Message(f"消息被风控，{e} "),
            at_sender=True,
            )
        await sleep(2)


async def get_miao():
    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        img_get = await client.get(url='http://edgecats.net/', timeout=60, )
    return img_get


async def get_erciyuan():
    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        img_get = await client.get(url='http://api.ixiaowai.cn/api/api.php', timeout=60)
    return img_get


async def get_bizhi():
    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        img_get = await client.get(url='http://api.ixiaowai.cn/gqapi/gqapi.php', timeout=60)
    return img_get


async def maijia_get():
    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        get_img = await client.get(url='http://api.uomg.com/api/rand.img3', timeout=60)
    return get_img


async def get_bing():
    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        get_img = await client.get(url='http://api.yimian.xyz/img?type=wallpaper', timeout=60)
    return get_img


@bizhi_er.handle()
async def erbi(bot: Bot, event: MessageEvent, state: T_State):
    await bizhi_er.send(message=f'{Bot_NICKNAME}正在寻找二次元壁纸……')
    msg = await get_ercibizhi()
    try:
        await bizhi_er.send(MessageSegment.image(msg.content))
        await bizhi_er.send(message='成功了，找到一张壁纸！', at_sender=True)
    except:
        await bizhi_er.finish(message=f'{Bot_NICKNAME}失败了，请稍后重试')


@bing.handle()
async def bin(bot: Bot, event: MessageEvent, state: T_State):
    await bing.send(message=f'{Bot_NICKNAME}正在获取bing图……')
    msg = await get_bing()
    try:
        await bing.send(MessageSegment.image(msg.content))
        await bing.send(message='成功了！你要的bing图', at_sender=True)
    except:
        await bing.finish(message=f'{Bot_NICKNAME}请求失败了，请稍后重试', at_sender=True)


@bizhi.handle()
async def bz(bot: Bot, event: MessageEvent, state: T_State):
    await bizhi.send(message=f'{Bot_NICKNAME}正在寻找壁纸……')
    msg = await get_bizhi()
    try:
        await bizhi.send(MessageSegment.image(msg.content))
        await bizhi.send(message='客官，你要的壁纸~', at_sender=True)
    except:
        await bizhi.finish(message=f'{Bot_NICKNAME}没有找到壁纸')


@maijia.handle()
async def mj(bot: Bot, event: MessageEvent, state: T_State):
    msg_list: List[Message] = []
    msg_list.insert(0, '买家秀找到如下')
    args = list(state["_matched_groups"])
    num = args[1]
    num = int(sub(r"[张|个|份|x|✖️|×|X|*]", "", num)) if num else 1
    num = 7 if num >= 7 else num
    while num > 0:
        num -= 1
        msg_list.append(MessageSegment.image((await maijia_get()).content))
    try:
        await send_forward_msg(bot, event, f"买家秀{Bot_NICKNAME}", 2854196306, msg_list)
    except Exception:
        await maijia.finish(message=f'请求超时了，{Bot_NICKNAME}没有找到图片')


@erciyuan.handle()
async def erci(bot: Bot, event: MessageEvent, state: T_State):
    await erciyuan.send(message=f'{Bot_NICKNAME}正在寻找二次元……')
    msg = await get_erciyuan()
    try:
        await erciyuan.send(MessageSegment.image(msg.content))
        await erciyuan.send(message='客官，你要的二次元~', at_sender=True)
    except:
        await erciyuan.finish(message=f'{Bot_NICKNAME}没有找到二次元')


@miao.handle()
async def hf(bot: Bot, event: MessageEvent, state: T_State):
    await miao.send(message=f'{Bot_NICKNAME}正在寻找猫猫……')
    msg = await get_miao()
    try:
        await miao.send(MessageSegment.image(msg.content))
        await miao.send(message='客官，你要的猫猫~', at_sender=True)
    except:
        await miao.finish(message=f'{Bot_NICKNAME}没有找到猫猫，请求超时了')


async def send_forward_msg(
        bot: Bot,
        event: MessageEvent,
        name: str,
        uin: str,
        msgs: List[Message],
) -> dict:
    def to_json(msg: Message):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    if isinstance(event, GroupMessageEvent):
        return await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        return await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
