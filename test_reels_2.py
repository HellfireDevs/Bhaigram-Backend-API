from instagrapi import Client

cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")

try:
    print("Fetching hashtag reels...")
    reels = cl.hashtag_medias_reels_v1('trending', amount=3)
    print(f"Got {len(reels)} reels")
    for r in reels:
        print(r.video_url)
except Exception as e:
    print(f"Error: {e}")
