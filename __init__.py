from nonebot.plugin import on_command
from nonebot.exception import ActionFailed
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot, MessageEvent, GroupMessageEvent
from .withdraw import add_withdraw_job
from nonebot_plugin_guild_patch import GuildMessageEvent
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg
from nonebot.log import logger
from asyncio import sleep
from typing import List
import httpx
import requests 
import json
import random

miao = on_command("来点猫猫", aliases={"随机猫猫","来点喵咪","来个猫咪","随机猫咪","来个猫猫"}, block=True)
erciyuan= on_command("来点二次元",aliases={'来张二次元','二次元'},block=True)
bizhi= on_command("来点壁纸",aliases={'来张壁纸','壁纸'},block=True)
help= on_command('来点帮助',aliases={'来点help'},block=True)
maijia=on_command('买家秀', aliases={'来点买家秀','来张买家秀','tb买家秀'},block=True)
bing=on_command('来点bing',aliases={'来张bing','随机bing图','随机必应图'},block=True)
bizhi_er=on_command('来点二次元壁纸',aliases={'来张二次元壁纸','二次元壁纸'},block=True)
setu = on_command('来点涩图',aliases={'来张涩图','来点色图','随机涩图','随机色图','随机p图','来点p图','来张p图'},block=False)
cos = on_command('来点cos',aliases={'cos','cos图','cosplay','来张cos'}, block=False, priority=5)
douyin = on_command('来点抖音',aliases={'抖音','随机抖音','小姐姐'},priority=5)
douyin2 = on_command('来点小姐',aliases={'woc','卧槽'}, block=False, priority=5)
touxiang = on_command('来点女头', aliases={'女生头像','随机女头'}, block=False, priority=5)
yuanshen = on_command('原神壁纸',aliases={'来点原神壁纸'},block=False,priority= 5)
meizi = on_command('来点妹子',aliases={'来点腿子','美腿'}, block=False,priority=5)
suangua = on_command('算卦',aliases={'算一卦','来一卦'},block=False,priority=5)
hushuo = on_command('胡说八道',aliases={'胡言乱语','写文章'},block=False,priority=5)
heji = on_command('壁纸合集',aliases={'合集图片','图片合集'},block=False,priority=5)
yuyin = on_command('语音点歌',block=False,priority=5)
suijivideo = on_command('随机视频',block=False, priority=5)
zcos = on_command('cos正片',block=False,priority=5)
history = on_command('历史上的今天',aliases={'历史上的今日'},block=False,priority=5)
suijierci = on_command('随机二次元',aliases={'ecy'},block=False,priority = 5)
r18 = on_command('神秘空间',aliases={'秘密森林'},block=False,priority=5)
soutu = on_command('p搜图',aliases={'p站搜图'},block=False, priority=6)
shua_vedio = on_command('刷视频',block=False,priority=6)

@shua_vedio.handle()
async def _(event:MessageEvent):
    if isinstance(event,GuildMessageEvent):
        await shua_vedio.finish("可可酱该功能暂不适配频道")
    await shua_vedio.send(message='可可酱正在刷视频……',at_sender=True)
    try:
        get_json = requests.get(url = 'http://ovooa.com/API/nowKuai/?type=json').text
    except:
        await shua_vedio.finish(message='可可酱请求超时了',at_sender=True)
    get_json = json.loads(get_json)['data']
    all_ifm = random.choice(get_json)
    author = all_ifm['author']['name']
    caption = all_ifm['data']['caption']
    mp4 = all_ifm['data']['photoUrl']
    try:
        await shua_vedio.send(message=f"⭐作者:{author}\n⭐标题:{caption}")
        await shua_vedio.send(MessageSegment.video(file=mp4))
    except:
        await shua_vedio.finish(message='可可酱出错了，格式不正确',at_sender=True)


@soutu.handle()
async def _(match:Matcher,args:Message = CommandArg()):
    args = str(args)#去除命令文字
    if args:
        match.set_arg('keyword',args)
    else:
        await soutu.send(message='本搜索图源来自p站',at_sender=True)

