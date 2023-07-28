import discord
import requests
from io import BytesIO
from PIL import Image
import area_code
import file_util
import git_util
import sys
import subprocess
import os
import asyncio
import glob
import re
try:
    import config
except ImportError:
    raise ImportError("config.pyが見つかりません")

# intent設定
intents = discord.Intents.all()
# intents.guilds = Truearea_code
# intents.messages = True
client = discord.Client(intents=intents)

# チャンネルを作成
async def create_channel(category_name, channel_name):
    try:
        # カテゴリを取得する
        category = discord.utils.get(client.guilds[0].categories, name=category_name)
        if not category:
            # カテゴリが存在しない場合は作成する
            category = await client.guilds[0].create_category(category_name)

        # チャンネルを作成する
        new_channel = await category.create_text_channel(channel_name)
        # チャンネルのIDを返す
        return new_channel.id
    except Exception as e:
        print(f"Failed to create channel: {e}")
        return None
    
# チャンネルをアーカイブに移動する
async def move_channel(channel_name, category_name):
    # 移動するチャンネルを取得する
    channel = discord.utils.get(client.guilds[0].channels, name=channel_name)
    if channel:
        # 移動先のカテゴリを取得する
        category = discord.utils.get(client.guilds[0].categories, name=category_name)
        if category:
            # チャンネルを移動する
            await channel.edit(category=category, reason="Moved to category")
            # 通知をオフにする
            await channel.edit(sync_permissions=True, reason="Turn off notifications")
            await channel.set_permissions(client.guild.default_role, read_messages=False)
            print(f"Moved channel {channel_name} to category {category_name} and turned off notifications.")
            return True
        else:
            print(f"Category {category_name} not found.")
            return False
    else:
        print(f"Channel {channel_name} not found.")
        return False
    
#tokenとチャンネルIDをtxtファイルから取る
BOT_TOKEN = config.BOT_TOKEN
CHANNEL_ID = config.CHANNEL_ID


useMcServer = True
mc_jardir = ''

try:
    jar_directory = config.MC_JARDIR
    useMcServer = bool(jar_directory)
except AttributeError:
    print("MC_JARDIRが定義されていません")
    useMcServer = False

@client.event
async def on_ready():
    print('私のアツいアイドル活動！アイカツ！始まります！！')
    if not useMcServer:
        print('MCServerの機能は使用しません')


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
            await message.channel.send(f'{emoji_name}が登録されたよ！')

    # 天気を知る
    # メッセージが辞書のキーのいずれかに合致する場合
    if any(code in message.content for code in area_code.area_codes_city.keys()) and "天気" in message.content:
        for code, city_name in area_code.area_codes_city.items():
            if code in message.content:
                url = area_code.get_weather(city_name,area_code.area_codes_town[code])
                await message.channel.send(f'{code}の天気は{url}\nだよ！')
                break
    
    # デバック用
    if 'おはよう' in message.content:
        await message.channel.send(f'おはよう！{message.author.name}くん！')
    if 'いちごちゃんまたね' in message.content:
        await message.channel.send(f'BOTを停止するね！')
        sys.exit()

    # mainからgit pullする
    if message.content.startswith('いちごをアップデート'):
        branch,result = git_util.git_pull()
        if result:
            await message.channel.send(f'最新のわたしになったよ！')
            subprocess.Popen(['nohup', 'python', 'discord_bot.py', '>/dev/null', '2>&1', '&'], shell=True)
            await message.channel.send(f'再起動するね！')
            sys.exit()
        else:
            await message.channel.send(f'失敗しちゃったみたい・・・')

    if message.content.startswith('チャンネル作成'):
        list = message.content.split("\n")
        if len(list) < 3:  # メッセージが不十分な場合
            await message.channel.send('カテゴリ名とチャンネル名を指定してください\n例:チャンネル作成\nカテゴリ\nチャンネル')
        else:
            new_channel_id = await create_channel(list[1],list[2])
            if new_channel_id:
                await message.channel.send(f'{list[1]}を作成したよ！ こちら <#{new_channel_id}>')
            else:
                await message.channel.send(f'チャンネル作成に失敗しました')

    if message.content.startswith('チャンネルアーカイブ'):
        result = await move_channel(message.channel.name,'Archive') # 'await'を付けて呼び出し
        if result:
            await message.channel.send(f'チャンネルをアーカイブにしたよ！')
        else:
            await message.channel.send(f'チャンネルアーカイブに失敗しました')

    # configで設定したキーがメッセージにマッチしたら対応するパスのシェルスクリプトを実行
    if message.content in config.SH_DICTIONARY:
        script_path = config.SH_DICTIONARY[message.content]

        if not os.path.isfile(script_path):
            await message.channel.send(f'スクリプトファイルが見つかりません: {script_path}')
        else:
            try:
                subprocess.check_call(['/bin/sh', script_path])
            except subprocess.CalledProcessError:
                await message.channel.send(f'スクリプトの実行に失敗しました: {script_path}')

client.run(BOT_TOKEN)
