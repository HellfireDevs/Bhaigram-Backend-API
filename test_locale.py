from instagrapi import Client
cl = Client()
cl.locale = "hi_IN"
cl.timezone_offset = 19800
cl.country = "IN"
cl.country_code = 91
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")
res = cl.private_request("clips/discover/", data={"seen_reels": ""})
items = res.get("items_with_ads", [])
for item in items[:3]:
    media = item.get("media", {})
    print(media.get("user", {}).get("username", ""), "-", media.get("caption", {}).get("text", "")[:30])
