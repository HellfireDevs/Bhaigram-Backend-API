from instagrapi import Client
cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")
res = cl.private_request("discover/topical_explore/")
items = res.get("sectional_items", [])
count = 0
for item in items:
    layout = item.get("layout_content", {})
    medias = layout.get("fill_items", []) + layout.get("medias", [])
    for m in medias:
        media = m.get("media", {})
        if media.get("media_type") == 2: # Video/Reel
            video_versions = media.get("video_versions", [])
            if video_versions:
                print("Found reel video url:", video_versions[0].get("url")[:30])
                count += 1
print("Total reels found:", count)
