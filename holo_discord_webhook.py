import re
import time
import requests
from requests.exceptions import ConnectionError, Timeout, ChunkedEncodingError
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

webhook_url_Hololive = ''
holodule_url = 'https://schedule.hololive.tv/'
holodule_list = []

#配信者のチャンネルID, 配信者名, アイコン画像のURLのリスト
Hololive = {
    "ときのそら": [
        "ときのそら",
        "https://hololive.hololivepro.com/wp-content/uploads/2021/05/tokino_sora_thumb.png",
        "https://www.youtube.com/channel/UCp6993wxpyDPHUpavwDFqgg"
    ],
    "AZKi": [
        "AZKi",
        "https://hololive.hololivepro.com/wp-content/uploads/2022/12/AZKi_list_thumb.png",
        "https://www.youtube.com/channel/UC0TXe_LYZ4scaW2XMyi5_kw"
    ],
    "ロボ子さん": [
        "ロボ子さん",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/06/roboco-san_thumb.png",
        "https://www.youtube.com/channel/UCDqI2jOz0weumE8s7paEk6g"
    ],
    "さくらみこ": [
        "さくらみこ",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/02/Sakura-Miko_thumb.png",
        "https://www.youtube.com/channel/UC-hM6YJuNYVAmUWxeIr9FeA"
    ],
    "白上フブキ": [
        "白上フブキ",
        "https://hololive.hololivepro.com/wp-content/uploads/2021/05/shirakami_fubuki_thumb.png",
        "https://www.youtube.com/channel/UCdn5BQ06XqgXoAxIhbqw5Rg"
    ],
    "夏色まつり": [
        "夏色まつり",
        "https://hololive.hololivepro.com/wp-content/uploads/2021/05/natsuiro_matsuri_thumb.png",
        "https://www.youtube.com/channel/UCQ0UDLQCjY0rmuxCDE38FGg"
    ],
    "夜空メル": [
        "夜空メル",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Yozora-Mel_list_thumb.png",
        "https://www.youtube.com/channel/UCD8HOxPs4Xvsm8H0ZxXGiBw"
    ],
    "赤井はあと": [
        "赤井はあと",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Akai-Haato_list_thumb.png",
        "https://www.youtube.com/channel/UC1CfXB_kRs3C-zaeTG3oGyg"
    ],
    "アキロゼ": [
        "アキ・ローゼンタール",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Aki-Rosenthal_list_thumb.png",
        "https://www.youtube.com/channel/UCFTLzh12_nrtzqBPsTCqenA"
    ],
    "湊あくあ": [
        "湊あくあ",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Minato-Aqua_list_thumb.png",
        "https://www.youtube.com/channel/UC1opHUrw8rvnsadT-iGp7Cg"
    ],
    "癒月ちょこ": [
        "癒月ちょこ",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Yuzuki-Choco_list_thumb.png",
        "https://www.youtube.com/channel/UC1suqwovbL1kzsoaZgFZLKg"
    ],
    "百鬼あやめ": [
        "百鬼あやめ",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/10/Nakiri-Ayame_list_thumb.png",
        "https://www.youtube.com/channel/UC7fk0CB07ly8oSl0aqKkqFg"
    ],
    "紫咲シオン": [
        "紫咲シオン",
        "https://hololive.hololivepro.com/wp-content/uploads/2021/12/shion_thumb.png",
        "https://www.youtube.com/channel/UCXTpFs_3PqI41qX2d9tL2Rw"
    ],
    "大空スバル": [
        "大空スバル",
        "https://hololive.hololivepro.com/wp-content/uploads/2021/05/oozora_subaru_thumb.png",
        "https://www.youtube.com/channel/UCvzGlP9oQwU--Y0r9id_jnA"
    ],
    "大神ミオ": [
        "大神ミオ",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/01/Ookami-Mio_thumb.png",
        "https://www.youtube.com/channel/UCp-5t9SrOQwXMU7iIjQfARg"
    ],
    "猫又おかゆ": [
        "猫又おかゆ",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/06/Nekomata-Okayu_list_thumb.png",
        "https://www.youtube.com/channel/UCvaTdHTWBGv3MKj3KVqJVCw"
    ],
    "戌神ころね": [
        "戌神ころね",
        "https://hololive.hololivepro.com/wp-content/uploads/2021/05/inugami_korone_thumb.png",
        "https://www.youtube.com/channel/UChAnqc_AY5_I3Px5dig3X1Q"
    ],
    "不知火フレア": [
        "不知火フレア",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Shiranui-Flare_list_thumb.png",
        "https://www.youtube.com/channel/UCvInZx9h3jC2JzsIzoOebWg"
    ],
    "白銀ノエル": [
        "白銀ノエル",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/01/Shirogane-Noel_thumb.png",
        "https://www.youtube.com/channel/UCdyqAaZDKHXg4Ahi7VENThQ"
    ],
    "宝鐘マリン": [
        "宝鐘マリン",
        "https://hololive.hololivepro.com/wp-content/uploads/2021/05/houshou_marine_thumb.png",
        "https://www.youtube.com/channel/UCCzUftO8KOVkV4wQG1vkUvg"
    ],
    "兎田ぺこら": [
        "兎田ぺこら",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Usada-Pekora_list_thumb.png",
        "https://www.youtube.com/channel/UC1DCedRgGHBdm81E1llLhOQ"
    ],
    "潤羽るしあ": [
        "潤羽るしあ",
        "https://hololive.hololivepro.com/wp-content/uploads/2021/11/uruha_rushia_thumb.png",
        "https://www.youtube.com/channel/UCl_gCybOJRIgOXw6Qb4qJzQ"
    ],
    "星街すいせい": [
        "星街すいせい",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Hoshimachi-Suisei_list_thumb-1.png",
        "https://www.youtube.com/channel/UC5CwaMl1eIgY8h02uZw7u8A"
    ],
    "天音かなた": [
        "天音かなた",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Amane-Kanata_list_thumb.png",
        "https://www.youtube.com/channel/UCZlDXzGoo7d44bwdNObFacg"
    ],
    "桐生ココ": [
        "桐生ココ",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Kiryu-Coco_list_thumb-1.png",
        "https://www.youtube.com/channel/UCS9uQI-jC3DE0L4IpXyvr6w"
    ],
    "角巻わため": [
        "角巻わため",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/04/Tsunomaki-Watame_list_thumb-1.png",
        "https://www.youtube.com/channel/UCqm3BQLlJfvkTsX_hvm0UmA"
    ],
    "常闇トワ": [
        "常闇トワ",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/06/Tokoyami-Towa_list_thumb.png",
        "https://www.youtube.com/channel/UC1uv2Oq6kNxgATlCiez59hw"
    ],
    "姫森ルーナ": [
        "姫森ルーナ",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/07/Himemori-Luna_list_thumb.png",
        "https://www.youtube.com/channel/UCa9Y57gfeY0Zro_noHRVrnw"
    ],
    "雪花ラミィ": [
        "雪花ラミィ",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/06/Yukihana-Lamy_list_thumb.png",
        "https://www.youtube.com/channel/UCFKOVgVbGmX65RxO3EtH3iw"
    ],
    "桃鈴ねね": [
        "桃鈴ねね",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/06/Momosuzu-Nene_list_thumb.png",
        "https://www.youtube.com/channel/UCAWSyEs_Io8MtpY3m-zqILA"
    ],
    "獅白ぼたん": [
        "獅白ぼたん",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/05/Shishiro-Botan_list_thumb.png",
        "https://www.youtube.com/channel/UCUKD-uaobj9jiqB-VXt71mA"
    ],
    "尾丸ポルカ": [
        "尾丸ポルカ",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/06/Omaru-Polka_list_thumb.png",
        "https://www.youtube.com/channel/UCK9V2B22uJYu3N7eR_BT9QA"
    ],
    "ラプラス": [
        "ラプラス・ダークネス",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/05/La-Darknesss_list_thumb.png",
        "https://www.youtube.com/channel/UCENwRMx5Yh42zWpzURebzTw"
    ],
    "鷹嶺ルイ": [
        "鷹嶺ルイ",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/08/Takane-Lui_list_thumb.png",
        "https://www.youtube.com/channel/UCs9_O1tRPMQTHQ-N_L6FU2g"
    ],
    "博衣こより": [
        "博衣こより",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/07/Hakui-Koyori_list_thumb.png",
        "https://www.youtube.com/channel/UC6eWCld0KwmyHFbAqK3V-Rw"
    ],
    "沙花叉クロヱ": [
        "沙花叉クロヱ",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/07/Sakamata-Chloe_list_thumb.png",
        "https://www.youtube.com/channel/UCIBY1ollUsauvVi4hW4cumw"
    ],
    "風真いろは": [
        "風真いろは",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/07/Kazama-Iroha_list_thumb.png",
        "https://www.youtube.com/channel/UC_vMYWcDjmfdpH6r4TTn1MQ"
    ],
    "Iofi": [
        "Airani Iofifteen / アイラニ・イオフィフティーン",
        "https://hololive.hololivepro.com/wp-content/uploads/2022/04/%E3%82%A4%E3%82%AA%E3%83%95%E3%82%A3-1.png",
        "https://www.youtube.com/channel/UCAoy6rzhSf4ydcYjJw3WoVg"
    ],
    "Moona": [
        "Moona Hoshinova / ムーナ・ホシノヴァ",
        "https://hololive.hololivepro.com/wp-content/uploads/2022/04/%E3%83%A0%E3%83%BC%E3%83%8A-1.png",
        "https://www.youtube.com/channel/UCP0BspO_AMEe3aQqqpo89Dg"
    ],
    "Risu": [
        "Ayunda Risu / アユンダ・リス",
        "https://hololive.hololivepro.com/wp-content/uploads/2022/04/%E3%83%AA%E3%82%B9-1.png",
        "https://www.youtube.com/channel/UCOyYb1c43VlX9rc_lT6NKQw"
    ],
    "Ollie": [
        "Kureiji Ollie / クレイジー・オリー",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/06/Kureiji-Ollie_list_thumb.png",
        "https://www.youtube.com/channel/UCYz_5n-uDuChHtLo7My1HnQ"
    ],
    "Anya": [
        "Anya Melfissa / アーニャ・メルフィッサ",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/07/Anya-Melfissa_list_thumb.png",
        "https://www.youtube.com/channel/UC727SQYUvx5pDDGQpTICNWg?"
    ],
    "Reine": [
        "Pavolia Reine / パヴォリア・レイネ",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/07/Pavolia-Reine_list_thumb.png",
        "https://www.youtube.com/channel/UChgTyjG-pdNvxxhdsXfHQ5Q?"
    ],
    "Zeta": [
        "Vestia Zeta / ベスティア・ゼータ",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/11/Vestia-Zeta_list_thumb.png",
        "https://www.youtube.com/channel/UCTvHWSfBZgtxE4sILOaurIQ"
    ],
    "Kaela": [
        "Kaela Kovalskia / カエラ・コヴァルスキア",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/09/Kaela-Kovalskia_list_thumb.png",
        "https://www.youtube.com/channel/UCZLZ8Jjx_RN2CXloOmgTHVg"
    ],
    "Kobo": [
        "Kobo Kanaeru / こぼ・かなえる",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/11/Kobo-Kanaeru_list_thumb.png",
        "https://www.youtube.com/channel/UCjLEmnpCNeisMxy134KPwWw"
    ],
    "Calli": [
        "Mori Calliope / 森カリオペ",
        "https://hololive.hololivepro.com/wp-content/uploads/2022/04/%E3%82%AB%E3%83%AA%E3%82%AA%E3%83%9A.png",
        "https://www.youtube.com/channel/UCL_qhgtOy0dy1Agp8vkySQg"
    ],
    "Kiara": [
        "Takanashi Kiara / 小鳥遊キアラ",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/01/Takanashi-Kiara_thumb.png",
        "https://www.youtube.com/channel/UCHsx4Hqa-1ORjQTh9TYDhww"
    ],
    "Ina": [
        "Ninomae Ina'nis / 一伊那尓栖",
        "https://hololive.hololivepro.com/wp-content/uploads/2022/04/%E3%81%84%E3%81%AA%E3%81%AB%E3%81%99.png",
        "https://www.youtube.com/channel/UCMwGHR0BTZuLsmjY_NT5Pwg"
    ],
    "Gura": [
        "Gawr Gura / がうる・ぐら",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/05/Gawr-Gura_list_thumb.png",
        "https://www.youtube.com/channel/UCoSrY_IQQVpmIRZ9Xf-y93g"
    ],
    "Amelia": [
        "Watson Amelia / ワトソン・アメリア",
        "https://hololive.hololivepro.com/wp-content/uploads/2022/04/%E3%82%A2%E3%83%A1%E3%83%AA%E3%82%A2.png",
        "https://www.youtube.com/channel/UCyl1z3jo3XHR1riLFKG5UAg"
    ],
    "IRyS": [
        "IRyS",
        "https://hololive.hololivepro.com/wp-content/uploads/2020/07/IRyS_list_thumb.png",
        "https://www.youtube.com/channel/UC8rcEBzJSleTkf_-agPM20g"
    ],
    "Sana": [
        "Tsukumo Sana / 九十九佐命",
        "https://hololive.hololivepro.com/wp-content/uploads/2021/08/%E4%B9%9D%E5%8D%81%E4%B9%9D-%E4%BD%90%E5%91%BD-1.png",
        "https://www.youtube.com/channel/UCsUj0dszADCGbF3gNrQEuSQ"
    ],
    "Fauna": [
        "Ceres Fauna / セレス・ファウナ",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/10/Ceres-Fauna_list_thumb.png",
        "https://www.youtube.com/channel/UCO_aKKYxn4tvrqPjcTzZ6EQ"
    ],
    "Kronii": [
        "Ouro Kronii / オーロ・クロニー",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/10/Ouro-Kronii_list_thumb.png",
        "https://www.youtube.com/channel/UCmbs8T6MWqUHP1tIQvSgKrg"
    ],
    "Mumei": [
        "Nanashi Mumei / 七詩ムメイ",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/10/Nanashi-Mumei_list_thumb.png",
        "https://www.youtube.com/channel/UC3n5uGu18FoCy23ggWWp8tA"
    ],
    "Baelz": [
        "Hakos Baelz / ハコス・ベールズ",
        "https://hololive.hololivepro.com/wp-content/uploads/2023/10/Hakos-Baelz_list_thumb.png",
        "https://www.youtube.com/channel/UCgmPnx-EEeOrZSg5Tiw7ZRQ"
    ],
    "Shiori": [
        "Shiori Novella / シオリ・ノヴェラ",
        "https://hololive.hololivepro.com/wp-content/uploads/2021/07/Shiori-Novella_list_thumb.png",
        "https://www.youtube.com/channel/UCgnfPPb9JI3e9A4cXHnWbyg"
    ],
    "Bijou": [
        "Koseki Bijou / 古石ビジュー",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/08/Koseki-Bijou_list_thumb.png",
        "https://www.youtube.com/channel/UC9p_lqQ0FEDz327Vgf5JwqA"
    ],
    "Nerissa": [
        "Nerissa Ravencroft / ネリッサ・レイヴンクロフト",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/08/Nerissa-Ravencroft_list_thumb.png",
        "https://www.youtube.com/channel/UC_sFNM0z0MWm9A6WlKPuMMg"
    ],
    "FUWAMOCO": [
        "Fuwawa&Mococo Abyssgard / フワワ&モココ・アビスガード",
        "https://yt3.googleusercontent.com/zt63obGOD6fnCX0elnzt8xkylqOTnAENmSCKmwg_PSiC857DDgB28kEjQ-FJlWGtNYZ9lqzEag",
        "https://www.youtube.com/channel/UCt9H_RpQzhxzlyBxFqrdHqA"
    ],
    "Elizabeth": [
        "Elizabeth Rose Bloodflame / エリザベス・ローズ・ブラッドフレイム",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/06/Elizabeth-Rose-Bloodflame_list_thumb.png",
        "https://www.youtube.com/@holoen_erbloodflame"
    ],
    "Gigi": [
        "Gigi Murin / ジジ・ムリン",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/06/Gigi-Murin_list_thumb.png",
        "https://www.youtube.com/@holoen_gigimurin"
    ],
    "Cecilia": [
        "Cecilia Immergreen / セシリア・イマーグリーン",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/06/Cecilia-Immergreen_list_thumb.png",
        "https://www.youtube.com/@holoen_ceciliaimmergreen"
    ],
    "Raora": [
        "Raora Panthera / ラオーラ・パンテーラ",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/06/Raora-Panthera_list_thumb.png",
        "https://www.youtube.com/@holoen_raorapanthera"
    ],
    "火威青": [
        "火威青",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/10/Hiodoshi-Ao_list_thumb.png",
        "https://www.youtube.com/channel/UCMGfV7TVTmHhEErVJg1oHBQ"
    ],
    "音乃瀬奏": [
        "音乃瀬奏",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/10/Otonose-Kanade_list_thumb.png",
        "https://youtube.com/@OtonoseKanade"
    ],
    "一条莉々華": [
        "一条莉々華",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/10/Ichijou-Ririka_list_thumb.png",
        "https://www.youtube.com/@IchijouRirika"
    ],
    "儒烏風亭らでん": [
        "儒烏風亭らでん",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/10/Juufuutei-Raden_list_thumb.png",
        "https://www.youtube.com/@JuufuuteiRaden"
    ],
    "轟はじめ": [
        "轟はじめ",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/10/Todoroki-Hajime_list_thumb.png",
        "https://www.youtube.com/@TodorokiHajime"
    ],
    "響咲リオナ": [
        "響咲リオナ",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/11/Isaki-Riona_list_thumb.png",
        "https://www.youtube.com/@IsakiRiona"
    ],
    "虎金妃笑虎": [
        "虎金妃笑虎",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/10/Otonose-Kanade_list_thumb.png",
        "https://www.youtube.com/@KoganeiNiko"
    ],
    "水宮枢": [
        "水宮枢",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/10/Ichijou-Ririka_list_thumb.png",
        "https://www.youtube.com/@MizumiyaSu"
    ],
    "輪堂千速": [
        "輪堂千速",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/10/Juufuutei-Raden_list_thumb.png",
        "https://www.youtube.com/@RindoChihaya"
    ],
    "綺々羅々ヴィヴィ": [
        "綺々羅々ヴィヴィ",
        "https://hololive.hololivepro.com/wp-content/uploads/2024/10/Todoroki-Hajime_list_thumb.png",
        "https://www.youtube.com/@KikiraraVivi"
    ],
    "花咲みやび": [
        "花咲みやび",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Hanasaki-Miyabi_list_thumb.png",
        "https://www.youtube.com/channel/UC6t3-_N8A6ME1JShZHHqOMw"
    ],
    "奏手イヅル": [
        "奏手イヅル",
        "https://holostars.hololivepro.com/wp-content/uploads/2024/08/Kanade-Izuru_list_thumb.png",
        "https://www.youtube.com/channel/UCZgOv3YDEs-ZnZWDYVwJdmA"
    ],
    "アルランディス": [
        "アルランディス",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Arurandeisu_list_thumb.png",
        "https://www.youtube.com/channel/UCKeAhJvy8zgXWbh9duVjIaQ"
    ],
    "律可": [
        "律可",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Rikka_list_thumb.png",
        "https://www.youtube.com/channel/UC9mf_ZVpouoILRY9NUIaK-w"
    ],
    "アステル・レダ": [
        "アステル・レダ",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Astel-Leda_list_thumb.png",
        "https://www.youtube.com/channel/UCNVEsYbiZjH5QLmGeSgTSzg"
    ],
    "岸堂天真": [
        "岸堂天真",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Kishido-Temma_list_thumb.png",
        "https://www.youtube.com/channel/UCGNI4MENvnsymYjKiZwv9eg"
    ],
    "夕刻ロベル": [
        "夕刻ロベル",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Yukoku-Roberu_list_thumb.png",
        "https://www.youtube.com/channel/UCANDOlYTJT7N5jlRC3zfzVA"
    ],
    "影山シエン": [
        "影山シエン",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Kageyama-Shien_list_thumb.png",
        "https://www.youtube.com/channel/UChSvpZYRPh0FvG4SJGSga3g"
    ],
    "荒咬オウガ": [
        "荒咬オウガ",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Aragami-Oga_list_thumb.png",
        "https://www.youtube.com/channel/UCwL7dgTxKo8Y4RFIKWaf8gA"
    ],
    "夜十神封魔": [
        "夜十神封魔",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Yatogami-Fuma_list_thumb.png",
        "https://www.youtube.com/channel/UCc88OV45ICgHbn3ZqLLb52w"
    ],
    "羽継烏有": [
        "羽継烏有",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Utsugi-Uyu_list_thumb.png",
        "https://www.youtube.com/channel/UCgRqGV1gBf2Esxh0Tz1vxzw"
    ],
    "緋崎ガンマ": [
        "緋崎ガンマ",
        "https://holostars.hololivepro.com/wp-content/uploads/2022/12/Hizaki-Gamma_thumb.png",
        "https://www.youtube.com/channel/UCkT1u65YS49ca_LsFwcTakw"
    ],
    "水無世燐央": [
        "水無世燐央",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Minase-Rio_list_thumb.png",
        "https://www.youtube.com/channel/UCdfMHxjcCc2HSd9qFvfJgjg"
    ],
    "Altare": [
        "Regis Altare / リージス・アルテア",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Regis-Altare_list_thumb.png",
        "https://www.youtube.com/channel/UCyxtGMdWlURZ30WSnEjDOQw"
    ],
    "Syrios": [
        "Axel Syrios / アクセル・シリオス",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Axel-Syrios_list_thumb.png",
        "https://www.youtube.com/channel/UC2hx0xVkMoHGWijwr_lA01w"
    ],
    "Bettel": [
        "Gavis Bettel / ガビス・ベッテル",
        "https://holostars.hololivepro.com/wp-content/uploads/2024/06/Gavis-Bettel_list_thumb.png",
        "https://www.youtube.com/channel/UCHP4f7G2dWD4qib7BMatGAw"
    ],
    "Flayon": [
        "Machina X Flayon / マキナ・X・フレオン",
        "https://holostars.hololivepro.com/wp-content/uploads/2024/06/Machina-X-Flayon_list_thumb.png",
        "https://www.youtube.com/channel/UC060r4zABV18vcahAWR1n7w"
    ],
    "Hakka": [
        "Hakka / 万象院ハッカ",
        "https://holostars.hololivepro.com/wp-content/uploads/2024/06/Banzoin-Hakka_list_thumb.png",
        "https://www.youtube.com/channel/UC7gxU6NXjKF1LrgOddPzgTw"
    ],
    "Shinri": [
        "Josuiji Shinri / 定水寺シンリ",
        "https://holostars.hololivepro.com/wp-content/uploads/2024/06/Josuiji-Shinri_list_thumb.png",
        "https://www.youtube.com/channel/UCMqGG8BRAiI1lJfKOpETM_w"
    ],
    "Jurard": [
        "Jurard T Rexford / ジュラルド・ティー・レクスフォード",
        "https://holostars.hololivepro.com/wp-content/uploads/2023/01/Jurard-T-Rexford_list_thumb.png",
        "https://www.youtube.com/channel/UCTVSOgYuSWmNAt-lnJPkEEw"
    ],
    "Goldbullet": [
        "Goldbullet / ゴールドブレット",
        "https://holostars.hololivepro.com/wp-content/uploads/2023/01/Goldbullet_list_thumb.png",
        "https://youtube.com/channel/UCJv02SHZgav7Mv3V0kBOR8Q"
    ],
    "Octavio": [
        "Octavio / オクタビオ",
        "https://holostars.hololivepro.com/wp-content/uploads/2023/01/Octavio_list_thumb.png",
        "https://www.youtube.com/channel/UCLk1hcmxg8rJ3Nm1_GvxTRA"
    ],
    "Crimzon": [
        "Crimzon Ruze / クリムゾン・ルーズ",
        "https://holostars.hololivepro.com/wp-content/uploads/2023/01/Crimzon-Ruze_list_thumb.png",
        "https://www.youtube.com/channel/UCajbFh6e_R8QZdHAMbbi4rQ"
    ],
    "鏡見キラ": [
        "鏡見キラ",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/%E3%82%AD%E3%83%A9%EF%BC%9A%E3%82%B5%E3%83%A0%E3%83%8D.png",
        "https://www.youtube.com/channel/UCEzsociuFqVwgZuMaZqaCsg"
    ],
    "Dezmond": [
        "Dezmond / マグニ・デズモンド",
        "https://holostars.hololivepro.com/wp-content/uploads/2023/06/Magni-Dezmondt_list_thumb.png",
        "https://www.youtube.com/channel/UC7MMNHR-kf9EN1rXiesMTMw"
    ],
    "Vesper": [
        "Noir Vesper / ノワール・ヴェスパー",
        "https://holostars.hololivepro.com/wp-content/uploads/2021/12/Noir-Vesper_list_thumb.png",
        "https://www.youtube.com/channel/UCDRWSO281bIHYVi-OV3iFYA"
    ],
    "ホロライブ": [
        "ホロライブ公式チャンネル",
        "https://yt3.ggpht.com/ytc/AKedOLTj0OSWM9TvPy4e8v1_o99OtP3Bg7FXthdkgr2bCQ=s288-c-k-c0xffffffff-no-rj-mo",
        "https://www.youtube.com/@hololive"
    ],
    "holo EN": [
        "hololive English",
        "https://yt3.googleusercontent.com/nfg9n5podc7KZsdkBdsKDRhpddQrC4Pa5XDphTlDUMc3vM1HXcxunI6FLDCBSwYe70zkTgEb3A=s176-c-k-c0x00ffffff-no-rj",
        "https://www.youtube.com/@hololiveEnglish"
    ],
    "holo ID": [
        "hololive Indonesia",
        "https://yt3.googleusercontent.com/ytc/AIdro_nqRoQYVOioAVLFHDrRP_y8Ri4zAUoq3kxEdHrQQLyrp44=s176-c-k-c0x00ffffff-no-rj",
        "https://www.youtube.com/@hololiveIndonesia"
    ],
    "hololive DEV_IS": [
        "hololive DEV_IS",
        "https://yt3.googleusercontent.com/KTypB1brQ2yd1KtZUBo4Y533L9kHmNeB1Q9aHZyfqWm3YE_6EOL10VYWj4LVRTwQ2jtg6hMyJQ",
        "https://www.youtube.com/@hololiveDEV_IS"
    ],
    "FLOW GLOW": [
        "hololive DEV_IS FLOW GLOW",
        "https://yt3.googleusercontent.com/ypxkfw18lthQENaCFsvuWT5dBtoIkDnFpMc8NASkgwFSospslVrIwt5gFZeq9TerPYeQktoS=s160-c-k-c0x00ffffff-no-rj",
        "https://www.youtube.com/@DEV_IS_FLOWGLOW"
    ],
    "ホロスターズ": [
        "ホロスターズ公式チャンネル",
        "https://yt3.googleusercontent.com/5Jn_OHkOZhZssXXwWopUQZVwnL16EJivvxTDGqVmp4Cah3nLmVTgZMQmfF-SyuMhtFkncyT9Lw=s176-c-k-c0x00ffffff-no-rj",
        "https://www.youtube.com/@HOLOSTARS"
    ],
    "HOLOSTARS EN": [
        "HOLOSTARS English",
        "https://yt3.googleusercontent.com/jvGFuTmqlv5udorr8TGYsllUntfo0yXRn2hpWrvjWz_nso1-tTQ2J3TPV616F-JLHLKB4s65=s176-c-k-c0x00ffffff-no-rj",
        "https://www.youtube.com/@HOLOSTARSEnglish"
    ]
}

