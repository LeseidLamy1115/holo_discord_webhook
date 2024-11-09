import json
import sys

try:
    with open('locale.json', 'r', encoding='utf-8') as f:
        lc = json.load(f)
except:
    print('[\033[31mError\033[0m]Failed to load localize file.(Cant find locale.json file. Is it there?)')
    print('[\033[31mエラー\033[0m]翻訳ファイルの取得に失敗しました。「locale.json」ファイルがあるかの確認をしてください。')
    sys.exit('')
    
class localizeto:
    text = ""

def localizeto(text='', lang='ja'):
    if not text in lc:
        print('[\033[33mLocalizeError\033[0m]Cant found text key "' + text + '" in localize data. Printed alternate text and ignored it.')
        return text
    else:
        return lc[text][lang]