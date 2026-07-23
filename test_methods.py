from instagrapi import Client

cl = Client()
methods = dir(cl)

print("Like methods:", [m for m in methods if 'like' in m])
print("Interest/Hide methods:", [m for m in methods if 'interest' in m or 'hide' in m or 'seen' in m])
