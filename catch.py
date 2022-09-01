import os

import requests
import re
import json
#b站地址

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}


def getElement(url):
    url = url
    headers['Referer'] = url  # 带上防爬链的referer
    resp = requests.get(url, headers=headers)
    return resp

def findJson(resp):
    # 找到页面源代码内含有视频音频json的区域(正则表达式)
    play_info_re = re.compile(r"window.__playinfo__=(?P<play_info>.*?)</script>")

    # 将在网页源代码搜索的结果包含的关键的视频音频json分出来
    play_info = play_info_re.search(resp.text).group("play_info")
    return play_info


def exchangeJson(play_info):
    # json转化成字典格式
    dic = json.loads(play_info)
    return dic


def findElement(dic):
    video_url = dic['data']['dash']['video'][0]['baseUrl']
    audio_url = dic['data']['dash']['audio'][0]['baseUrl']
    # print(video_url+"\n"+audio_url)
    return video_url,audio_url





##下载音频和视频
#发请求,保存成文件
def download(video_url,audio_url):
    v_resp = requests.get(video_url, headers=headers)
    with open('video.m4s', mode='wb') as f:
        f.write(v_resp.content)

    a_resp = requests.get(audio_url, headers=headers)
    with open('audio.m4s', mode='wb') as f:
        f.write(a_resp.content)


#得到页面源代码,存到resp里
resp=getElement('https://www.bilibili.com/video/BV1j4411Y7Qa?spm_id_from=333.999.0.0&vd_source=82a50743c10dd61cc1c313eda84d3e98')
#将在网页源代码搜索的结果包含的关键的视频音频json分出来,然后转化为字典格式
dic=exchangeJson(findJson(resp))
#找到视频音频的链接存起来
li=findElement(dic)

download(li[0], li[1])

os.system("ffmpeg -i audio.m4s -i video.m4s -acodec copy -vcodec copy good.mp4")