# ホロライブP 配信開始通知Discord Webhook Bot

![image](https://hanano.hiromin.xyz/content/discordbot/holo_discord_webhook_image.jpg)

## 紹介

ホロジュールの配信予定時刻表示を読み取り、配信の10分前に告知するDiscord向けWebhookボットです。

## 参考サイト

[ホロライブメンバーの配信予定を取得して配信開始時刻に通知するDiscord botを作った](https://qiita.com/wak_t/items/4796d0e80097f93af656)

## 必要環境

Python 3以降
(テスト環境はPython 3.10.5)

## インストールが必要なPythonライブラリ

- Requests
- Beautiful Soup 4

```
pip install requests
pip install bs4
```

## 初期セットアップ

まずはDiscordのWebhook URLを取得してください。
1. 自分の所有する（または権限のある）サーバー設定を開きます。
2. 連携サービス、ウェブフックの確認を開きます。
3. 新しいウェブフックを押し、ウェブフックを新規作成します。
4. 新規作成されたウェブフックを選択し、管理しやすい名前に変更、配信告知を投稿するチャンネルを選択します。
5. 最後に「ウェブフックURLをコピー」を押し、URLを取得します。

次にボットの編集です。
「Config.ini」を開き、webhookに取得したURLを貼り付けます。

「webhook =」の後に先ほどコピーしたURLをペーストします。

例：

```
webhook = https://discord.com/api/webhooks/<数字が書いてある>/<文字列がならんでいる>
```

ペーストした後は保存し、準備完了です。
起動方法は環境によるため割愛します。

## 更新間隔

ホロジュールにアクセスし情報を取得する間隔は、初期設定では10分ごとになっています。
同じく「config.ini」にて間隔を変更できます。ただし若干癖があります。

例(10分間隔)：

```
[Interval]
holodule_refresh = 10
```

これで0:00、0:10、0:20…と取得されます。

例(35分間隔)：

```
[Interval]
holodule_refresh = 35
```

これで0:00, 0:35, 1:10…に取得されます。問題は日が変わる前後で、23:20, **23:55**, **0:00**, 0:35…に取得されます。
これは起動してから35分ではなく、現在時刻が35分で割れる時に取得するからです。

なお、更新間隔の上限と下限はそれぞれ1分、1440分に設定されています。
ホロジュールの更新間隔はかなり短く、配信開始が遅れている場合、何度も同じ通知を出してしまう可能性があるため、10分以上の間隔が望ましいです(あと単にアクセスが増えてしまうため)。

## 【Windowsのみ】run.batについて

```
@echo off
start wt -p "Command Prompt" python holo_discord_webhook.py
exit
```

中身はこんな感じになっています。
これは「Windows ターミナル」(wt.exe)がインストールされている環境で実行できます。

もし宗教上の関係でターミナルをインストールしていない場合は以下のように書き換えてください。

```
@echo off
python holo_discord_webhook.py
exit
```

複数バージョンのPythonがインストールされている場合、環境変数「python」で起動されるPythonに必要なモジュールをインストールしてください。
もしくはバッチを書き換えて、目的のバージョンのPythonが起動できるようにしてください。