class Holodule:
    datetime = None
    name = ""
    url = ""

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
                        # print(holodule.url)
                    # 時刻（先に取得しておいた日付と合体）
                    div_time = thumbnail.find('div', class_="col-4 col-sm-4 col-md-4 text-left datetime")
                    if div_time is not None:
                        time_text = div_time.text.strip()
                        match_time = re.search(r'[0-9]{1,2}:[0-9]{1,2}', time_text)
                        times = match_time.group(0).split(":")
                        hour = int(times[0])
                        minute = int(times[1])
                        datetime_string = f"{date_string} {hour}:{minute}"
                        holodule.datetime = datetime.strptime(datetime_string, "%Y/%m/%d %H:%M")
                    # ライバーの名前
                    div_name = thumbnail.find('div', class_="col text-right name")
                    if div_name is not None:
                        holodule.name = div_name.text.strip()
                    # リストに追加
                    holodule_list.append(holodule)
        print('[\033[36mInfo\033[0m]List length:' + str(len(holodule_list)))
    except ConnectionError:
        print('[\033[31mError\033[0m]Refresh Holodule Failed(ConnectionError).')
        print('Tried time: [' + str(datetime.now().hour) + ':' + str(datetime.now().minute) + ']')
    except Timeout:
        print('[\033[31mError\033[0m]Refresh Holodule Failed(Timeout).')
        print('Tried time: [' + str(datetime.now().hour) + ':' + str(datetime.now().minute) + ']')
    except ChunkedEncodingError:
        print('[\033[31mError\033[0m]Refresh Holodule Failed(ChunkedEncodingError).')
        print('Tried time: [' + str(datetime.now().hour) + ':' + str(datetime.now().minute) + ']')

