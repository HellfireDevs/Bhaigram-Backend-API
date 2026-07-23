import requests
import json
import subprocess
import os

print("Fetching feed from local API...")
res = requests.get("http://localhost:8001/feed/123456?limit=4")
data = res.json()

reels = data.get("reels", [])
print(f"Found {len(reels)} reels.")

for i, reel in enumerate(reels):
    video_url = reel.get("video_url")
    if not video_url:
        continue
        
    filename = f"reel_{i+1}.mp4"
    print(f"Downloading {filename}...")
    
    # Download the video
    with requests.get(video_url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                
    print(f"Uploading {filename} to yukiapi.site...")
    # Upload via curl
    curl_cmd = [
        "curl", "-X", "POST", 
        "-F", f"file=@{filename}", 
        "https://yukiapi.site/upload"
    ]
    result = subprocess.run(curl_cmd, capture_output=True, text=True)
    print(f"Upload Response for {filename}: {result.stdout}\n")
    
    # Cleanup
    os.remove(filename)

print("Done!")
