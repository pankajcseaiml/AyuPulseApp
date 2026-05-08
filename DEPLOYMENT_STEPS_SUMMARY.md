# AyuPulseApp Deployment: Step-by-Step Guide

This guide provides detailed steps to deploy AyuPulseApp using **Render** (backend), **Vercel** (frontend), and **MongoDB Atlas** (database).

## Prerequisites
1. **GitHub Account** (your code is at: https://github.com/pankajcseaiml/AyuPulseApp)
2. **MongoDB Atlas Account** (free tier): https://www.mongodb.com/cloud/atlas
3. **Render Account** (free tier): https://render.com
4. **Vercel Account** (free tier): https://vercel.com

---

## Step 1: MongoDB Atlas Setup

### 1.1 Create MongoDB Atlas Cluster
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and sign up/login
2. Click "Create" → "Create a Database"
3. Choose **FREE tier (M0)**
4. Select cloud provider (AWS, Google Cloud, or Azure)
5. Choose region closest to your users (e.g., Mumbai for India)
6. Click "Create Cluster" (takes 1-3 minutes)

### 1.2 Create Database User
1. In Atlas dashboard, go to "Database Access" → "Add New Database User"
2. Choose "Password" authentication
3. Enter username: `ayupulse_user`
4. Generate secure password (save it!)
5. Set privileges: "Read and write to any database"
6. Click "Add User"

### 1.3 Configure Network Access
1. Go to "Network Access" → "Add IP Address"
2. Click "Allow Access from Anywhere" (0.0.0.0/0) for development
3. Click "Confirm"

### 1.4 Get Connection String
1. Go to "Database" → click "Connect" on your cluster
2. Choose "Drivers" → "Python"
3. Copy the connection string:
   ```
   mongodb+srv://ayupulse_user:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual password
5. Add database name at the end: `/ayupulse?retryWrites=true&w=majority`
6. **Save this connection string** - you'll need it for Render

---

## Step 2: Deploy Backend to Render

### 2.1 Prepare Backend Code
1. Ensure your `backend/render.yaml` file exists (it does)
2. Verify `backend/requirements.txt` has all dependencies
3. Update `backend/.env.production` with your MongoDB connection string

### 2.2 Deploy via Render Dashboard
1. Go to [render.com](https://render.com) and sign in with GitHub
2. Click "New +" → "Web Service"
3. Select "Build and deploy from a Git repository"
4. Connect GitHub account if not already connected
5. Select repository: `pankajcseaiml/AyuPulseApp`
6. Configure the service:
   - **Name**: `ayupulse-backend`
   - **Environment**: `Python`
   - **Region**: Choose closest (e.g., Oregon, Singapore)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2.3 Add Environment Variables
Click "Advanced" → "Add Environment Variable":
- `MONGODB_URL`: Your MongoDB Atlas connection string from Step 1.4
- `SECRET_KEY`: Generate a strong secret key (Render can generate)
- `BACKEND_CORS_ORIGINS`: `https://ayu-pulse-app.vercel.app,https://ayupulseapp.vercel.app,http://localhost:5174`
- `DEBUG`: `false`
- `PROJECT_NAME`: `AyuPulseApp`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`

### 2.4 Create Web Service
1. Click "Create Web Service"
2. Render will build and deploy (5-10 minutes)
3. Note the URL: `https://ayupulse-backend.onrender.com`

### 2.5 Verify Backend Deployment
1. Visit `https://ayupulse-backend.onrender.com/docs` (Swagger UI)
2. Test `/health` endpoint: `https://ayupulse-backend.onrender.com/health`
3. Should return `{"status":"healthy"}`

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Prepare Frontend Code
1. Update `frontend/.env.example` with your Render backend URL
2. Verify `frontend/vercel.json` configuration exists

### 3.2 Deploy via Vercel Dashboard
1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click "Add New" → "Project"
3. Import your GitHub repository: `pankajcseaiml/AyuPulseApp`
4. Configure project settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)

### 3.3 Add Environment Variables
Click "Environment Variables":
- `VITE_API_URL`: Your Render backend URL (e.g., `https://ayupulse-backend.onrender.com`)
- `VITE_APP_NAME`: `AyuPulse`
- `VITE_APP_VERSION`: `1.0.0`