def check_schedule(now_time, holodule_list):
    for bd in list(holodule_list):
        try:
            now_time10 = now_time + timedelta(minutes=10)
            sd_time = bd.datetime
            if sd_time == None:
                continue
            if(now_time10.hour == sd_time.hour and now_time10.minute == sd_time.minute and now_time10.month == sd_time.month and now_time10.day == sd_time.day):
                print('・' + bd.name + '[\033[33m' + str(sd_time) + '\033[0m]')
                post_broadcast_schedule(bd.name, bd.url, sd_time) #ツイート
        except KeyError:
            continue

def post_broadcast_schedule(userName, videoUrl, starttime):
    if not userName in Hololive:
        print('[\033[33mIgnored\033[0m]"' + userName + '" is not in list.')
        return
    st_hour = str(starttime.hour)
    st_min = str(starttime.minute)
    st = st_hour + ':' + mindec(st_min)
    #Discordに投稿される文章
    content = "10分後に配信開始予定！（予定時刻：" + st + '）\n' + videoUrl
    main_content = {
        "username": Hololive[userName][0], #配信者名
        "avatar_url": Hololive[userName][1], #アイコン
        "content": content #文章
    }
    time.sleep(1)
    requests.post(webhook_url_Hololive, main_content) #Discordに送信

def mindec(min):
    if len(str(min)) == 1:
        min = '0' + str(min)
    return min

get_holodule()
print('[\033[36mNotice\033[0m]Start up complete.')

while True:
    now_time = datetime.now()
    if(now_time.minute % 10 == 0 and now_time.second == 0):
        get_holodule()
        print('[\033[36mInfo\033[0m][\033[33m' + str(now_time.hour) + ':' + str(mindec(now_time.minute)) + '\033[0m]Scheduled Refresh Holodule.')
    if(now_time.second == 0):
        check_schedule(now_time, holodule_list)
    time.sleep(1)