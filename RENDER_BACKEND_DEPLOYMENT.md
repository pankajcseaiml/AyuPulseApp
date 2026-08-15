# 🚀 Comprehensive Guide: Deploying AyuPulseApp Backend on Render

This guide provides step-by-step instructions to deploy your FastAPI backend (`backend/` folder) to [Render](https://render.com) from scratch.

---

## 📋 Pre-requisites Checklist

Before starting, ensure you have:
1. A **GitHub Repository** containing your `AyuPulseApp` code.
2. A **MongoDB Atlas Account** with a running database cluster.
3. A free **Render Account** ([https://render.com](https://render.com)).

---

## 🔑 Step 1: Prepare MongoDB Atlas (Database)

Render free tier instances use dynamic IP addresses. You must whitelist incoming connections from any IP.

1. Log in to [MongoDB Atlas](https://cloud.mongodb.com).
2. In the left navigation menu, click **Network Access** under Security.
3. Click the **+ Add IP Address** button.
4. Click **Allow Access from Anywhere** (this populates `0.0.0.0/0`).
5. Click **Confirm**.
6. In the left menu, click **Database** under Deployment.
7. Click **Connect** next to your cluster.
8. Choose **Drivers** (Node.js/Python).
9. Copy your connection string. It looks like this:
   ```text
   mongodb+srv://<username>:<password>@cluster0.xxxx.mongodb.net/ayupulse?retryWrites=true&w=majority
   ```
   > 💡 **Important:** Replace `<username>` and `<password>` with your actual MongoDB database user credentials.

---

## 🐙 Step 2: Push Latest Changes to GitHub

Open PowerShell or Terminal in your project root (`AyuPulseApp`) and push your repository to GitHub:

```powershell
# 1. Check git status
git status

# 2. Add all changes
git add .

# 3. Commit changes
git commit -m "Prepare backend for Render deployment"

# 4. Push to GitHub main branch
git push origin main
```

---

## 🌐 Step 3: Create Web Service on Render

1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click the **New +** button in the top right corner and select **Web Service**.
3. Choose **Build and deploy from a Git repository** and click **Next**.
4. If you haven't connected GitHub yet, click **+ Connect account** and authorize Render.
5. Find your repository `AyuPulseApp` and click **Connect**.

### Configure Web Service Settings Exactly as Below:

| Setting Field | Value to Enter | Notes |
| :--- | :--- | :--- |
| **Name** | `ayupulse-backend` | Name of your service on Render |
| **Region** | `Singapore` (or nearest to you) | Select any region |
| **Branch** | `main` | Production branch |
| **Root Directory** | `backend` | **CRITICAL!** Tells Render your backend is inside `backend/` folder |
| **Runtime** | `Python 3` | Environment runtime |
| **Build Command** | `pip install -r requirements.txt` | Installs FastAPI, PyTorch, etc. |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` | Starts FastAPI server |
| **Instance Type** | `Free` | Select Free tier ($0/month) |

---

## ⚙️ Step 4: Add Environment Variables

Scroll down to the **Environment Variables** section on the same creation page (or click **Advanced** -> **Add Environment Variable**).

Add the following **12 Key-Value pairs**:

| Key | Value |
| :--- | :--- |
| `MONGODB_URL` | `mongodb+srv://<user>:<password>@cluster0.xxx.mongodb.net/ayupulse?retryWrites=true&w=majority` *(Your Atlas Connection String)* |
| `SECRET_KEY` | `ayupulse_super_secret_jwt_key_2026_production_secure_token_123` |
| `DEBUG` | `false` |
| `BACKEND_CORS_ORIGINS` | `*` |
| `PROJECT_NAME` | `AyuPulseApp` |
| `VERSION` | `1.0.0` |
| `API_V1_STR` | `/api/v1` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |
| `ALGORITHM` | `HS256` |
| `UPLOAD_DIR` | `./uploads` |
| `MAX_UPLOAD_SIZE` | `10485760` |
| `LOG_LEVEL` | `INFO` |

> ⚠️ **Note:** `BACKEND_CORS_ORIGINS` is set to `*` initially so that testing is easy. Once your frontend is deployed on Vercel, you can update this to your specific Vercel URL.

---

## 🚀 Step 5: Deploy the Backend

1. Click the **Create Web Service** button at the bottom of the page.
2. Render will automatically clone your code, install dependencies, and start the app.
3. Watch the live **Logs** tab in Render:
   - You will see lines like `pip install ...`
   - Once build succeeds, you will see `Starting service with uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Look for: `Application startup complete.`

---

## 🧪 Step 6: Verify Backend Deployment

Once deployment reaches status **Live**, Render gives you a public URL at the top left of the dashboard (e.g., `https://ayupulse-backend.onrender.com`).

Test your backend using a browser or PowerShell:

### 1. Root Endpoint Test
Open in browser:
```text
https://ayupulse-backend.onrender.com/
```
Expected output:
```json
{
  "message": "Welcome to AyuPulseApp Backend API"
}
```

### 2. Health & Database Check
Open in browser:
```text
https://ayupulse-backend.onrender.com/health
```
Expected output:
```json
{
  "status": "healthy",
  "service": "AyuPulseApp Backend",
  "version": "1.0.0",
  "database": "connected"
}
```
> ✅ **Check:** Make sure `"database"` says `"connected"`. If it says `error`, check your `MONGODB_URL` environment variable and Mongo Atlas IP Whitelist.

### 3. Interactive API Documentation (Swagger UI)
Open in browser:
```text
https://ayupulse-backend.onrender.com/docs
```
You should see the full interactive API documentation page where you can test auth, health, prediction, and patient endpoints directly.

---

## 🛠️ Troubleshooting Guide

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| **Build Error: Out of Memory** | PyTorch installation exceeded free 512MB RAM | Render free tier limits build memory. Wait 2 minutes and click **Manual Deploy** -> **Clear build cache & deploy**. |
| **Database: error in /health** | Incorrect Mongo URL or IP Blocked | 1. Ensure `0.0.0.0/0` is whitelisted in MongoDB Atlas Network Access.<br>2. Check `MONGODB_URL` in Render Environment Variables for missing characters or invalid password. |
| **First request is slow (30s+)** | Render Free Tier Sleep Mode | Free instances go to sleep after 15 mins of inactivity. The first request wakes up the service (takes 30–50s). Subsequent requests are instant. |
| **404 Not Found on Root** | Missing Root Directory | Ensure **Root Directory** in Render settings is set to `backend`. |

---

## 🎯 Next Steps

Once your backend is successfully deployed on Render and `/health` returns `"database": "connected"`:
1. Save your Render Backend URL (e.g., `https://ayupulse-backend.onrender.com`).
2. You are now ready to proceed with frontend deployment!
