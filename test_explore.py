from instagrapi import Client
cl = Client()
cl.login_by_sessionid("23968603971%3AGwOefxN51uIM7L%3A22%3AAYgBLlXNx8S0RFQZkJbFxi-eoWpuvOiD3YokYWU32w")
try:
    res = cl.private_request("discover/topical_explore/")
    items = res.get("sectional_items", [])
    print(f"Topical explore items: {len(items)}")
except Exception as e:
    print(f"Topical explore error: {e}")
