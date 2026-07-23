from instagrapi import Client

cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")
print("Logged in!")

try:
    print("Fetching explore_reels...")
    reels = cl.explore_reels(amount=2)
    print(f"Got {len(reels)} from explore_reels")
    for r in reels:
        print(r.video_url)
except Exception as e:
    print(f"explore_reels error: {e}")

try:
    print("Fetching fbsearch_reels_v2...")
    # wait, fbsearch is search. Is there a better one?
    reels2 = cl.get_reels_tray_feed()
    print(f"Got {len(reels2)} from get_reels_tray_feed")
except Exception as e:
    print(f"get_reels_tray_feed error: {e}")