@soutu.got('keyword',prompt="请告诉可可酱关键词吧")
async def got_keyword(bot:Bot, event:MessageEvent, keyword:Message = Arg()):
    msg_list:List[Message]=[]
    msg_list.insert(0,'可可酱找到图片如下')
    async with httpx.AsyncClient(follow_redirects=True) as c:
        url ='https://image.anosu.top/pixiv/direct?keyword='+str(keyword).replace(r"amp;amp;",'')
        try:
            image = await c.get(url=url)
            msg_list.append(MessageSegment.image(image.content))
        except:
            await soutu.send(message=f'请求超时了，或者你输入的关键词不符合规范:{keyword}',at_sender=True)
        try:
            if not isinstance(event,GuildMessageEvent):
                await send_forward_msg(bot,event,'搜图可可酱',bot.self_id,msg_list)
            else: 
                await soutu.send(msg_list[1])
        except ActionFailed as e:
            await soutu.finish(message=f'账户风控了或者图片格式错误:{e.__context__}')


@r18.handle()
async def _(bot:Bot, event:MessageEvent):
    await r18.send(message='触发神秘空间……',at_sender=True)
    if isinstance(event,GuildMessageEvent):
        await r18.finish("该功能不适配频道哦~",at_sender=True)
    msg_list:List[Message]=[]
    msg_list.insert(0,'可可酱提醒你，请不要随便告诉他人这个神秘空间')
    json_get = requests.get(url='https://moe.jitsu.top/img/?sort=r18&size=original&type=json&num=4').text
    json_get = json.loads(json_get)['pics']
    for key in json_get:
        msg_list.append(MessageSegment.image(key))
    try:
        msg_info = await send_forward_msg(bot, event, "未知领域", bot.self_id, msg_list)
        add_withdraw_job(bot, **msg_info)
    except:
        await r18.finish(message='出错了或者账户风控了',at_sender=True)


@suijierci.handle()
async def _(bot:Bot, event:MessageEvent):
    await suijierci.send(message='可可酱正在寻找二次元中……',at_sender=True)
    msg_list:List[Message]=[]
    msg_list.insert(0,'客官，可可酱找到二次元如下')
    json_get = requests.get(url='https://moe.anosu.top/img/?num=5').text
    json_get = json.loads(json_get)['pics']
    for key in json_get:       
        msg_list.append(MessageSegment.image(key))
    try:
        if isinstance(event,GuildMessageEvent):
            for num in msg_list:
                await suijierci.send(num)
        else:
            await send_forward_msg(bot, event, "二次元可可酱", bot.self_id, msg_list)
    except:
        await suijierci.finish(message='出错了或者账户风控了',at_sender=True)

@history.handle()
async def _(event:MessageEvent):
    await history.send(message='可可酱正在查询历史上的今天……',at_sender=True)
    try:
        await history.send(MessageSegment.image(file='https://xiaoapi.cn/API/lssdjt_pic.php'))
    except:
        await history.finish(message='可可酱请求超时了，请及时联系管理员',at_sender=True)


@zcos.handle()
async def _(bot:Bot,event:MessageEvent):
    await zcos.send(message='诶？诶！可可酱马上找找……,可能很慢，请稍等哦~',at_sender=True)
    get_json = json.loads(requests.get(url='http://ovooa.com/API/cosplay/api.php').text)['data']
    title = get_json['Title']
    data = get_json['data']
    msg_list:List[Message]=[]
    msg_list.insert(0,title)
    try:
        for num in range(1,11):
            msg_list.append(MessageSegment.image(data[num]))
    except:
        await zcos.send(message='超出数据范围，请重新发送')
    try:
        if isinstance(event,GuildMessageEvent):
            for num in msg_list:
                await zcos.send(num)
        else:
            await send_forward_msg(bot, event, "可可酱", bot.self_id, msg_list)
    except ActionFailed as e:
        await zcos.finish(message='出错了或者账户风控了',at_sender=True) 



@suijivideo.handle()
async def sui(event:MessageEvent,match:Matcher,args:Message = CommandArg()):
    if isinstance(event,GuildMessageEvent):
        await suijivideo.finish("该功能不适配频道哦~",at_sender=True)
    args = args.extract_plain_text()#去除命令文字
    if args:
        match.set_arg('type',args)
    else:
        await suijivideo.send(message='明星/热舞/风景/游戏/动物/动漫。默认动漫',at_sender=True)
