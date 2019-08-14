from twitch import TwitchClient

client = TwitchClient(client_id='zlj6axia46p0bmv64275aj3jjdbf13')

# clips.get_top docs
# https://python-twitch-client.readthedocs.io/en/latest/v5/clips.html
channel_info = client.clips.get_top(channel='koil', period='week', limit=100)

# write clip url to text file
for item in channel_info:
    with open('clips.txt', 'a') as file:
        file.writelines(f"{item['url']}\n")
        print(item['url'])