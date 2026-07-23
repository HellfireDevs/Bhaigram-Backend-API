from instagrapi import Client

cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")

try:
    res = cl.private_request("clips/discover/", data={"seen_reels": ""})
    items_ads = res.get("items_with_ads", [])
    print(f"Items with ads length: {len(items_ads)}")
    for i in items_ads[:2]:
        media = i.get("media", {})
        video_versions = media.get("video_versions", [])
        if video_versions:
            print(video_versions[0].get("url"))
except Exception as e:
    print(e)
