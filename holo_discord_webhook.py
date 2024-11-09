import asyncio
import re
import time
import requests
from requests.exceptions import ConnectionError, Timeout, ChunkedEncodingError
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import math
import sys
import json

import config
from getlocale import localizeto

try:
    lang, conf_webhook, ampm, interval = config.load_config()
    if not (lang == 'ja' or lang == 'en'):
        print('[\033[33mignored\033[0m]"Unsupported language. Continue in Japanese.')
        lang = 'ja'
except:
    print('[\033[31m'+localizeto('error',lang)+'\033[0m]'+localizeto('fail_load_config',lang))
    sys.exit('')

timezone_str = ''
if not datetime.now().astimezone().utcoffset().seconds == 32400:
    timezone_str = '(JST)'

if conf_webhook == "":
    print('[\033[31m'+localizeto('error',lang)+'\033[0m]'+localizeto('fail_load_webhookurl',lang))
    sys.exit('')
webhook_url_Hololive = conf_webhook
holodule_url = 'https://schedule.hololive.tv/'
holodule_list = []

#配信者のチャンネルID, 配信者名, アイコン画像のURLのリスト
Hololive = {}
try:
    with open('holomen.json', 'r', encoding='utf-8') as f:
        Hololive = json.load(f)
except:
    print('[\033[31m'+localizeto('error',lang)+'\033[0m]'+localizeto('fail_load_json_holomen',lang))
    sys.exit('')

class Holodule:
    datetime = None
    name = ""
    url = ""

def print_time():
    time = str(datetime.now().strftime('%H:%M'))
    return time

