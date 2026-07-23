<p align="center">
  <img src="https://img.icons8.com/fluent/150/000000/instagram-new.png" alt="Bhaigram Logo" width="120" />
</p>

<h1 align="center">✨ Bhaigram Backend API ✨</h1>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb" alt="MongoDB" />
  <img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel" alt="Vercel" />
</p>

<p align="center">
  <b>A highly optimized, custom backend server for Bhaigram providing an exact replica of Instagram's Reels feed, direct media downloads, and profile lookups using <code>instagrapi</code>.</b>
</p>

---

## 🌟 Key Features

- 🎥 **Algorithm-driven Reels Feed:** Fetch the same explore feed as the official Instagram app.
- 📥 **Media Downloader:** Get direct MP4/JPEG download links for any Reel, Post, or Carousel natively!
- 👤 **Profile Info Lookup:** Retrieve complete account details (Verification, Follower count, HD DPs) using a Username or URL.
- ❤️ **Interactions:** Like reels and use the "Not Interested" capability seamlessly.
- ⚡ **Extremely Fast:** Powered by `FastAPI` and async capabilities.
- ☁️ **Cloud Ready:** One-click deployment configured for Vercel, Heroku, Railway, etc.

---

## 🚀 Quick Start & Deployment

This project is fully configured for easy cloud deployments! 

### 🟢 Deploy on Vercel
Simply import this repository into your Vercel Dashboard. The `vercel.json` is already configured for serverless Python functions!

### 🟣 Deploy on Heroku / Railway
Click the deploy button or push to Heroku. The `app.json` and `Dockerfile` are fully set up.

---

## 🛠️ Environment Variables

Ensure you configure the following variables in your cloud provider or local `.env`:

| Variable | Description | Required |
|----------|-------------|----------|
| `IG_SESSION_ID` | Your Instagram Session ID from cookies. Mandatory to fetch IG data. | ✅ Yes |
| `MONGO_URI` | MongoDB Connection URL for saving offline comments and saved reels. | ✅ Yes |

---

## 🌐 API Endpoints

### 📲 Core Feed & Actions
- `GET /health` : Health check endpoint.
- `GET /feed/{telegram_id}` : Get randomized, fresh Reels feed (includes likes, comments, and links).
- `POST /like/{media_id}` : Like a specific reel.
- `POST /not_interested/{media_id}` : Report a reel to fix your algorithm.

### 📥 Downloader & Scraper
- `GET /download/media?url={URL}` : Paste **ANY** Instagram link (Reel, Post, Carousel) to get direct HD download links and stats.
- `GET /profile/info?query={USERNAME_OR_URL}` : Get deep profile statistics and High-Res profile pictures.

### 💾 Database Endpoints
- `POST /reel/{reel_id}/comment/{telegram_id}` : Add an offline comment.
- `GET /reel/{reel_id}/comments` : Retrieve all offline comments for a reel.
- `POST /saved/{telegram_id}/{reel_id}` : Save a reel.
- `GET /saved/{telegram_id}` : Get all saved reels.

---

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to get started, run the server locally, and submit Pull Requests.

---

## 📜 License

This project is licensed under the terms of the MIT License. See the [LICENSE](./LICENSE) file for more details.

<p align="center">
  <i>Developed with ❤️ for Bhaigram</i>
</p>
