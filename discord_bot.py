import discord
import requests
from io import BytesIO
from PIL import Image

# intent設定
intents = discord.Intents.all()
# intents.guilds = True
# intents.messages = True
client = discord.Client(intents=intents)

#例外 tokenとチャンネルID
BOT_TOKEN = ''
CHANNEL_ID = ''

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

client.run(BOT_TOKEN)
