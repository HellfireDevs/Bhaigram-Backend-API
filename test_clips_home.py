from instagrapi import Client

cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")

print("Trying raw private_request('clips/home/') ...")
try:
    res = cl.private_request("clips/home/", data={"seen_reels": ""})
    items = res.get("items", [])
    print(f"Success! Got {len(items)} from raw clips/home.")
    for i in items[:4]:
        media = i.get("media", {})
        video_versions = media.get("video_versions", [])
        if video_versions:
            print(video_versions[0]["url"])
except Exception as e:
    print(f"raw clips/home failed: {e}")
