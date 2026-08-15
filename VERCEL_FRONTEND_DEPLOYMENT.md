# ⚡ Comprehensive Guide: Deploying AyuPulseApp Frontend on Vercel

This guide walks you through deploying your React + Vite frontend (`frontend/` folder) to [Vercel](https://vercel.com) and linking it to your live Render backend (`https://ayupulse-backend.onrender.com`).

---

## 📋 Pre-requisites Checklist

Before starting, ensure:
1. Your backend is live and healthy at `https://ayupulse-backend.onrender.com`.
2. Your GitHub repository (`AyuPulseApp`) is up to date with the latest commits.
3. You have a free [Vercel Account](https://vercel.com) connected to your GitHub account.

---

## 🐙 Step 1: Commit & Push Latest Code to GitHub

Make sure all latest frontend configurations (including `vercel.json` for SPA routing) are pushed to GitHub:

```powershell
# 1. Check status
git status

# 2. Add all changes
git add .

# 3. Commit
git commit -m "Configure frontend for Vercel deployment with live Render backend"

# 4. Push to GitHub master branch
git push origin master
```

---

## 🌐 Step 2: Create a New Project on Vercel

1. Log in to your [Vercel Dashboard](https://vercel.com/dashboard).
2. Click the **Add New...** button (top right) ➔ Select **Project**.
3. Under **Import Git Repository**, find your repository `AyuPulseApp` (or `pankajcseaiml/AyuPulseApp`).
4. Click the **Import** button next to it.

---

## ⚙️ Step 3: Configure Vercel Project Settings

On the **Configure Project** screen, fill in and verify each field:

| Field Name | Setting / Value | Notes |
| :--- | :--- | :--- |
| **Project Name** | `ayupulse-app` (or any name you choose) | Public project name |
| **Framework Preset** | `Vite` | Vercel automatically detects Vite |
| **Root Directory** | `frontend` | **CRITICAL!** Click **Edit** next to Root Directory, select `frontend`, and click **Continue** |
| **Build Command** | `npm run build` | Default Vite build command |
| **Output Directory** | `dist` | Default Vite output directory |
| **Install Command** | `npm install` | Default package installation |

---

## 🔑 Step 4: Add Environment Variable

Expand the **Environment Variables** section on the same configuration page.

Add the following Key-Value pair:

| Key | Value | Purpose |
| :--- | :--- | :--- |
| `VITE_API_URL` | `https://ayupulse-backend.onrender.com` | Connects your frontend UI to your live Render FastAPI backend |

> 💡 **Tip:** Make sure there is **no trailing slash** at the end of the URL (use `https://ayupulse-backend.onrender.com`, not `...onrender.com/`).

---

## 🚀 Step 5: Deploy the Frontend

1. Click the blue **Deploy** button at the bottom.
2. Vercel will clone the repo, run `npm install`, build your TypeScript & React code, and deploy to their global edge CDN.
3. Once the build finishes (takes ~45 seconds), you will see confetti and the message **"Congratulations! You just deployed a new Project to Vercel."**
4. Click **Continue to Dashboard** or click your deployment screenshot preview to open your live web app!

---

## 🧪 Step 6: Verify Full-Stack Functionality

Open your new live Vercel URL (e.g. `https://ayupulse-app.vercel.app`):

1. **Authentication Flow**:
   - Click **Sign In** / **Register**.
   - Create a new test user account.
   - Verify that registration and login succeed and store the JWT authentication token.
2. **Dashboard & Medical Features**:
   - Open Dashboard (`/dashboard`).
   - Navigate between tabs (Patients, Risk Assessment, Predictions).
   - Refresh the page on any subroute (e.g., `/dashboard` or `/profile`) — confirm it loads smoothly without a 404 error (handled by `frontend/vercel.json`).
3. **Run AI Risk Assessment**:
   - Submit clinical patient values or test an X-ray / ECG prediction.
   - Verify that the frontend receives results and visualizations from your Render backend.

---

## 🔒 Step 7: (Optional Security Polish) Lock Down Backend CORS

Now that your frontend has its official Vercel domain (e.g. `https://ayupulse-app.vercel.app`):

1. Open your [Render Dashboard](https://dashboard.render.com/) ➔ `ayupulse-backend`.
2. Go to **Environment** tab.
3. Update `BACKEND_CORS_ORIGINS` to your exact Vercel domains:
   ```text
   https://ayupulse-app.vercel.app,http://localhost:5173
   ```
4. Click **Save Changes**. This prevents unauthorized websites from calling your backend API!

---

## 🛠️ Troubleshooting Guide

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| **404 Not Found on Page Refresh** | Missing SPA rewrite rules | Ensure `frontend/vercel.json` contains the rewrite rule for `index.html` (already configured in our repo). |
| **API Network Errors (Failed to Fetch)** | Incorrect API URL or Render Sleeping | 1. Ensure `VITE_API_URL` is exactly `https://ayupulse-backend.onrender.com` in Vercel Environment Variables.<br>2. Remember Render free tier sleeps after 15 mins. If asleep, the first request takes ~30-50s to wake up. |
| **Build Failed on Vercel** | Incorrect Root Directory | Ensure **Root Directory** in Vercel project settings is set to `frontend`. |
