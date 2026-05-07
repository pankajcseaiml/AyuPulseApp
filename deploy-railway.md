# Deploy AyuPulseApp Backend to Railway

This guide provides step-by-step instructions to deploy the FastAPI backend to Railway using the fixed `railway.json` and `Railway.toml` configurations.

## Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository (already at https://github.com/pankajcseaiml/AyuPulseApp)
2. **Railway Account**: Sign up at [railway.app](https://railway.app) (free tier available)
3. **MongoDB Atlas Account**: For cloud database (free tier available)

## Fixed Configuration

The previous Railway deployment failed with "Railpack could not determine how to build the app" because Railway was analyzing the entire repository instead of just the backend directory. This has been fixed with:

1. **Updated `railway.json`** at repository root with explicit configuration
2. **Added `Railway.toml`** for additional configuration support
3. **Removed duplicate `backend/railway.json`** to avoid confusion

### Current Configuration Files

#### 1. `railway.json` (at repository root)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt",
    "rootDirectory": "./backend",
    "watchPatterns": [
      "backend/**",
      "!frontend/**",
      "!data/**",
      "!scripts/**",
      "!tests/**"
    ]
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 60,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "numReplicas": 1
  },
  "variables": {
    "PYTHON_VERSION": "3.10",
    "NODE_VERSION": "18",
    "ENVIRONMENT": "production",
    "DEBUG": "false",
    "SECRET_KEY": {
      "description": "Secret key for JWT token generation",
      "generator": "secret"
    },
    "MONGODB_URL": {
      "description": "MongoDB connection string",
      "required": true
    },
    "BACKEND_CORS_ORIGINS": "https://ayu-pulse-app.vercel.app,https://ayupulseapp.vercel.app,http://localhost:5173",
    "ALLOWED_HOSTS": "*"
  },
  "plugins": [
    {
      "name": "mongodb",
      "type": "database.mongodb",
      "required": true
    }
  ],
  "service": {
    "name": "ayu-pulse-backend",
    "description": "FastAPI backend for AyuPulseApp healthcare platform",
    "type": "web"
  }
}
```

#### 2. `Railway.toml` (at repository root)
```toml
[build]
builder = "nixpacks"
buildCommand = "pip install -r requirements.txt"
rootDirectory = "./backend"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 60
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10
numReplicas = 1

[variables]
PYTHON_VERSION = "3.10"
NODE_VERSION = "18"
ENVIRONMENT = "production"
DEBUG = "false"
SECRET_KEY = { generator = "secret" }
MONGODB_URL = { required = true }
BACKEND_CORS_ORIGINS = "https://ayu-pulse-app.vercel.app,https://ayupulseapp.vercel.app,http://localhost:5173"
ALLOWED_HOSTS = "*"

[[plugins]]
name = "mongodb"
type = "database.mongodb"
required = true

[service]
name = "ayu-pulse-backend"
description = "FastAPI backend for AyuPulseApp healthcare platform"
type = "web"
```

## Step 1: Prepare Your Backend Code

Ensure your backend code is ready for production:

1. **Verify the configuration files exist**:
   - `railway.json` at repository root (updated)
   - `Railway.toml` at repository root (new)
   - No `railway.json` in `backend/` directory (removed)

2. **Verify requirements.txt exists** in `backend/requirements.txt`

3. **Check environment variables** in `backend/.env.production`:
   - Update with your actual MongoDB Atlas connection string
   - Set a strong SECRET_KEY
   - Add your Vercel frontend domain to BACKEND_CORS_ORIGINS

## Step 2: Deploy to Railway

### Option A: Deploy via Railway Dashboard (Recommended)

1. **Go to [railway.app](https://railway.app)** and sign in with your GitHub account.

2. **Create a New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub account if prompted

3. **Select Your Repository**:
   - Choose "pankajcseaiml/AyuPulseApp"
   - Railway will detect the `railway.json` and `Railway.toml` configurations automatically

4. **Configure Service Settings**:
   - Railway will auto-configure based on the configuration files:
     - **Root Directory**: `backend` (explicitly set in railway.json)
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Verify these settings match

5. **Add Environment Variables**:
   Click "Variables" tab and add the following:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster0.mongodb.net/ayupulse?retryWrites=true&w=majority
   DATABASE_NAME=ayupulse
   SECRET_KEY=your_secure_random_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DEBUG=False
   BACKEND_CORS_ORIGINS=https://ayu-pulse-app.vercel.app,https://ayupulseapp.vercel.app
   MAX_UPLOAD_SIZE=10485760
   ALLOWED_IMAGE_TYPES=["image/jpeg","image/png","image/jpg"]
   PORT=8000
   ```

   **Important**: Replace `MONGODB_URL` with your actual MongoDB Atlas connection string.