@suijivideo.got('type',prompt="请告诉可可酱视频类型吧~")
async def get_type(event:MessageEvent,type:Message = Arg()):
    if str(type) in ['明星','热舞','风景','游戏','动漫','动物']:
        url = 'http://ovooa.com/API/sjsp/api.php?msg='+str(type)
        await suijivideo.send(message='可可酱正在寻找中……')
    else:
        await suijivideo.finish("没有你所说的类型,请重新说“随机视频”",at_sender=True)
    mp4 = json.loads(requests.get(url=url).text)['data']['url']
    try:
        await suijivideo.send(MessageSegment.video(mp4))
    except ActionFailed as e:
        await suijivideo.finish(message='出错了,未知情况',at_sender=True)

@yuyin.handle()
async def gta(event:MessageEvent,match:Matcher,args:Message = CommandArg()):
    if isinstance(event,GuildMessageEvent):
        await yuyin.finish("该功能不适配频道哦~",at_sender=True)
    args = args.extract_plain_text()#去除命令文字
    if args:
        match.set_arg('name',args)#如命令后有文字赋值加入

@yuyin.got("name",prompt='请把歌名交给可可酱吧~')
async def handle_music(state:T_State,name:Message = Arg()):
    state['name'] = str(name)
    if not state['name']:
        await yuyin.reject('歌名格式错误，或者没有找到歌名，请重新输入歌名',at_sender=True)
    state['url'] = 'http://ovooa.com/API/yydg/api.php?msg='+str(state['name'])
    await yuyin.send(requests.get(state['url']).text,at_sender=True)

@yuyin.got("n",prompt='请发送歌名的序号给可可酱')
async def getmusic(state:T_State, event:MessageEvent):
    state['url'] = state['url']+"&n="+str(event.get_message())
    try:
        state['music'] = json.loads(requests.get(url=state['url']).text)['data']['url']
    except:
        await yuyin.reject('出错了，没有找到对应的歌曲或者你输入的数字不正确，请重新输入序号',at_sender=True)


@yuyin.handle()
async def _(state:T_State):
    await yuyin.send(message='可可酱正在寻找歌曲中……',at_sender=True)
    async with httpx.AsyncClient() as client:
        mp3 = await client.get(url=state['music'])
    try:
        await yuyin.send(MessageSegment.record(mp3.content))
    except:
        await yuyin.finish(message='出错了，语音格式不正确',at_sender=True)


@heji.handle()
async def ll(match:Matcher,args:Message = CommandArg()):
    args = args.extract_plain_text()#去除命令文字
    if args:
        match.set_arg('type',args)
    else:
        await heji.send(message='1是美女壁纸  2是动漫壁纸  3是风景壁纸  4是游戏壁纸  5是文字壁纸  6是视觉壁纸  7是情感壁纸  8是设计壁纸  9是明星壁纸  10是物语壁纸',at_sender=True)


@heji.got("type", prompt="请发送类型数字给可可酱吧")
async def get_type(state:T_State, event:MessageEvent,type:Message = Arg()):
    if str(type) in ['1','2','3','4','5','6','7','8','9','10']:
        state['url'] = 'http://ovooa.com/API/bizhi/api.php?msg='+str(type)
    else:
        await heji.reject('数字不正确，请输入1-10的数字给可可酱吧~',at_sender=True)
    try:
        await heji.send(message='可可酱正在寻找壁纸中……',at_sender=True)
        imge = requests.get(url=state['url']).text
    except:
        await heji.finish(message='请求超时了，请重试吧',at_sender=True)
    try:
        await heji.send(MessageSegment.image(json.loads(imge)['url']))
    except ActionFailed as e:
        await heji.finish(message=f"出错了，可能是消息格式出错或者账户风控了{e}",at_sender=True)


@hushuo.handle()
async def hu(match:Matcher,args:Message = CommandArg()):
    args = args.extract_plain_text()#去除命令文字
    if args:
        match.set_arg('name',args)#如命令后有文字赋值加入