### 3.4 Deploy
1. Click "Deploy"
2. Vercel will build and deploy (2-3 minutes)
3. Note the URL: `https://ayupulse.vercel.app`

### 3.5 Update Backend CORS
1. Go back to Render dashboard
2. Edit environment variable `BACKEND_CORS_ORIGINS`
3. Add your Vercel frontend URL: `https://ayupulse.vercel.app`
4. Save and redeploy backend

---

## Step 4: Connect Everything

### 4.1 Update Frontend API URL
1. In Vercel dashboard, go to your project
2. Click "Settings" → "Environment Variables"
3. Update `VITE_API_URL` to match your Render backend URL
4. Redeploy frontend

### 4.2 Test Full Application
1. Open frontend: `https://ayupulse.vercel.app`
2. Register a new user
3. Login and test prediction functionality
4. Verify data is saved to MongoDB Atlas

### 4.3 Initialize Database
1. Create a test user via frontend registration
2. Or use the backend API directly:
   ```bash
   curl -X POST "https://ayupulse-backend.onrender.com/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"Test123!","full_name":"Test User"}'
   ```

---

## Step 5: Troubleshooting

### Common Issues

#### 1. Backend Fails to Start on Render
- Check build logs in Render dashboard
- Ensure `requirements.txt` has correct versions
- Verify Python version compatibility (3.9+)

#### 2. MongoDB Connection Failed
- Check `MONGODB_URL` environment variable
- Verify MongoDB Atlas network access allows all IPs (0.0.0.0/0)
- Ensure database user credentials are correct

#### 3. CORS Errors
- Verify `BACKEND_CORS_ORIGINS` includes your frontend URL
- Check for typos in URLs
- Restart backend after updating CORS

#### 4. Frontend Can't Connect to Backend
- Check `VITE_API_URL` in Vercel environment variables
- Test backend API directly: `https://ayupulse-backend.onrender.com/health`
- Verify backend is running (not sleeping - free tier sleeps after inactivity)

---

## Step 6: Maintenance

### Keep Services Alive (Free Tier)
- **Render**: Free tier sleeps after 15 minutes of inactivity
  - Use uptime monitoring service to ping backend every 10 minutes
  - Or upgrade to paid plan for always-on
- **Vercel**: Always active for frontend
- **MongoDB Atlas**: Free tier has 512MB storage limit

### Monitoring
1. **Render**: Check logs in dashboard
2. **Vercel**: Analytics in dashboard
3. **MongoDB Atlas**: Monitor usage in cluster view

### Updates
1. Push changes to GitHub `main` branch
2. Render and Vercel will auto-deploy
3. Test thoroughly after updates

---

## Quick Reference URLs

- **GitHub Repository**: https://github.com/pankajcseaiml/AyuPulseApp
- **Backend (Render)**: `https://ayupulse-backend.onrender.com`
- **Frontend (Vercel)**: `https://ayupulse.vercel.app`
- **Backend API Docs**: `https://ayupulse-backend.onrender.com/docs`
- **Health Check**: `https://ayupulse-backend.onrender.com/health`

---

## Next Steps

1. **Set up custom domains** (optional)
   - Add custom domain in Vercel for frontend
   - Add custom domain in Render for backend
   - Update CORS and environment variables accordingly

2. **Implement CI/CD**
   - Add GitHub Actions for automated testing
   - Set up staging environment

3. **Add monitoring**
   - Set up error tracking (Sentry)
   - Add performance monitoring

4. **Scale up**
   - Upgrade Render to paid plan for always-on backend
   - Upgrade MongoDB Atlas for more storage
   - Add Redis caching for better performance

---

## Support

If you encounter issues:
1. Check the detailed guides:
   - `DEPLOYMENT_GUIDE_COMPLETE.md` - Full comprehensive guide
   - `deploy-render.md` - Render-specific instructions
   - `DEPLOY_VERCEL.md` - Vercel-specific instructions
2. Review error logs in respective dashboards
3. Test locally first to isolate issues

**Your AyuPulseApp is now deployed and ready to use!**