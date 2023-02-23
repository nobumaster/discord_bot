import discord
import requests
from io import BytesIO
from PIL import Image
import area_code
import file_util

# intent設定
intents = discord.Intents.all()
# intents.guilds = Truearea_code
# intents.messages = True
client = discord.Client(intents=intents)

#例外 tokenとチャンネルID
BOT_TOKEN = file_util.read_text_file('token.txt')
CHANNEL_ID = file_util.read_text_file('channel.txt')

@client.event
async def on_ready():
    print('私のアツいアイドル活動！アイカツ！始まります！！')

@client.event
async def on_message(message):
    # デバック用
    # print(message.content)
    if message.author == client.user:
        print('BOTだよ')
        return

    # 絵文字の登録
    if message.content.startswith('芸能人は絵文字が命'):
        # メッセージに添付された画像を取得
        attachment = message.attachments[0]
        response = requests.get(attachment.url)
        img = Image.open(BytesIO(response.content))
        # 画像をリサイズ
        size = (128, 128)
        img.thumbnail(size)
        # リサイズした画像をバイト列に変換
        with BytesIO() as output:
            img.convert('RGBA').save(output, format='PNG')
            img_data = output.getvalue()
        # 絵文字として登録
        emoji_name = message.content.split(' ')[-1]
        emoji = await message.guild.create_custom_emoji(name=emoji_name, image=img_data)
        # 絵文字が登録されたらメッセージを送信
        if emoji:
            await message.channel.send('うんうん それもまたアイカツだね')
            await message.channel.send('{0}が登録されたよ！'.format(emoji_name))

    # 天気を知る
    # メッセージが辞書のキーのいずれかに合致する場合
    if any(code in message.content for code in area_code.area_codes_city.keys()) and "天気" in message.content:
        for code, city_name in area_code.area_codes_city.items():
            if code in message.content:
                url = area_code.get_weather(city_name,area_code.area_codes_town[code])
                await message.channel.send(f'{code}の天気は{url}\nだよ！')
                break

        

client.run(BOT_TOKEN)
