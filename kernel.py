import requests
import time
true=True
false=False
import json
import sys
from PyQt5.QtWidgets import QApplication,QMessageBox,QMainWindow,QWidget

#该脚本包含:生成二维码图片,根据二维码验证结果保存cookie文件,根据cookie得到用户信息,视频封面,用户头像,格式化用户信息,供主窗口使用的初始化,获取cid

def mkqr():
    import qrcode
    try:
        a=requests.get('http://passport.bilibili.com/qrcode/getLoginUrl').text
    except Exception as e:
        debug(e)
        exit(-1)
    repdic=eval(a)  # rep meaning response

    url=repdic['data']['url']
    pack= {'oauthKey':repdic['data']['oauthKey']}
    qr = qrcode.QRCode(
        version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert("RGBA")
    img.save('img/qr.png')  # 显示图片,可以通过save保存
    return pack

def getAcookie(pack):
    while True:
        resp=requests.post('http://passport.bilibili.com/qrcode/getLoginInfo',pack)
        d=eval(resp.text)
        if d['status'] == true:
            cookies=resp.cookies.get_dict()
            break
        time.sleep(1)

    savecookies=json.dumps(cookies)

    with open("logininfo/cookies.cookie", "w") as f:
        f.write(savecookies)

def getUsrinfo(cookie):
    cookies=eval(cookie)
    r=requests.get('http://api.bilibili.com/x/space/myinfo',cookies=cookies)
    return eval(r.text)['data']

def picdown(url):
    name='img/face.jpg'
    response = requests.get(url)
    with open(name,'wb')as f:
        f.write(response.content)

def vidpicdown(url):
    name='img/cover.jpg'
    response = requests.get(url)
    with open(name,'wb')as f:
        f.write(response.content)

def cut(info):
    info_cut={}

    info_cut['mid']=info['mid']
    info_cut['name']=info['name']
    info_cut['level']=info['level']
    info_cut['exp']=str(info['level_exp']['current_exp'])+'/'+str(info['level_exp']['next_exp'])
    print(info_cut['exp'])
    info_cut['coins']=info['coins']

    info_cut['viptype']=info['vip']['type']
    info_cut['viplabel'] = info['vip']['label']['text']

    return info_cut

def init():
    try:
        #读取cookie
        with open("logininfo/cookies.cookie", 'r') as f:
            cookie=f.read()
        info=getUsrinfo(cookie)   #根据cookie获取信息
    except:
        return 'fail',None
    picdown(info['face'])   #下载用户图
    info_cut=cut(info)  #筛选有效信息
    collect=requests.get('http://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={}'.format(info_cut['mid'])).text #获取用户收藏
    return 'ok',[info_cut,collect]


def gcid(bid):
    url='http://api.bilibili.com/x/web-interface/view?bvid={}'.format(bid)
    ele = requests.get(url)
    ele.encoding = 'utf-8'
    text = ele.text
    true = True
    false = False
    data = eval(text)
    return data['data']['cid']

if __name__ == '__main__':
    init()
