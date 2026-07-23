from instagrapi import Client
import requests
import subprocess
import os
import random

cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")

print("Fetching 3 entirely new unique reels from #funnycats...")
reels = cl.hashtag_medias_reels_v1('funnycats', amount=10)
random.shuffle(reels)  # Shuffle to guarantee uniqueness

count = 0
for i, reel in enumerate(reels):
    if count >= 3:
        break
        
    video_url = reel.video_url
    if not video_url and reel.resources:
        video_url = reel.resources[0].video_url
        
    if not video_url:
        continue
        
    count += 1
    filename = f"unique_reel_{count}.mp4"
    print(f"Downloading {filename}...")
    
    with requests.get(video_url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                
    print(f"Uploading {filename} to yukiapi.site...")
    curl_cmd = [
        "curl", "-X", "POST", 
        "-F", f"file=@{filename}", 
        "https://yukiapi.site/upload"
    ]
    result = subprocess.run(curl_cmd, capture_output=True, text=True)
    print(f"Response: {result.stdout}")
    os.remove(filename)

print("Done!")
