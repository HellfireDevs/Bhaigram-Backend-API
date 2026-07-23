from instagrapi import Client

cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")

try:
    print("Trying friends_reels...")
    reels = cl.friends_reels(amount=2)
    print(f"Got {len(reels)} friends_reels")
    if reels:
        print(type(reels[0]))
except Exception as e:
    print(f"friends_reels error: {e}")

try:
    print("Trying clips/discover...")
    res = cl.private_request("clips/discover/", data={"seen_reels": ""})
    items = res.get("items_with_ads", [])
    print(f"Got {len(items)} from discover")
except Exception as e:
    print(f"discover error: {e}")