@hushuo.got("name", prompt="请发送主角名字给可可酱吧")
async def got_name(state:T_State, name:Message = Arg()):
    if str(name):
        url = 'http://ovooa.com/API/dog/api.php?msg='+name
    else:
        await hushuo.reject('主角名字错误，请从新输入吧~',at_sender=True)
    params = {
    'num':'200',
    'type':'text'
    }
    try:
        state['message'] = requests.get(url=url,params=params).text
    except:
        await hushuo.finish(message='可可酱请求出错了，请联系管理员',at_sender=True)

@hushuo.handle()
async def _(bot:Bot, event:MessageEvent, state: T_State):
    try:
        await hushuo.send(state['message'],at_sender=True)
    except:
        await hushuo.finish(message='出错了，可能是消息格式出错或者账户风控了',at_sender=True)


@suangua.handle()
async def _():
    await suangua.send(message='可可酱为你算一卦~',at_sender=True)
    try:
        json_get = requests.get(url='http://ovooa.com/API/chouq/api.php').text
    except:
        await suangua.finish(message='请求出错了，请及时联系管理员',at_sender=True)
    title = json.loads(json_get)['data']['draw']
    messgae = ('⭐'+json.loads(json_get)['data']['annotate']+'⭐\n⭐'
    +json.loads(json_get)['data']['explain']+'\n⭐'
    +json.loads(json_get)['data']['explain']+'\n⭐'
    +json.loads(json_get)['data']['details'])
    image = json.loads(json_get)['data']['image']
    await suangua.send(messgae)
    await suangua.finish(MessageSegment.image(image))


@meizi.handle()
async def _():
    await meizi.send(message='可可酱正在寻找妹子')
    try:
        img = json.loads(requests.get(url='http://ovooa.com/API/meizi/api.php').text)['text']
        await meizi.send(MessageSegment.image(img))
        await meizi.send(message="你要的美腿~（弱弱一句）：lsp！",at_sender=True)
    except:
        await meizi.finish(message='出错了，可能是消息格式出错或者账户风控了')

@yuanshen.handle()
async def _(bot:Bot, event:MessageEvent):
    await yuanshen.send(message='可可酱正在寻找派蒙中……')
    try:
        get_json = requests.get(url='http://ovooa.com/API/yuan/api?type=text').text
    except:    
        await yuanshen.finish(message='请求超时了，请及时联系管理员', at_sender=True)
    try:
        await yuanshen.send(MessageSegment.image(get_json))
        await yuanshen.send(message=f"喏~", at_sender = True)
    except:
        await yuanshen.finish(message='出错了，可能是消息格式出错或者账户风控了')


@touxiang.handle()
async def _(bot:Bot, event:MessageEvent):
    await touxiang.send(message='可可酱正在寻找头像中……')
    try:
        get_ifm = requests.get(url='https://v.api.aa1.cn/api/api-tx/index.php?wpon=json').text
    except:
        await touxiang.finish(message='请求超时了，可可酱没有找到头像。', at_sender=True)
    get_json = get_ifm[get_ifm.rfind('{'):]
    url = 'https:'+json.loads(get_json)['img']
    async with httpx.AsyncClient(follow_redirects=True) as client:
        img = await client.get(url=url)
    try:
        await touxiang.send(MessageSegment.image(img.content))
        await touxiang.finish(message='客官，你要的头像', at_sender = True)
    except ActionFailed as e:
        await touxiang.finish(message=f"可可酱出错了！{e}")


@douyin2.handle()
async def _(bot:Bot, event:MessageEvent):
    await douyin2.send(message='可可酱正在刷视频……')
    if isinstance(event,GuildMessageEvent):
        await douyin2.finish("该功能暂不适配频道哦~",at_sender=True)
    try:
        img = requests.get(url= 'https://tucdn.wpon.cn/api-girl/index.php?wpon=json').text
    except:
        await douyin2.finish(message="请求超时了，没有找到神秘东西。", at_sender=True)
    img = json.loads(img)['mp4']
    img = 'https:'+str(img)
    try:
        await douyin.send(MessageSegment.video(img))
        await douyin.finish(message='喏~', at_sender=True)
    except ActionFailed as e:
        await douyin.finish(message=f"出错了,{e}", at_sender=True)