6. **Deploy**:
   - Railway will automatically start building and deploying
   - Monitor the deployment logs in real-time
   - Wait for "Deployment Succeeded" message

7. **Get Your Backend URL**:
   - Once deployed, Railway will provide a URL like `https://ayupulse-backend.up.railway.app`
   - Copy this URL for the next step

### Option B: Deploy via Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize Railway Project**:
   ```bash
   cd /path/to/AyuPulseApp
   railway init
   ```
   - Follow prompts to create/link project

4. **Deploy**:
   ```bash
   railway up
   ```
   - Railway will use the `railway.json` and `Railway.toml` configurations automatically

5. **Set Environment Variables**:
   ```bash
   railway variables set MONGODB_URL "your_mongodb_connection_string"
   railway variables set SECRET_KEY "your_secret_key"
   railway variables set BACKEND_CORS_ORIGINS "https://ayu-pulse-app.vercel.app,https://ayupulseapp.vercel.app"
   # Add all other variables from Step 5 above
   ```

6. **Get Deployment URL**:
   ```bash
   railway status
   ```
   - Copy the URL shown in the output

## Step 3: Update Frontend Configuration

After deploying the backend, update your frontend to use the Railway backend URL:

1. **Update Vercel Environment Variables**:
   - Go to your Vercel project dashboard
   - Navigate to Settings > Environment Variables
   - Add/update: `VITE_API_URL=https://your-railway-backend-url.up.railway.app`

2. **Redeploy Frontend** (if needed):
   ```bash
   cd frontend
   npm run build
   vercel --prod
   ```

## Step 4: Test the Deployment

Test your deployed backend:

1. **Health Check**:
   ```
   GET https://your-railway-backend-url.up.railway.app/health
   ```
   Should return: `{"status":"healthy","timestamp":"..."}`

2. **API Documentation**:
   ```
   GET https://your-railway-backend-url.up.railway.app/docs
   ```
   Should show Swagger UI with all API endpoints

3. **Test Authentication**:
   Use the demo accounts:
   - Admin: `admin` / `admin123`
   - Doctor: `doctor` / `doctor123`
   - Patient: `patient` / `patient123`

## Troubleshooting

### Common Issues

1. **"Railpack could not determine how to build the app"**
   - Ensure `railway.json` is at repository root (not in backend/)
   - Check that `rootDirectory` is set to `"./backend"`
   - Remove any duplicate `railway.json` files

2. **Build fails due to missing dependencies**
   - Check `backend/requirements.txt` exists and is valid
   - Railway uses Python 3.10 by default (configured in railway.json)

3. **Application fails to start**
   - Check logs in Railway dashboard
   - Verify `startCommand` is correct: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Ensure `app.main:app` points to the correct FastAPI application

4. **CORS errors from frontend**
   - Verify `BACKEND_CORS_ORIGINS` includes your Vercel frontend URL
   - Check that the frontend `VITE_API_URL` matches the Railway backend URL

5. **Database connection issues**
   - Verify `MONGODB_URL` is correctly set in Railway variables
   - Check MongoDB Atlas network access allows Railway IPs

### Checking Deployment Logs

1. In Railway dashboard, go to your project
2. Click on the deployment
3. View "Logs" tab for real-time logs
4. Check "Build Logs" for build-time errors
5. Check "Runtime Logs" for application errors

## Next Steps

1. **Set up custom domain** (optional):
   - In Railway dashboard, go to Settings > Domains
   - Add your custom domain

2. **Enable auto-deploy**:
   - In Railway dashboard, go to Settings > Git
   - Enable "Auto Deploy" for main branch

3. **Set up monitoring**:
   - Railway provides basic monitoring in the dashboard
   - Consider adding external monitoring services

4. **Backup strategy**:
   - Set up MongoDB Atlas backups
   - Consider Railway's backup plugin for database

## Support

If you encounter issues:
1. Check Railway documentation: https://docs.railway.app
2. Review deployment logs in Railway dashboard
3. Verify all environment variables are set correctly
4. Test locally with the same configuration

## Success Checklist

- [ ] Backend deployed to Railway with successful build
- [ ] Health check endpoint returns `{"status":"healthy"}`
- [ ] API documentation accessible at `/docs`
- [ ] Frontend updated with Railway backend URL
- [ ] Authentication works with demo accounts
- [ ] CORS configured correctly for Vercel frontend
- [ ] MongoDB Atlas connected successfully