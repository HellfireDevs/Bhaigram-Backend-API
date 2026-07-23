from instagrapi import Client

cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")

def check_reels(method_name, method, **kwargs):
    print(f"\n--- Testing {method_name} ---")
    try:
        reels = method(**kwargs)
        if hasattr(reels, "get"):  # If it's a dict instead of list
            pass
        print(f"Success! Got {len(reels)} items")
        for i, r in enumerate(reels[:2]):
            try:
                # Check aspect ratio / resolution if possible, or just print url
                print(f"[{i}] {r.video_url}")
            except:
                pass
    except Exception as e:
        print(f"Failed: {e}")

check_reels("explore_reels", cl.explore_reels, amount=2)
# check_reels("reels_timeline_media", cl.reels_timeline_media) # takes dict
check_reels("friends_reels", cl.friends_reels, amount=2)
# user_clips of a viral account, e.g. 9gag (id: 259220806)
check_reels("user_clips 9gag", cl.user_clips, user_id=259220806, amount=2)

