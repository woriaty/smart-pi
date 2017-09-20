#-*- coding:utf-8 -*-
from urllib import request, parse
import json
import random
import re
import os

from wx_gui import  main_window
import wx
import wx.xrc

singer_name = "李玉刚"
song_name = "刚好遇见你"
showapi_appid = "****"  # 替换此值
showapi_sign = "********************"  # 替换此值
url = "http://route.showapi.com/213-1"
send_api_data = parse.urlencode([
    ('showapi_appid', showapi_appid)
    , ('showapi_sign', showapi_sign)
    , ('keyword', song_name)
    , ('page', "1")
])

class audio_op:
    def __init__(self):
        self.name = "audio operate"

    def audio_json_get(self,url,send_data):          #获取音频的json数据
        print('send data....')
        req = request.Request(url)
        req.add_header("User-Agent", \
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")
        try:
            response = request.urlopen(req, data=send_data.encode('utf-8'), timeout=10)  # 10秒超时反馈
        except Exception as e:
            print(e)
        result = response.read().decode('utf-8')
        result_json = json.loads(result)
        print("result_json data is {}".format(result_json))
        return result_json

    def str_cmp(self,source_str, target_str):  # 目标字符串能和原字符串匹配，则返回true
        string = r"" + source_str
        rule = re.compile(string)
        if re.findall(rule, target_str) != []:
            return True
        else:
            return False

    def audio_data_get(self,audio_json):     #解析json数据，返回音频数据字典
        audio_dict = {'singer': None, 'name': None, 'url': None}  # 定义感兴趣的音频数据字典，分别为歌手、歌曲名和地址
        audio_match = False
        for i in range(len(audio_json)):
            target_url = audio_json['showapi_res_body']['pagebean']['contentlist'][i]['m4a']
            target_singername = audio_json['showapi_res_body']['pagebean']['contentlist'][i]['singername']
            target_song_name = audio_json['showapi_res_body']['pagebean']['contentlist'][i]['songname']
            if self.str_cmp(singer_name,target_singername):
                print("歌手匹配完成，开始播放音乐")
                audio_match = True
                break
        if audio_match == False:
            rand_song = random.randint[0,len(audio_json)]
            target_url = audio_json['showapi_res_body']['pagebean']['contentlist'][rand_song]['m4a']
            target_singername = audio_json['showapi_res_body']['pagebean']['contentlist'][rand_song]['singername']
            target_song_name = audio_json['showapi_res_body']['pagebean']['contentlist'][rand_song]['songname']
            print("搜索完毕，歌手匹配异常,开始随机播放")
        audio_dict['singer'] = target_singername
        audio_dict['name'] = target_song_name
        audio_dict['url'] = target_url
        print('audio_dict = %s' % audio_dict)
        return audio_dict

    def audio_save(self,audio_name,audio_url):   # 保存到本地，覆盖或创建的方式保存
        audio_data = request.urlopen(audio_url).read()
        target_audio_name = audio_name + "-" + song_name + ".m4a"
        with open(target_audio_name, "wb") as f:
            f.write(audio_data)

    def audio_play_online(self,audio_url):  #调用shell命令播放在线音乐
        os.system("cvlc %s" % audio_url)

class audio_gui(main_window):
    def __init__(self,parent):
        main_window.__init__(self,parent)

    def search_button_click( self, event ):
        song_name_input = self.audio_name.GetValue()
        print(song_name_input)
        self.audio_list.SetStringSelection(song_name_input)

if __name__ == '__main__':
    # audio = audio_op()
    # print(audio.name)
    # audio_json = audio.audio_json_get(url,send_api_data)
    # audio_data = audio.audio_data_get(audio_json)
    # audio.audio_play_online(audio_data['url'])
    app = wx.App(False)
    frame = audio_gui(None)
    frame.Show(True)
    # start the applications
    app.MainLoop()
