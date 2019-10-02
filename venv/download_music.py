import requests
import re
import json
import os

# 便于存放作者的姓名
zuozhe = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}


def get_singermid():
    name = input('请输入你要下载歌曲的作者:')
    zuozhe.append(name)
    if not os.path.exists(name):
        os.mkdir(name)
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    data = {
        'w': name,
        'jsonpCallback': 'MusicJsonCallback885332333726736', }
    response = requests.get(url, headers=headers, params=data).text
    patt = re.compile('MusicJsonCallback\d+\((.*?)\}\)')
    singermid = re.findall(patt, response)[0]
    singermid = singermid + '}'
    dic = json.loads(singermid)
    return dic['data']['song']['list'][0]['singer'][0]['mid']


def get_page_html(singermid):
    url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg'
    params = {
        'g_tk': 5381,
        'jsonpCallback': 'MusicJsonCallbacksinger_track',
        'loginUin': 0,
        'hostUin': 0,
        'format': 'jsonp',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': 0,
        'platform': 'yqq',
        'needNewCode': 0,
        'singermid': singermid,
        'order': 'listen',
        'begin': 0,  # 页数  0 30  60
        'num': 30,
        'songstatus': 1,
    }
    response = requests.get(url, headers=headers, params=params)
    return response.text


def get_vkey_data(songmid, strMediaMid, name):
    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
    strMediaMid1 = 'C400' + strMediaMid + '.m4a'
    data = {
        'g_tk': 5381,
        'jsonpCallback': "MusicJsonCallback4327043425715609",
        'loginUin': 0,
        'hostUin': 0,
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': 0,
        'platform': 'yqq',
        'needNewCode': 0,
        'cid': 205361747,
        'callback': 'MusicJsonCallback4327043425715609',
        'uin': 0,
        'songmid': songmid,
        'filename': strMediaMid1,
        'guid': 4428680404,
    }
    response = requests.get(url, headers=headers, params=data).text
    try:
        patt = re.compile('\"vkey\":\"(.*?)\"')
        vkey = re.findall(patt, response)[0]
        patt = re.compile('\"filename\":\"(.*?)\"')
        filename = re.findall(patt, response)[0]
        url1 = 'http://dl.stream.qqmusic.qq.com/' + filename + '?vkey=' + vkey + '&guid=4428680404&uin=0&fromtag=66'
        yingyue = requests.get(url1, headers=headers).content
        with open(zuozhe[0] + '/' + name + '.m4a', 'wb') as f:
            f.write(yingyue)
            f.close()
            print('下载完成《' + name + '》')
    except Exception as e:
        print(e)
        pass


def get_detail_html(html):
    if html:
        patt = re.compile('data\":{\"list\":(.*?),\"singer_id', re.S)
        json_html = re.findall(patt, html)[0]
        data_html = json.loads(json_html)
        for data in data_html:
            name = data['musicData']['songname']
            songmid = data['musicData']['songmid']
            strMediaMid = data['musicData']['strMediaMid']
            print('正在下载《' + name + '》......')
            get_vkey_data(songmid, strMediaMid, name)


def main():
    # 获取 singermid
    singermid = get_singermid()
    html = get_page_html(singermid)
    get_detail_html(html)


if __name__ == '__main__':
    main()