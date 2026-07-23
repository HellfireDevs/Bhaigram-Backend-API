from instagrapi import Client

cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")

endpoints = [
    "clips/discover/",
    "discover/reels/",
    "feed/reels_tray/",
    "clips/timeline/"
]

for ep in endpoints:
    print(f"Trying raw private_request('{ep}') ...")
    try:
        res = cl.private_request(ep, data={"seen_reels": ""})
        items = res.get("items", [])
        if items:
            print(f"Success! Got {len(items)} items.")
            break
        elif "tray" in res:
            print(f"Success! Got {len(res['tray'])} tray items.")
    except Exception as e:
        print(f"{ep} failed: {e}")
