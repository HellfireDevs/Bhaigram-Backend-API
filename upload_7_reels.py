from instagrapi import Client
import requests
import subprocess
import os

cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")

print("Fetching 7 genuine reels via clips/discover...")
res = cl.private_request("clips/discover/", data={"seen_reels": ""})
items = res.get("items_with_ads", [])

count = 0
for item in items:
    if count >= 7:
        break
        
    media = item.get("media", {})
    if not media:
        continue
        
    video_versions = media.get("video_versions", [])
    if not video_versions:
        continue
        
    video_url = video_versions[0].get("url")
    if not video_url:
        continue
        
    count += 1
    filename = f"reel_batch_{count}.mp4"
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
