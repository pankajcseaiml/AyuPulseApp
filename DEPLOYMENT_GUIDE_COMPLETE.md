# Complete Deployment Guide: AyuPulseApp

This comprehensive guide provides step-by-step instructions to deploy AyuPulseApp using:
- **Vercel** for React frontend
- **Render** for FastAPI backend  
- **MongoDB Atlas** for cloud database

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [MongoDB Atlas Setup](#mongodb-atlas-setup)
3. [Backend Deployment to Render](#backend-deployment-to-render)
4. [Frontend Deployment to Vercel](#frontend-deployment-to-vercel)
5. [Connecting Everything](#connecting-everything)
6. [Testing the Deployment](#testing-the-deployment)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance](#maintenance)

## Prerequisites

### Accounts Needed
1. **GitHub Account** (already have: https://github.com/pankajcseaiml/AyuPulseApp)
2. **MongoDB Atlas Account** (free tier): https://www.mongodb.com/cloud/atlas
3. **Render Account** (free tier): https://render.com
4. **Vercel Account** (free tier): https://vercel.com

### Code Preparation
Ensure your code is ready:
- Frontend: React/Vite application in `frontend/` directory
- Backend: FastAPI application in `backend/` directory
- Configuration files are present (see verification below)

## Step 1: MongoDB Atlas Setup

### 1.1 Create MongoDB Atlas Cluster
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up or log in
3. Click "Create" → "Create a Database"
4. Choose FREE tier (M0)
5. Select cloud provider (AWS, Google Cloud, or Azure)
6. Choose region closest to your users
7. Click "Create Cluster" (takes 1-3 minutes)

### 1.2 Create Database User
1. In Atlas dashboard, go to "Database Access" → "Add New Database User"
2. Choose "Password" authentication
3. Enter username (e.g., `ayupulse_user`)
4. Generate secure password or create your own
5. Set privileges: "Read and write to any database"
6. Click "Add User"

### 1.3 Configure Network Access
1. Go to "Network Access" → "Add IP Address"
2. Click "Allow Access from Anywhere" (0.0.0.0/0) for testing
   - For production, add specific IPs: Render IPs + your IP
3. Click "Confirm"

### 1.4 Get Connection String
1. Go to "Database" → click "Connect" on your cluster
2. Choose "Connect your application"
3. Select driver: "Python" and version: "3.6 or later"
4. Copy the connection string:
   ```
   mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<username>` and `<password>` with your database user credentials
6. Save this connection string for later

## Step 2: Backend Deployment to Render

### 2.1 Prepare Backend Code
Verify these files exist in your repository:
- `backend/render.yaml` - Render configuration
- `backend/requirements.txt` - Python dependencies
- `backend/app/main.py` - FastAPI application
- `backend/.env.production` - Production environment template

### 2.2 Deploy to Render

#### Option A: Using Render Dashboard (Recommended)
1. **Go to https://render.com** and sign in with GitHub
2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Select "Build and deploy from a Git repository"
   - Connect GitHub account if not already connected
   - Select repository: `pankajcseaiml/AyuPulseApp`

3. **Configure Service**:
   - **Name**: `ayupulse-backend` (or your preferred name)
   - **Environment**: `Python`
   - **Region**: Choose closest to users (Oregon, Singapore, Frankfurt)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables** (click "Advanced"):
   - `MONGODB_URL`: Your MongoDB Atlas connection string from Step 1.4
   - `SECRET_KEY`: Generate a strong secret key (Render can generate)
   - `BACKEND_CORS_ORIGINS`: `https://ayu-pulse-app.vercel.app,https://ayupulseapp.vercel.app,http://localhost:5174`
   - `DEBUG`: `false`
   - `PROJECT_NAME`: `AyuPulseApp`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
   - `API_V1_STR`: `/api/v1`

5. **Create Disk** (optional, for file uploads):
   - Name: `uploads`
   - Mount Path: `/opt/render/project/src/uploads`
   - Size: 1GB

6. **Click "Create Web Service"**:
   - Render will build and deploy (5-10 minutes)
   - Wait for "Live" status

#### Option B: Using Render Blueprint
1. Ensure `backend/render.yaml` exists
2. Push code to GitHub
3. In Render dashboard, click "New +" → "Blueprint"
4. Connect GitHub repository
5. Render will auto-configure from `render.yaml`
6. Add environment variables as above

### 2.3 Get Backend URL
After deployment:
1. Go to your Render service dashboard
2. Copy the URL (e.g., `https://ayupulse-backend.onrender.com`)
3. Test it: `curl https://ayupulse-backend.onrender.com/health`
   Should return: `{"status":"healthy","version":"1.0.0"}`

## Step 3: Frontend Deployment to Vercel

### 3.1 Prepare Frontend Code
Verify these files exist:
- `frontend/vercel.json` - Vercel configuration
- `frontend/.env.example` - Environment template
- `frontend/vite.config.ts` - Build configuration

### 3.2 Deploy to Vercel

#### Option A: Using Vercel Dashboard
1. **Go to https://vercel.com** and sign in with GitHub
2. **Import Project**:
   - Click "Add New" → "Project"
   - Import Git repository: `pankajcseaiml/AyuPulseApp`
   - Vercel will auto-detect as React app

3. **Configure Project**:
   - **Project Name**: `ayu-pulse-app` (auto-generated)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Framework Preset**: Vite

4. **Add Environment Variables**:
   - `VITE_API_URL`: Your Render backend URL (from Step 2.3)
   - `VITE_APP_NAME`: `AyuPulseApp`
   - `VITE_APP_VERSION`: `1.0.0`
   - `VITE_ENABLE_ANALYTICS`: `false`

5. **Click "Deploy"**:
   - Vercel will build and deploy (2-5 minutes)
   - Wait for deployment to complete

#### Option B: Using Vercel CLI
1. Install Vercel CLI: `npm i -g vercel`
2. Navigate to frontend: `cd frontend`
3. Run: `vercel`
4. Follow prompts to link project
5. Set environment variables: `vercel env add VITE_API_URL`

### 3.3 Get Frontend URL
After deployment:
1. Go to your Vercel project dashboard
2. Copy the URL (e.g., `https://ayu-pulse-app.vercel.app`)
3. Visit the URL to verify frontend loads

## Step 4: Connecting Everything

### 4.1 Update CORS Configuration
1. Go to Render dashboard → your backend service → Environment
2. Update `BACKEND_CORS_ORIGINS` to include your exact Vercel domain:
   ```
   https://ayu-pulse-app.vercel.app,https://ayupulseapp.vercel.app,http://localhost:5174
   ```
3. Add any custom domains you use
4. Restart service if needed

### 4.2 Update Frontend API URL
1. Go to Vercel dashboard → your project → Settings → Environment Variables
2. Ensure `VITE_API_URL` points to your Render backend URL
3. Redeploy frontend if you changed the variable

### 4.3 Test Connection
1. Open browser developer tools
2. Visit your Vercel frontend
3. Check Network tab for API calls
4. Should see successful requests to your Render backend

## Step 5: Testing the Deployment

### 5.1 Test Backend Endpoints
```bash
# Health check
curl https://ayupulse-backend.onrender.com/health

# API info
curl https://ayupulse-backend.onrender.com/info

# Test with authentication (using demo admin)
curl -X POST https://ayupulse-backend.onrender.com/auth/login \
  -d "username=admin@ayupulse.com&password=admin123"
```

### 5.2 Test Frontend Functionality
1. **Visit your Vercel URL**: `https://ayu-pulse-app.vercel.app`
2. **Test authentication** with demo accounts:
   - Admin: `admin@ayupulse.com` / `admin123`
   - Doctor: `doctor@ayupulse.com` / `doctor123`
   - Patient: `patient@ayupulse.com` / `patient123`
3. **Test features**:
   - Login/Logout
   - Dashboard view
   - Create prediction
   - View prediction history
   - Patient management (Doctor/Admin)
   - Admin panel (Admin only)

### 5.3 Verify Three-Role System
1. **Patient Role**:
   - Can view own predictions
   - Cannot access admin panel
   - Cannot view other patients

2. **Doctor Role**:
   - Can view assigned patients
   - Can create/view predictions
   - Cannot access admin settings

3. **Admin Role**:
   - Full access to all features
   - User management
   - System statistics

## Step 6: Troubleshooting

### Common Issues

#### Backend Won't Start (Render)
- **Error**: "Application failed to start"
- **Solution**: Check Render logs for Python errors
- **Check**: `requirements.txt` includes all dependencies
- **Verify**: `uvicorn` is in requirements.txt

#### CORS Errors
- **Error**: "Access to fetch at ... from origin ... has been blocked by CORS policy"
- **Solution**: Update `BACKEND_CORS_ORIGINS` with exact frontend domain
- **Check**: Domain includes protocol (https://) and no trailing slash

#### MongoDB Connection Failed
- **Error**: "Server selection timeout"
- **Solution**: 
  1. Verify connection string is correct
  2. Check MongoDB Atlas IP whitelist includes 0.0.0.0/0
  3. Ensure database user has correct permissions
  4. Check cluster is running (not paused)

#### Frontend Shows "Network Error"
- **Error**: "Network Error" when making API calls
- **Solution**: 
  1. Check `VITE_API_URL` is correct in Vercel
  2. Verify backend is running (test health endpoint)
  3. Check CORS configuration

#### Render Service Sleeps
- **Issue**: Free tier services sleep after 15 minutes inactivity
- **Solution**: 
  1. First request after sleep will be slow (cold start)
  2. Consider upgrading to paid plan for always-on
  3. Use uptime monitoring to ping service regularly

### Logs and Debugging
1. **Render Logs**: Dashboard → Service → Logs
2. **Vercel Logs**: Dashboard → Project → Deployments → Click deployment → "View Logs"
3. **MongoDB Atlas Logs**: Atlas → Cluster → ... → "View Logs"

## Step 7: Maintenance

### Regular Tasks
1. **Monitor costs**: Free tiers have limits
2. **Update dependencies**: Regularly update Python/Node.js packages
3. **Backup database**: MongoDB Atlas offers automated backups
4. **Review logs**: Check for errors or security issues

### Scaling Up
1. **Render**: Upgrade from Free to Starter/Pro plan
2. **Vercel**: Upgrade for more bandwidth/build minutes
3. **MongoDB Atlas**: Upgrade from M0 to M10+ for production

### Security Best Practices
1. **Rotate secrets**: Change SECRET_KEY periodically
2. **Restrict IPs**: In production, limit MongoDB Atlas IP access
3. **Use environment variables**: Never commit secrets to GitHub
4. **Enable 2FA**: On all cloud accounts

## Alternative Deployment Options

### Backend Alternatives to Render
1. **Railway**: Already configured with `railway.json`
2. **Heroku**: Requires `Procfile` and different configuration
3. **AWS/GCP/Azure**: More complex but full control

### Database Alternatives to MongoDB Atlas
1. **Railway MongoDB**: Built-in with Railway deployment
2. **Self-hosted MongoDB**: More control but maintenance required
3. **Other databases**: PostgreSQL, MySQL with schema changes

## Support Resources

- **Render Documentation**: https://render.com/docs
- **Vercel Documentation**: https://vercel.com/docs
- **MongoDB Atlas Documentation**: https://www.mongodb.com/docs/atlas/
- **AyuPulseApp GitHub**: https://github.com/pankajcseaiml/AyuPulseApp/issues
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **React/Vite Documentation**: https://vitejs.dev/guide/

## Quick Reference

### URLs After Deployment
- **Frontend**: `https://ayu-pulse-app.vercel.app`
- **Backend**: `https://ayupulse-backend.onrender.com`
- **API Documentation**: `https://ayupulse-backend.onrender.com/docs`

### Demo Accounts
- **Admin**: `admin@ayupulse.com` / `admin123`
- **Doctor**: `doctor@ayupulse.com` / `doctor123`
- **Patient**: `patient@ayupulse.com` / `patient123`

### Environment Variables Checklist
**Backend (Render)**:
- `MONGODB_URL`: ✅
- `SECRET_KEY`: ✅
- `BACKEND_CORS_ORIGINS`: ✅
- `DEBUG`: `false`

**Frontend (Vercel)**:
- `VITE_API_URL`: ✅
- `VITE_APP_NAME`: `AyuPulseApp`

## Final Verification
Run this command to verify everything is working:
```bash
# Test backend
curl https://ayupulse-backend.onrender.com/health

# Test frontend connection
curl -I https://ayu-pulse-app.vercel.app
```

If both return successfully, your AyuPulseApp is fully deployed and ready to use!