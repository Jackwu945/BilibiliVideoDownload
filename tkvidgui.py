from tkinter import *
from PIL import Image, ImageTk
from kernel import vidpicdown,gcid
import requests
import json
import time
from ffmpy import FFmpeg
import os

def mix(vidname):
    stat['text'] = '合并视频中...'
    app.update()
    ff = FFmpeg(
        inputs={'down.mp4': None,'down.mp3':None},
        outputs={'vidout/{}.mp4'.format(vidname): '-c:v copy -c:a aac'}
    )
    print(ff.cmd)
    # ffmpeg -i fate.mkv -c:v libx264 -c:a aac -strict -2 -f hls -hls_list_size 0 -hls_time 2 fate.m3u8
    ff.run()

    os.remove('down.mp4')
    os.remove('down.mp3')
    stat['text'] = '下载完成!'





def downVIDstream(stream):
    headers = {"Referer": "http://www.bilibili.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
    response = requests.get(stream, headers=headers, stream=True)  # stream=True表示请求成功后并不会立即开始下载，而是在调用iter_content方法之后才会开始下载
    chunk_size = 512000  # 设置每次下载的块大小
    content_size = int(response.headers['content-length'])  # 从返回的response的headers中获取文件大小
    size=content_size
    with open('down' + '.mp4', 'wb') as f:
        total_d=0
        a = time.time()
        for data in response.iter_content(chunk_size=chunk_size):  # 在循环读取文件时，刷新进度条
            f.write(data)
            app.update()
            b=time.time()
            if int(b-a)==0:
                b+=1
            spd=round(total_d/int(b-a),2)
            stat['text']='下载视频中:速度{}Mb/s, 进度{}%'.format(int(int(spd)/1000000),round((total_d/size)*100,2))
            app.update()
            total_d+=chunk_size
def downAUDstream(stream):
    headers = {"Referer": "http://www.bilibili.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
    response = requests.get(stream, headers=headers, stream=True)  # stream=True表示请求成功后并不会立即开始下载，而是在调用iter_content方法之后才会开始下载
    chunk_size = 512000  # 设置每次下载的块大小
    content_size = int(response.headers['content-length'])  # 从返回的response的headers中获取文件大小
    size=content_size
    with open('down' + '.mp3', 'wb') as f:
        total_d=0
        a = time.time()
        for data in response.iter_content(chunk_size=chunk_size):  # 在循环读取文件时，刷新进度条
            f.write(data)
            app.update()
            b=time.time()
            if int(b-a)==0:
                b+=1
            spd=round(total_d/int(b-a),2)
            stat['text'] = '下载音频中:速度{}Mb/s, 进度{}%'.format(int(spd) / 1000000, round((total_d / size) * 100, 2))
            total_d+=chunk_size



def download(bv,vidname):
    global app
    with open("logininfo/cookies.cookie", 'r') as f:
        cookie = eval(f.read())

    parm = {'bvid': bv, 'cid': gcid(bv),'qn':64,'fnval':16} #BV1664y1v7iA
    stream=json.loads(requests.get('http://api.bilibili.com/x/player/playurl', cookies=cookie, params=parm).text)['data']['dash']['video'][0]['baseUrl']
    audiostream= json.loads(requests.get('http://api.bilibili.com/x/player/playurl', cookies=cookie, params=parm).text)['data']['dash']['audio'][0]['baseUrl']

    downVIDstream(stream)
    downAUDstream(audiostream)
    mix(vidname)







def main(vidlist):
    global stat
    global app
    app=Tk()
    print(vidlist)
    try:
        vl = vidlist['stat']
        vidpicdown(vidlist['pic'])
        topic=vidlist['title']
        desc=vidlist['desc']
    except:
        vl= {'view':0,'like':0,'coin':0,'favorite':0}
        vidpicdown(vidlist['result']['cover'])
        topic=vidlist['result']['season_title']
        desc=vidlist['result']['evaluate']


    app.geometry('1093x498')
    app.wm_title('vidinfo')


    image = Image.open("img/cover.jpg")
    image=image.resize((300,300),Image.ANTIALIAS)
    pyt = ImageTk.PhotoImage(image)
    label = Label(app, image=pyt)
    label.place(x=20, y=10, width=300, height=300)


    label_topic=Label(app,font=('Arial', '24', 'bold'),text=topic)
    label_topic.place(x=400,y=10,width=700,height=71)


    label_desc=Message(app,text=desc)
    label_desc.place(x=380,y=90,width=691,height=250)

    sanlian = '播放量{},点赞{},投币{},收藏{}'.format(vl['view'], vl['like'], vl['coin'], vl['favorite'])
    label_stat=Label(app,text=sanlian)
    label_stat.place(x=380,y=310,width=701,height=61)

    initwrd = ''
    stat=Label(app,text=initwrd)
    stat.place(x=380,y=350,width=701,height=61)


    button = Button(app, text='下载',command=lambda: download(vidlist['bvid'],vidlist['title']))
    button.place(x=40, y=340, width=201, height=71)

    canvas = Canvas(app, width=465, height=22, bg="white")
    canvas.place(x=505, y=400)

    app.mainloop()

if __name__ == '__main__':
    main()