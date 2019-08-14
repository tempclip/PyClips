from twitch import TwitchClient
import time

client = TwitchClient(client_id='zlj6axia46p0bmv64275aj3jjdbf13')

# clips.get_top docs
# https://python-twitch-client.readthedocs.io/en/latest/v5/clips.html
channel_info = client.clips.get_top(channel='koil', period='week', limit=20)

# clips are output as 'https://clips.twitch.tv/KathishSweetWhalePrimeMe?tt_medium=clips_api&tt_content=url'
# download link needs to split on '?'. Everything after '?' isn't needed
# we split at '?'[0] and write to text file

clip_urls = []
ddmmyyyy = time.strftime("%d-%m-%y") # amazing variable name (example: dd-mm-yy)
for item in channel_info:
    item['url'] = item['url'].split('?')[0] # take everything before '?'
    with open(f'Downloaded Clips {ddmmyyyy}.txt', 'a') as file:
        file.writelines(f"{item['url']}\n")
        print(item['url'])