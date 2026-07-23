from fastapi import FastAPI, HTTPException, Request
from instagrapi import Client
from pymongo import MongoClient
import uvicorn
import json
import os
from datetime import datetime

app = FastAPI()

# MongoDB Setup (Use Railway variable or local default)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = mongo_client["bhaigram_db"]
comments_col = db["comments"]
saved_col = db["saved_reels"]

def get_client(telegram_id: str = None):
    cl = Client()
    
    # Strictly use Railway .env session ID
    env_session = os.environ.get("IG_SESSION_ID")
    if env_session:
        try:
            cl.login_by_sessionid(env_session)
            return cl
        except Exception as e:
            print(f"Env login failed: {e}")
            raise HTTPException(status_code=401, detail="Invalid Session ID in environment variables")
    else:
        raise HTTPException(status_code=401, detail="IG_SESSION_ID not found in environment variables")

@app.get("/")
def home():
    return {
        "status": "Running 🚀",
        "message": "Welcome to Bhaigram Backend API",
        "endpoints": {
            "health_check": "/health",
            "download_media": "/download/media?url=...",
            "profile_info": "/profile/info?query=username_or_url",
            "profile_stories": "/profile/stories?username=...",
            "profile_highlights": "/profile/highlights?username=...",
            "profile_posts": "/profile/posts?username=...&amount=12",
            "profile_followers": "/profile/followers?username=...&amount=20",
            "profile_following": "/profile/following?username=...&amount=20",
            "search_users": "/search/users?query=...",
            "search_hashtag": "/search/hashtag?name=...&amount=10",
            "user_feed": "/feed/{telegram_id}",
            "user_saved": "/saved/{telegram_id}"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Bhaigram backend is running perfectly!"}

user_pagination = {}

@app.get("/feed/{telegram_id}")
def get_reels_feed(telegram_id: str, limit: int = 5):
    try:
        cl = get_client(telegram_id)
        
        payload = {"seen_reels": ""}
        if telegram_id in user_pagination and user_pagination[telegram_id]:
            payload["max_id"] = user_pagination[telegram_id]
            
        res = cl.private_request("clips/discover/", data=payload)
        items = res.get("items_with_ads", [])
        
        paging_info = res.get("paging_info", {})
        if paging_info and paging_info.get("max_id"):
            user_pagination[telegram_id] = paging_info.get("max_id")
        
        import random
        random.shuffle(items)
        items = items[:limit]
        
        response_data = []
        for item in items:
            media = item.get("media", {})
            if not media:
                continue
                
            pk = media.get("pk", "")
            author = media.get("user", {}).get("username", "")
            caption = media.get("caption", {}).get("text", "") if media.get("caption") else ""
            
            # Real IG Like Count & Comment Count directly in feed to avoid extra API calls
            like_count = media.get("like_count", 0)
            comment_count = media.get("comment_count", 0)
            
            video_versions = media.get("video_versions", [])
            video_url = video_versions[0].get("url") if video_versions else ""
            
            image_versions = media.get("image_versions2", {}).get("candidates", [])
            thumbnail_url = image_versions[0].get("url") if image_versions else ""
            
            if not video_url:
                continue

            response_data.append({
                "id": pk,
                "author": author,
                "caption": caption,
                "like_count": like_count,
                "comment_count": comment_count,
                "video_url": str(video_url),
                "thumbnail_url": str(thumbnail_url)
            })
            
        return {"reels": response_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/like/{media_id}")
async def like_reel(media_id: str, request: Request):
    try:
        data = await request.json()
        telegram_id = data.get("telegram_id")
        cl = get_client(telegram_id)
        cl.media_like(media_id)
        return {"success": True, "message": "Reel liked on Instagram!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/not_interested/{media_id}")
async def not_interested_reel(media_id: str, request: Request):
    try:
        data = await request.json()
        telegram_id = data.get("telegram_id")
        cl = get_client(telegram_id)
        try:
            cl.private_request(f"discover/explore_report/", data={"explore_source_token": "", "media_id": media_id})
        except:
            pass
        return {"success": True, "message": "Instagram will show fewer reels like this."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ================= NEW ENDPOINTS (MongoDB + IG Info) =================

@app.get("/reel/{reel_id}/info")
def get_reel_info(reel_id: str):
    """Fallback endpoint if you need live IG like count anytime"""
    try:
        cl = get_client()
        # media_info is slow, but perfectly gets real-time likes
        info = cl.media_info(reel_id)
        return {
            "reel_id": reel_id,
            "like_count": info.like_count,
            "comment_count": info.comment_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reel/{reel_id}/comment/{telegram_id}")
async def add_comment(reel_id: str, telegram_id: str, request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        
        comment = {
            "reel_id": reel_id,
            "telegram_id": telegram_id,
            "text": text,
            "timestamp": datetime.utcnow().isoformat()
        }
        comments_col.insert_one(comment)
        return {"success": True, "message": "Comment added to MongoDB!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reel/{reel_id}/comments")
def get_comments(reel_id: str):
    try:
        comments = list(comments_col.find({"reel_id": reel_id}, {"_id": 0}))
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/saved/{telegram_id}/{reel_id}")
def save_reel(telegram_id: str, reel_id: str):
    try:
        # Save reference in MongoDB
        saved_col.update_one(
            {"telegram_id": telegram_id, "reel_id": reel_id},
            {"$set": {"timestamp": datetime.utcnow().isoformat()}},
            upsert=True
        )
        return {"success": True, "message": "Reel saved in MongoDB!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/saved/{telegram_id}")
def get_saved_reels(telegram_id: str):
    try:
        reels = list(saved_col.find({"telegram_id": telegram_id}, {"_id": 0}))
        return {"saved_reels": reels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/media")
def download_media(url: str):
    """Fetch direct download links and details for ANY Instagram Reel, Post, or Carousel from a URL"""
    try:
        cl = get_client()
        # media_pk_from_url automatically handles /p/, /reel/, and strips ?igsh= etc.
        media_pk = cl.media_pk_from_url(url)
        media_info = cl.media_info(media_pk)
        
        # Bhaigram Extra Details
        response_data = {
            "media_id": media_info.pk,
            "shortcode": getattr(media_info, 'code', ''),
            "media_type": media_info.media_type, # 1: Photo, 2: Video/Reel, 8: Carousel
            "author": media_info.user.username,
            "taken_at": media_info.taken_at.isoformat() if media_info.taken_at else None,
            "caption": media_info.caption_text,
            "like_count": media_info.like_count,
            "comment_count": media_info.comment_count,
            "play_count": getattr(media_info, 'play_count', 0),
            "video_duration": getattr(media_info, 'video_duration', 0.0),
        }
        
        # Location Info
        if getattr(media_info, 'location', None):
            response_data["location"] = {
                "name": media_info.location.name,
                "city": getattr(media_info.location, 'city', ''),
                "lng": getattr(media_info.location, 'lng', None),
                "lat": getattr(media_info.location, 'lat', None)
            }
            
        # Music Info for Reels
        clips_metadata = getattr(media_info, 'clips_metadata', {})
        if clips_metadata and 'music_info' in clips_metadata and clips_metadata['music_info']:
            music = clips_metadata['music_info'].get('music_asset_info', {})
            response_data["music_info"] = {
                "title": music.get('title', ''),
                "artist": music.get('display_artist', ''),
                "is_original": music.get('is_original_sound', False)
            }
        
        # Download Links
        if media_info.media_type == 2: # Video/Reel
            response_data["video_url"] = str(media_info.video_url)
            response_data["thumbnail_url"] = str(media_info.thumbnail_url)
        elif media_info.media_type == 1: # Single Photo
            response_data["image_url"] = str(media_info.thumbnail_url)
        elif media_info.media_type == 8: # Carousel (Multiple photos/videos)
            resources = []
            for item in media_info.resources:
                if item.media_type == 2:
                    resources.append({"type": "video", "url": str(item.video_url)})
                else:
                    resources.append({"type": "image", "url": str(item.thumbnail_url)})
            response_data["carousel"] = resources
            
        return {"success": True, "data": response_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/info")
def profile_info(query: str):
    """Fetch complete profile info using either a username or an Instagram profile URL"""
    try:
        import re
        cl = get_client()
        
        # Extract username if a full URL is provided
        username = query
        if "instagram.com/" in query:
            match = re.search(r"instagram\.com/([^/?]+)", query)
            if match:
                username = match.group(1)
        
        user_info = cl.user_info_by_username(username)
        
        response_data = {
            "pk": user_info.pk,
            "username": user_info.username,
            "full_name": user_info.full_name,
            "biography": user_info.biography,
            "external_url": getattr(user_info, "external_url", ""),
            "follower_count": user_info.follower_count,
            "following_count": user_info.following_count,
            "media_count": user_info.media_count,
            "is_private": user_info.is_private,
            "is_verified": user_info.is_verified,
            "is_business": getattr(user_info, "is_business", False),
            "business_category": getattr(user_info, "business_category_name", ""),
            "public_email": getattr(user_info, "public_email", ""),
            "contact_phone_number": getattr(user_info, "contact_phone_number", ""),
            "whatsapp_number": getattr(user_info, "whatsapp_number", ""),
            "pronouns": getattr(user_info, "pronouns", []),
            "has_anonymous_profile_picture": getattr(user_info, "has_anonymous_profile_picture", False),
            "account_type": getattr(user_info, "account_type", None),
            "location_data": {
                "city_name": getattr(user_info, "city_name", ""),
                "address_street": getattr(user_info, "address_street", ""),
                "zip": getattr(user_info, "zip", ""),
                "latitude": getattr(user_info, "latitude", None),
                "longitude": getattr(user_info, "longitude", None)
            },
            "profile_pic_url": str(user_info.profile_pic_url),
            "profile_pic_url_hd": str(user_info.profile_pic_url_hd)
        }
        
        return {"success": True, "data": response_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/stories")
def get_user_stories(username: str):
    try:
        user_id = cl.user_id_from_username(username)
        stories = cl.user_stories(user_id)
        data = []
        for s in stories:
            data.append({
                "pk": s.pk,
                "taken_at": s.taken_at.isoformat() if s.taken_at else None,
                "media_type": s.media_type,
                "video_url": str(s.video_url) if s.video_url else None,
                "thumbnail_url": str(s.thumbnail_url) if s.thumbnail_url else None
            })
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/highlights")
def get_user_highlights(username: str):
    try:
        user_id = cl.user_id_from_username(username)
        highlights = cl.user_highlights(user_id)
        data = []
        for h in highlights:
            cover_url = None
            if h.cover_media and getattr(h.cover_media, 'cropped_image_version', None):
                cover_url = str(h.cover_media.cropped_image_version.url)
            data.append({
                "pk": h.pk,
                "title": h.title,
                "cover_url": cover_url
            })
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/posts")
def get_user_posts(username: str, amount: int = 12):
    try:
        user_id = cl.user_id_from_username(username)
        medias = cl.user_medias(user_id, amount=amount)
        data = []
        for m in medias:
            data.append({
                "pk": m.pk,
                "code": m.code,
                "media_type": m.media_type,
                "like_count": m.like_count,
                "comment_count": getattr(m, 'comment_count', 0),
                "play_count": getattr(m, 'play_count', 0),
                "taken_at": m.taken_at.isoformat() if m.taken_at else None,
                "thumbnail_url": str(m.thumbnail_url) if m.thumbnail_url else None
            })
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/followers")
def get_user_followers(username: str, amount: int = 20):
    try:
        user_id = cl.user_id_from_username(username)
        # Using _v1 because the standard dict return structure is simpler to parse usually, 
        # or we just iterate over the values of the dict. instagrapi user_followers returns dict{uid: UserShort}
        followers = cl.user_followers(user_id, amount=amount)
        data = []
        for uid, u in followers.items():
            data.append({
                "pk": u.pk,
                "username": u.username,
                "full_name": u.full_name,
                "profile_pic_url": str(u.profile_pic_url) if u.profile_pic_url else None,
                "is_private": u.is_private
            })
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/following")
def get_user_following(username: str, amount: int = 20):
    try:
        user_id = cl.user_id_from_username(username)
        following = cl.user_following(user_id, amount=amount)
        data = []
        for uid, u in following.items():
            data.append({
                "pk": u.pk,
                "username": u.username,
                "full_name": u.full_name,
                "profile_pic_url": str(u.profile_pic_url) if u.profile_pic_url else None,
                "is_private": u.is_private
            })
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/users")
def search_users(query: str):
    try:
        users = cl.search_users(query)
        data = []
        for u in users:
            data.append({
                "pk": u.pk,
                "username": u.username,
                "full_name": u.full_name,
                "profile_pic_url": str(u.profile_pic_url) if u.profile_pic_url else None,
                "is_private": u.is_private,
                "is_verified": u.is_verified
            })
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/hashtag")
def search_hashtag(name: str, amount: int = 10):
    try:
        medias = cl.hashtag_medias_top(name, amount=amount)
        data = []
        for m in medias:
            data.append({
                "pk": m.pk,
                "code": m.code,
                "media_type": m.media_type,
                "like_count": m.like_count,
                "taken_at": m.taken_at.isoformat() if m.taken_at else None
            })
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