def get_holodule():
    global holodule_list
    try:
        holodule_list = []
        response = requests.get(holodule_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # スケジュールの取得
        date_string = ""
        today = datetime.now()
        tab_pane = soup.find('div', class_="tab-pane show active")
        containers = tab_pane.find_all('div', class_="container")
    except ConnectionError:
        print('[\033[31m'+localizeto('error',lang)+'\033[0m][\033[33m' + print_time() + '\033[0m]'+localizeto('fail_refresh_connectionerror',lang))
    except Timeout:
        print('[\033[31m'+localizeto('error',lang)+'\033[0m][\033[33m' + print_time() + '\033[0m]'+localizeto('fail_refresh_timeout',lang))
    except ChunkedEncodingError:
        print('[\033[31m'+localizeto('error',lang)+'\033[0m][\033[33m' + print_time() + '\033[0m]'+localizeto('fail_refresh_chunkedencodingerror',lang))
    else:
        for container in containers:
            # 日付のみ取得
            div_date = container.find('div', class_="holodule navbar-text")
            if div_date is not None:
                date_text = div_date.text.strip()
                match_date = re.search(r'[0-9]{1,2}/[0-9]{1,2}', date_text)
                dates = match_date.group(0).split("/")
                month = int(dates[0])
                day = int(dates[1])
                year = today.year
                if month < today.month or ( month == 12 and today.month == 1 ):
                    year = year - 1
                elif month > today.month or ( month == 1 and today.month == 12 ):
                    year = year + 1

                date_string = f"{year}/{month}/{day}"
            # ライバー毎のスケジュール
            thumbnails = container.find_all('a', class_="thumbnail")
            if thumbnails is not None:
                for thumbnail in thumbnails:
                    holodule = Holodule()
                    youtube_url = thumbnail.get("href")
                    if youtube_url is not None:
                        #いろいろ分岐してるけど動作は何も変わらない。URLにこれらの単語含まれていない場合は通知しない。
                        if 'watch' in youtube_url or 'twitch' in youtube_url:
                            # YouTube or Twitch URL
                            holodule.url = youtube_url
                        elif  'joqr' in youtube_url:
                            # Joqr URL
                            if 'suikoro' in youtube_url:
                                #平行線すくらんぶる
                                holodule.url = youtube_url
                            elif 'hip' in youtube_url:
                                #hololive IDOL PROJECT presents
                                holodule.url = youtube_url
                        elif 'skdw' in youtube_url:
                            #Vのすこんなオタ活なんだワ
                            holodule.url = youtube_url
                        else:
                            continue
                    # 時刻（先に取得しておいた日付と合体）
                    div_time = thumbnail.find('div', class_="col-4 col-sm-4 col-md-4 text-left datetime")
                    if div_time is not None:
                        time_text = div_time.text.strip()
                        match_time = re.search(r'[0-9]{1,2}:[0-9]{1,2}', time_text)
                        times = match_time.group(0).split(":")
                        hour = int(times[0])
                        minute = int(times[1])
                        datetime_string = f"{date_string} {hour}:{minute}:00+0900"
                        holodule.datetime = datetime.strptime(datetime_string, "%Y/%m/%d %H:%M:%S%z")
                    # ライバーの名前
                    div_name = thumbnail.find('div', class_="col text-right name")
                    if div_name is not None:
                        holodule.name = div_name.text.strip()
                    # リストに追加
                    holodule_list.append(holodule)
        print('[\033[36m'+localizeto('info',lang)+'\033[0m]'+localizeto('listlength',lang)+': ' + str(len(holodule_list)))

def check_schedule(now_time, holodule_list):
    for bd in list(holodule_list):
        try:
            now_time10 = now_time + timedelta(minutes=10)
            sd_time = bd.datetime.astimezone()
            if sd_time == None:
                continue
            if(now_time10.hour == sd_time.hour and now_time10.minute == sd_time.minute and now_time10.month == sd_time.month and now_time10.day == sd_time.day):
                print('- ' + bd.name + '[\033[33m' + str(sd_time) + '\033[0m]')
                post_broadcast_schedule(bd.name, bd.url, sd_time)
        except KeyError:
            continue

def post_broadcast_schedule(userName, videoUrl, starttime):
    if not userName in Hololive:
        print('[\033[33m'+localizeto('ignored',lang)+'\033[0m]"' + userName + localizeto('notinlist',lang))
        return
    if ampm:
        strptime = str(starttime.strftime('%I:%M %p'))
    else:
        strptime = str(starttime.strftime('%H:%M'))
    st = strptime + timezone_str
    #Discordに投稿される文章
    content = localizeto('livein10minutes',lang)+"("+localizeto('scheduled_time',lang)+st+')\n'+videoUrl
    main_content = {
        "username": Hololive[userName][0], #配信者名
        "avatar_url": Hololive[userName][1], #アイコン
        "content": content #文章
    }
    time.sleep(1)
    requests.post(webhook_url_Hololive, main_content) #Discordに送信

get_holodule()
print('[\033[36m'+localizeto('notice',lang)+'\033[0m]' + localizeto('startup_complete',lang))

interval_sec = math.floor(interval)*60
if interval_sec > 86400:
    interval_sec = 86400
elif interval_sec < 60:
    interval_sec = 60
print('[\033[36m'+localizeto('info',lang)+'\033[0m]'+localizeto('refreshinterval',lang)+': '+str(interval_sec))

async def get_holodule_loop(now_time):
    now_td = now_time - datetime(now_time.year, now_time.month, now_time.day) 
    if(now_td.seconds % interval_sec == 0):
        get_holodule()
        print('[\033[36m'+localizeto('info',lang)+'\033[0m][\033[33m' + print_time() + '\033[0m]' + localizeto('scheduled_refresh',lang))

async def check_schedule_loop(now_time):
    if(now_time.second == 0):
        check_schedule(now_time, holodule_list)

async def main_loop():
    while True:
        now_time = datetime.now()
        ghl = asyncio.create_task(get_holodule_loop(now_time))
        csl = asyncio.create_task(check_schedule_loop(now_time))
        await asyncio.wait({ghl, csl})
        await asyncio.sleep(1)
    
loop = asyncio.new_event_loop()
try:
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_loop())
except KeyboardInterrupt:
    loop.stop()
finally:
    loop.close()
