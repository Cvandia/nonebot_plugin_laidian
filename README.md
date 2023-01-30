

<div align="center">

<a href="https://v2.nonebot.dev/store"><img src="https://v2.nonebot.dev/logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>

</div>

<div align="center">

# nonebot-plugin-laidian

_⭐基于Nonebot2的一款来点随机图的插件⭐_


</div>


## ⭐ 介绍

基于大量的API，实现来点图片的发送,目前可通过[频道补丁](https://github.com/mnixry/nonebot-plugin-guild-patch)完成QQ频道适配
>别看了，这里什么都没有@_@

## 💿 安装

<details>
<summary>nb-cli安装</summary>

在项目目录文件下运行

```
nb plugin install nonebot_plugin_laidian
```
</details>

<details>
<summary>pip安装</summary>

```
pip install nonebot-plugin-laidian
```
</details>

——————————————————————————————————


## ⚙️ 配置

在```.env```中添加如下配置

```
laidian_with = 10
```
该选项是某些图片撤回时间（秒），不设置默认不撤回
```
Bot_NICKNAME = ""
```
bot的名字


## ⭐ 使用

### 指令：
| 指令 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|
|来点帮助|否|私聊、群聊|查看所有来点帮助|


全部功能如下：
```
🚪来点壁纸   
🚪来点二次元 
🚪来点猫猫   
🚪来点买家秀 
🚪来点bing   
🚪来点二次元壁纸
🚪来点p图    
🚪来点cos    
🚪来点抖音   
🚪来点小姐姐 
🚪来点女头   
🚪来点原神壁纸
🚪来点妹子   
🚪胡言乱语  
🚪算一卦     
🚪壁纸合集   
🚪语音点歌 
🚪随机视频   
🚪cos正片 
🚪历史上的今天
🚪随机二次元
🚪p搜图   
🚪刷视频     
```    
**注意**

默认情况下, 您应该在指令前加上命令前缀, 通常是 /

## 🌙 未来todo

- [x] 语音点歌
- [ ]  优化匹配机制
- [ ] 优化请求结构
- [ ] 添加更多功能
- [ ] 菜单图片化

## ⭐问题

由于API不稳定，可能有时候掉线或者挂掉，有情况可联系作者
>m1141538825@163.com

## 🌙鸣谢
__>[夏柔API](https://api.aa1.cn/)__

__>[独角兽API](http://ovooa.com/)__

__>[小歪API](https://api.ixiaowai.cn/)__

__>[随机涩图API](https://img.jitsu.top/)__