@douyin.handle()
async def _(bot:Bot, event:MessageEvent):
    await douyin.send(message='可可酱正在寻找小姐姐……')
    if isinstance(event,GuildMessageEvent):
        await douyin.finish("该功能暂不适配频道哦~",at_sender=True)
    try:
        url = 'https://v.api.aa1.cn/api/api-dy-girl/index.php?aa1=json'
        get_img = requests.get(url=url, timeout=30).text
    except:
        await douyin.finish(message='请求失败了，可可酱没有找到视频qwq', at_sender=True)
    img = json.loads(get_img)['mp4']
    img = img.replace(" ","%20")
    img = 'https:'+img
    try:
        await douyin.send(MessageSegment.video(img))
        await douyin.finish(message='喏~', at_sender=True)
    except ActionFailed as e:
        await douyin.finish(message=f"{e}", at_sender=True)

@cos.handle()
async def _(bot:Bot, event:MessageEvent,i=1):
    await cos.send(message='可可酱正在寻找cosplayer中……')
    msg_list:List[Message]=[]
    msg_list.insert(0,'客官,可可酱找到coser如下')
    heads = {
        'uer-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    while i<=5:
        i+=1
        img = requests.get(url='http://121.40.95.21/api/cos.php',headers=heads).text
        msg_list.append(MessageSegment.image(file=(img.replace('\n',''))))
        await sleep(0.5)
    try:
        if isinstance(event,GuildMessageEvent):
            for num in msg_list:
                await cos.send(num)
        else:
            await send_forward_msg(bot, event, "cos可可酱", bot.self_id, msg_list)
    except ActionFailed as e:
        await cos.finish(message='账户风控了，或格式出错了',at_sender=True)


@help.handle()
async def hp(bot:Bot, event:MessageEvent, state: T_State):
    await help.finish(message="⭐可可酱一些来点图片的帮助⭐\n\
🚪来点壁纸   🚪\n\
🚪来点二次元 🚪\n\
🚪来点猫猫   🚪\n\
🚪来点买家秀 🚪\n\
🚪来点bing   🚪\n\
🚪来点二次元壁纸🚪\n\
🚪来点p图    🚪\n\
🚪来点cos    🚪\n\
🚪来点抖音   🚪\n\
🚪来点小姐姐 🚪\n\
🚪来点女头   🚪\n\
🚪来点原神壁纸🚪\n\
🚪来点妹子   🚪\n\
🚪胡言乱语   🚪\n\
🚪算一卦     🚪\n\
🚪壁纸合集   🚪\n\
🚪语音点歌   🚪\n\
🚪随机视频   🚪\n\
🚪cos正片    🚪\n\
🚪历史上的今天🚪\n\
🚪随机二次元 🚪\n\
🚪p搜图      🚪\n\
🚪刷视频     🚪\n\
⭐更多功能还待完善⭐\n")

async def get_ercibizhi():
    async with httpx.AsyncClient(follow_redirects=True)as client:
        img_get=await client.get(url='https://api.yimian.xyz/img?type=moe&size=1920x1080', timeout=120)
    return img_get


@setu.handle()
async def p(bot:Bot, event:MessageEvent):
    await setu.send(message='可可酱正在寻找p图……')
    try:
        get_json = requests.get(url='http://sex.nyan.xyz/api/v2/',timeout=60).text
        get_json = json.loads(get_json)
        date = get_json['data'][0]
        url = date['url']
        tags = date['tags'][0] +' '+ date['tags'][1] +' '+ date['tags'][2] + ' '+date['tags'][3]
    except:
        await setu.finish(message='出错了，可可酱没有找到p图')
    msg = tags + MessageSegment.image(url)
    msg_list:List[Message]=[]
    msg_list=msg_list[:3]
    msg_list.insert(0,"可可酱提醒你，未经管理员允许，请勿转发")
    msg_list.insert(1,msg)
    msg_list.insert(2,f"原链接：{date['page']}")
    faild_num = 0
    try:
        if isinstance(event,GuildMessageEvent):
            for num in msg_list:
                await setu.send(num)
        else:
            await send_forward_msg(bot, event, "可可酱", bot.self_id, msg_list)
    except ActionFailed as e:
        logger.warning(e)
        faild_num = 1
    if faild_num == 1:
        await setu.finish(
            message=Message(f"消息被风控，{faild_num} 个图发不出来了\n"),
            at_sender=True,
        )
    await sleep(2)




async def get_miao():
    async with httpx.AsyncClient(verify=False,follow_redirects=True)as client:
        img_get=await client.get(url='http://edgecats.net/', timeout=60,)
    return img_get

async def get_erciyuan():
    async with httpx.AsyncClient(verify=False,follow_redirects=True)as client:
        img_get=await client.get(url='http://api.ixiaowai.cn/api/api.php', timeout=60)
    return img_get

async def get_bizhi():
    async with httpx.AsyncClient(verify=False,follow_redirects=True)as client:
        img_get=await client.get(url='http://api.ixiaowai.cn/gqapi/gqapi.php', timeout=60)
    return img_get   


async def maijia_get():
    async with httpx.AsyncClient(verify=False,follow_redirects=True)as client:
        get_img=await client.get(url='http://api.uomg.com/api/rand.img3', timeout=60)
    return get_img


async def get_bing():
    async with httpx.AsyncClient(verify=False,follow_redirects=True)as client:
        get_img=await client.get(url='http://api.yimian.xyz/img?type=wallpaper', timeout=60)
    return get_img


@bizhi_er.handle()
async def erbi(bot:Bot, event:MessageEvent, state:T_State):
    await bizhi_er.send(message='可可酱正在寻找二次元壁纸……')
    msg=await get_ercibizhi()
    try:
        await bizhi_er.send(MessageSegment.image(msg.content))
        await bizhi_er.send(message='成功了，找到一张壁纸！',at_sender=True)
    except:
        await bizhi_er.finish(message='可可酱失败了，请稍后重试')


@bing.handle()
async def bin(bot:Bot, event:MessageEvent, state:T_State):
    await bing.send(message='可可酱正在获取bing图……')
    msg=await get_bing()
    try:
        await bing.send(MessageSegment.image(msg.content))
        await bing.send(message='成功了！你要的bing图',at_sender=True)
    except:
        await bing.finish(message='可可酱请求失败了，请稍后重试',at_sender=True)


@bizhi.handle()
async def bz(bot:Bot, event:MessageEvent, state: T_State):
    await bizhi.send(message='可可酱正在寻找壁纸……')
    msg=await get_bizhi()
    try:
        await bizhi.send(MessageSegment.image(msg.content))
        await bizhi.send(message='客官，你要的壁纸~',at_sender=True)
    except:
        await bizhi.finish(message='可可酱没有找到壁纸')

@maijia.handle()
async def mj(bot:Bot, event:MessageEvent, state: T_State):
    await maijia.send(message='可可酱正在寻找买家秀……')
    msg=await maijia_get()
    try:
        msg_info = await maijia.send(MessageSegment.image(msg.content))
        await maijia.send(message='找到了一张买家图，喏~',at_sender=True)
        add_withdraw_job(bot, **msg_info)
        await sleep(1)
    except:
        await maijia.finish(message='请求超时了，可可酱没有找到图片')


@erciyuan.handle()
async def erci(bot: Bot, event:MessageEvent, state: T_State):
    await erciyuan.send(message='可可酱正在寻找二次元……')
    msg=await get_erciyuan()
    try:
        await erciyuan.send(MessageSegment.image(msg.content))
        await erciyuan.send(message='客官，你要的二次元~',at_sender=True)
    except:
        await erciyuan.finish(message='可可酱没有找到二次元')    


@miao.handle()
async def hf(bot: Bot, event: MessageEvent, state: T_State):
    await miao.send(message='可可酱正在寻找猫猫……')
    msg=await get_miao()
    try:
        await miao.send(MessageSegment.image(msg.content))
        await miao.send(message='客官，你要的猫猫~',at_sender=True)
    except:
        await miao.finish(message='可可酱没有找到猫猫，请求超时了')


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