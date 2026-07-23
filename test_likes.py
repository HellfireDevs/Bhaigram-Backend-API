from instagrapi import Client
cl = Client()
cl.login_by_sessionid("41766182615%3AVy2dIkT6PjQ81R%3A7%3AAYgNTWwSW7KgI1sJJP5KX0nX43dS4wEsM_R-VRv9gg")
res = cl.private_request("clips/discover/", data={"seen_reels": ""})
for item in res.get("items_with_ads", [])[:1]:
    media = item.get("media", {})
    print("Like count:", media.get("like_count"))
    print("Comment count:", media.get("comment_count"))
