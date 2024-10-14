import os
import requests
import pandas as pd

searchName = "黑白照片"
savePath = '../结果文件/'+searchName+'/'
saveName = searchName+'.csv'

# 读取数据
data = pd.read_csv(savePath + saveName, usecols=['id', '微博视频url', '微博图片url', 'user_authentication'])

data_dict = data.to_dict('records')

# print(data_dict)
filtered_data = [
    entry for entry in data_dict 
    if (isinstance(entry['微博视频url'], str) and entry['微博视频url'].strip()) 
    or (isinstance(entry['微博图片url'], (list, str)) and entry['微博图片url'])
]

# print(filtered_data)

url_dict = {}  
for entry in filtered_data:
    id = entry['id']
    video_url = entry['微博视频url'].strip() if isinstance(entry['微博视频url'], str) else ''
    image_urls = entry['微博图片url'].split(',') if isinstance(entry['微博图片url'], str) else []
    
    # Ensure the video URL has a schema (http or https)
    if video_url and not video_url.startswith(('http://', 'https://')):
        video_url = 'http://' + video_url
    
    url_dict[id] = {
        'video_url': video_url,
        'image_urls': image_urls
    }

# 显示数据


def download_file(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {url} to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Create directories

videoPath = savePath +'videos'
imagePath = savePath +'images'

os.makedirs(videoPath, exist_ok=True)
os.makedirs(imagePath, exist_ok=True)

for id, urls in url_dict.items():
    video_url = urls['video_url']
    image_urls = urls['image_urls']

    # # Download video
    if video_url:
        video_save_path = f"{videoPath}/{id}.mp4"
        download_file(video_url, video_save_path)

    # Download images
    for idx, image_url in enumerate(image_urls):
        if image_url:
            image_save_path = f"{imagePath}/{id}_{idx}.jpg"
            download_file('https://image.baidu.com/search/down?url='+image_url, image_save_path)

print(url_dict)
