from instagrapi import Client
import json
cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")
try:
    res = cl.private_request("clips/discover/", data={"seen_reels": "", "max_id": ""})
    items = res.get("items_with_ads", [])
    print(f"Clips discover items: {len(items)}")
except Exception as e:
    print(f"Clips discover error: {e}")
