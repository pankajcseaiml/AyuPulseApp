# 🚀 Comprehensive Guide: Deploying AyuPulseApp Backend on Render

This guide provides step-by-step instructions to deploy your FastAPI backend (`backend/` folder) to [Render](https://render.com) from scratch with **maximum security best practices**.

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
6. Your database connection string for `AyuPulseApp` is ready:
   ```text
   mongodb+srv://ayu-user-app-v2:pankaj092005@cluster0.kd08zo1.mongodb.net/ayupulse?retryWrites=true&w=majority
   ```
   > 🔒 **Security Notice:** This connection string will be saved **ONLY in Render's encrypted environment variables**, NEVER committed to public GitHub code.

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
git push origin master
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
| **Branch** | `master` | Production branch |
| **Root Directory** | `backend` | **CRITICAL!** Tells Render your backend is inside `backend/` folder |
| **Runtime** | `Python 3` | Environment runtime |
| **Build Command** | `pip install -r requirements.txt` | Installs FastAPI, PyTorch, etc. |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` | Starts FastAPI server |
| **Instance Type** | `Free` | Select Free tier ($0/month) |

---

## ⚙️ Step 4: Add Environment Variables (Secure Setup)

Scroll down to the **Environment Variables** section on the same creation page (or click **Advanced** -> **Add Environment Variable**).

Copy and paste these exact **12 Key-Value pairs** into Render:

| Key | Value | Security Function |
| :--- | :--- | :--- |
| `MONGODB_URL` | `mongodb+srv://ayu-user-app-v2:pankaj092005@cluster0.kd08zo1.mongodb.net/ayupulse?retryWrites=true&w=majority` | Encrypted connection string to MongoDB Atlas |
| `SECRET_KEY` | `800ac9feb47b8fe852fce5af4cf3935c8d059bc24156be31659540ee7a72179e` | Cryptographic key used to sign JWT authentication tokens |
| `DEBUG` | `false` | Disables debug mode so full error stack traces are hidden |
| `BACKEND_CORS_ORIGINS` | `*` | Temporary origin policy for testing (will restrict to frontend URL after frontend deploy) |
| `PROJECT_NAME` | `AyuPulseApp` | Project identifier |
| `VERSION` | `1.0.0` | API version |
| `API_V1_STR` | `/api/v1` | API route prefix |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | JWT token expiration time |
| `ALGORITHM` | `HS256` | JWT encryption algorithm |
| `UPLOAD_DIR` | `./uploads` | Directory for uploaded patient files |
| `MAX_UPLOAD_SIZE` | `10485760` | Max file upload limit (10MB) |
| `LOG_LEVEL` | `INFO` | Application log level |

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

## 🔒 Security & Data Protection Guarantee

Here is how your database and application data are protected against exposure and security breaches:

1. **Zero Secret Leaks to GitHub (`.gitignore`)**:
   - `backend/.env` containing your database connection credentials is git-ignored and **NEVER pushed to GitHub**.
   - Render environment variables are encrypted at rest on Render's server infrastructure and only accessible by your running backend process.

2. **TLS / SSL Encryption in Transit**:
   - MongoDB connection uses `mongodb+srv://` which enforces mandatory SSL/TLS encryption for all data traveling between Render and MongoDB Atlas.
   - Render automatically provisions an **HTTPS** SSL certificate for your backend domain, ensuring all client request payloads (passwords, health data) are encrypted.

3. **Secure Authentication & Passwords**:
   - All user passwords stored in MongoDB Atlas are hashed using **bcrypt** salt encryption.
   - User authentication sessions are secured using 256-bit SHA-256 JWT signatures.

4. **Production Information Disclosure Prevention**:
   - `DEBUG=false` hides internal Python tracebacks and database details if an unhandled exception occurs.
   - `SecurityHeadersMiddleware` sets HTTP security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection).

5. **Post-Frontend CORS Restriction**:
   - After we deploy your frontend to Vercel, we will update `BACKEND_CORS_ORIGINS` from `*` to your exact Vercel URL (e.g. `https://ayupulse.vercel.app`), preventing any unauthorized external websites from accessing your backend APIs.

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
1. Copy your Render Backend URL (e.g., `https://ayupulse-backend.onrender.com`).
2. Share the URL with me so we can configure and deploy your Vercel frontend!
