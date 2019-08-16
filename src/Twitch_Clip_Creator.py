from twitch import TwitchClient
from moviepy.editor import VideoFileClip, concatenate_videoclips
import re, time, requests, sys, urllib.request, os

# scrape clips
def clip_scraper():
    client = TwitchClient(client_id='zlj6axia46p0bmv64275aj3jjdbf13')

    # clips.get_top docs
    # https://python-twitch-client.readthedocs.io/en/latest/v5/clips.html
    channel_info = client.clips.get_top(channel='koil', period='week', limit=2)

    # clips are output as 'https://clips.twitch.tv/KathishSweetWhalePrimeMe?tt_medium=clips_api&tt_content=url'
    # download link needs to split on '?'. Everything after '?' isn't needed
    # we split at '?'[0] and write to text file
    clip_urls = []
    ddmmyyyy = time.strftime("%d-%m-%y") # amazing variable name (example: dd-mm-yy)
    for item in channel_info:
        item['url'] = item['url'].split('?')[0] # take everything before '?'
        with open(f'C:\TwitchDownloader\src\Downloaded Clips {ddmmyyyy}.txt', 'a') as file:
            file.writelines(f"{item['url']}\n")
            print(item['url'])

clip_scraper()

# download clips
basepath = f'C:/TwitchDownloader/src/downloads/'
base_clip_path = 'https://clips-media-assets2.twitch.tv/'

def retrieve_mp4_data(slug):
    #cid = sys.argv[1]
    cid = 'zlj6axia46p0bmv64275aj3jjdbf13'
    clip_info = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + slug,
        headers={"Client-ID": cid}).json()
    thumb_url = clip_info['data'][0]['thumbnail_url']
    title = clip_info['data'][0]['title']
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + '.mp4'
    return mp4_url, title

def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()

# for each clip in clips.txt
ddmmyyyy = time.strftime("%d-%m-%y")
for clip in open(f'C:\TwitchDownloader\src\Downloaded Clips {ddmmyyyy}.txt', 'r'):
    slug = clip.split('/')[3].replace('\n', '')
    mp4_url, clip_title = retrieve_mp4_data(slug)
    regex = re.compile('[^a-zA-Z0-9_]')
    clip_title = clip_title.replace(' ', '_')
    out_filename = regex.sub('', clip_title) + '.mp4'
    output_path = (basepath + out_filename)

    print('\nDownloading clip slug: ' + slug)
    print('"' + clip_title + '" -> ' + out_filename)
    print(mp4_url)
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
    print('\nDone.')

print('Finished downloading all the videos.')

# merge clips
def clip_merge():
    os.chdir(r'C:\TwitchDownloader\src\downloads')
    clips = []
    for files in os.listdir(r'C:\TwitchDownloader\src\downloads'):
        if files.endswith('.mp4'):
            clips.append(VideoFileClip(files))
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("C:\TwitchDownloader\src\my_concatenation.mp4")

clip_merge()