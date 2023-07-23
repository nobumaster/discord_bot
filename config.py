import file_util

MC_JARDIR = ""
# 別に直書きでもいいです
BOT_TOKEN = file_util.read_text_file('token.txt')
CHANNEL_ID = file_util.read_text_file('channel.txt')