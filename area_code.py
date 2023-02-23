import requests
from bs4 import BeautifulSoup

area_codes_town = {
    '東京': '4410',
    '大阪': '6200',
    '名古屋': '5110',
    '横浜': '4610',
    '長野': '4810',
    '札幌': '1400',
    '沖縄': '9110',
}
area_codes_city = {
    '東京': '13',
    '大阪': '27',
    '名古屋': '23',
    '横浜': '14',
    '長野': '20',
    '札幌': '1',
    '沖縄': '47'
}

# Yahoo!天気情報のWebページから、指定された地域コードに対応する地域の天気情報URL取得
def get_weather(city_code,town_code):
    url = f"https://weather.yahoo.co.jp/weather/jp/{city_code}/{town_code}.html"
    # 地域名、日付、天気情報の文字列からなるタプル。
    return url
