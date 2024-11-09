import os
import configparser

def load_config(path="./config.ini"):
    if os.path.exists(path) and os.path.isfile(path):
        ini = configparser.ConfigParser()
        ini.read('./config.ini', 'UTF-8')
        lang = ini['Language']['lang']
        webhook = ini['webhook']['webhook']
        if ini['Time']['ampm'] == "True":
            ampm = True
        else:
            ampm = False
        interval = int(ini['Interval']['holodule_refresh'])

    return lang, webhook, ampm, interval
