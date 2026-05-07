# Deploy AyuPulseApp Backend to Render

This guide provides step-by-step instructions to deploy the FastAPI backend to Render using the provided `render.yaml` configuration.

## Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository (already at https://github.com/pankajcseaiml/AyuPulseApp)
2. **Render Account**: Sign up at [render.com](https://render.com) (free tier available)
3. **MongoDB Atlas Account**: For cloud database (free tier available)

## Step 1: Prepare Your Backend Code

Ensure your backend code is ready for production:

1. **Check the render.yaml configuration** in `backend/render.yaml`:
   ```yaml
   # Render Blueprint for AyuPulseApp Backend
   services:
     - type: web
       name: ayupulse-backend
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
       healthCheckPath: /health
       envVars:
         - key: MONGODB_URL
           sync: false
         - key: SECRET_KEY
           generateValue: true
         - key: BACKEND_CORS_ORIGINS
           value: "https://ayu-pulse-app.vercel.app,https://ayupulseapp.vercel.app,http://localhost:5174"
   ```

2. **Verify requirements.txt exists** in `backend/requirements.txt`

3. **Check environment variables** in `backend/.env.production`:
   - Update with your actual MongoDB Atlas connection string
   - Set a strong SECRET_KEY
   - Add your Vercel frontend domain to BACKEND_CORS_ORIGINS

## Step 2: Deploy to Render

### Option A: Deploy via Render Dashboard (Recommended)

1. **Go to [render.com](https://render.com)** and sign in with your GitHub account.

2. **Create a New Web Service**:
   - Click "New +" → "Web Service"
   - Select "Build and deploy from a Git repository"
   - Connect your GitHub account if not already connected
   - Select the repository: `pankajcseaiml/AyuPulseApp`

3. **Configure the Service**:
   - **Name**: `ayupulse-backend` (or your preferred name)
   - **Environment**: `Python`
   - **Region**: Choose closest to your users (e.g., Oregon, Singapore)
   - **Branch**: `main` (or your deployment branch)
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable"
   Add the following variables:
   - `MONGODB_URL`: Your MongoDB Atlas connection string
   - `SECRET_KEY`: A strong secret key (Render can generate one)
   - `BACKEND_CORS_ORIGINS`: `https://ayu-pulse-app.vercel.app,https://ayupulseapp.vercel.app,http://localhost:5174`
   - `DEBUG`: `false`
   - `PROJECT_NAME`: `AyuPulseApp`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`

5. **Create Web Service**:
   - Click "Create Web Service"
   - Render will build and deploy your application
   - Wait for deployment to complete (5-10 minutes)

### Option B: Deploy via Render Blueprint (Advanced)

If you have the Render CLI installed:

1. **Install Render CLI**:
   ```bash
   npm install -g @renderinc/cli
   ```

2. **Login to Render**:
   ```bash
   render login
   ```

3. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

4. **Deploy using blueprint**:
   ```bash
   render blueprint launch
   ```

5. **Set environment variables**:
   ```bash
   render env set MONGODB_URL "your_mongodb_connection_string"
   render env set SECRET_KEY "your_secret_key"
   ```

## Step 3: After Render Deployment

1. **Get your Render backend URL**:
   - After deployment completes, you'll get a URL like: `https://ayupulse-backend.onrender.com`
   - Copy this URL

2. **Update Vercel environment variable**:
   - Go to your Vercel project dashboard
   - Go to Settings → Environment Variables
   - Add/Update `VITE_API_URL` with your Render backend URL
   - Example: `VITE_API_URL=https://ayupulse-backend.onrender.com`

3. **Update CORS configuration**:
   - If your Vercel domain changes, update the `BACKEND_CORS_ORIGINS` environment variable in Render
   - Add your exact Vercel domain to the list

4. **Test your deployment**:
   ```bash
   curl https://ayupulse-backend.onrender.com/health
   ```
   Should return: `{"status":"healthy","version":"1.0.0"}`

## Step 4: Test Complete Application

1. **Visit your Vercel frontend**: `https://ayu-pulse-app.vercel.app`
2. **Test authentication** using demo accounts:
   - Admin: `admin@ayupulse.com` / `admin123`
   - Doctor: `doctor@ayupulse.com` / `doctor123`
   - Patient: `patient@ayupulse.com` / `patient123`
3. **Test prediction creation**
4. **Test patient management** (Doctor/Admin roles)
5. **Test admin panel** (Admin role only)

## Troubleshooting

### Common Issues

1. **Build fails with Python dependencies**:
   - Check `backend/requirements.txt` exists and has correct packages
   - Render uses Python 3.9+ by default

2. **Application fails to start**:
   - Check logs in Render dashboard
   - Verify `uvicorn` is in requirements.txt
   - Ensure `app.main:app` points to correct FastAPI instance

3. **CORS errors**:
   - Verify `BACKEND_CORS_ORIGINS` includes your exact Vercel domain
   - Restart service after updating environment variables

4. **MongoDB connection fails**:
   - Verify MongoDB Atlas connection string is correct
   - Ensure IP whitelist includes Render's IP ranges (0.0.0.0/0 for testing)
   - Check MongoDB Atlas cluster is running

### Render Free Tier Limitations

- **Sleeps after inactivity**: Free services sleep after 15 minutes of inactivity
- **Cold starts**: First request after sleep may be slow (30+ seconds)
- **Bandwidth limits**: 100GB/month on free tier
- **Consider upgrading** to paid plan for production use

## Monitoring and Maintenance

1. **View logs**: Render dashboard → Your service → Logs
2. **Monitor health**: Render dashboard → Your service → Health
3. **Update deployment**: Push changes to GitHub, Render auto-deploys
4. **Scale up**: Upgrade plan for higher traffic

## Alternative: Railway vs Render

| Feature | Railway | Render |
|---------|---------|--------|
| Free Tier | Yes | Yes |
| Auto-deploy from GitHub | Yes | Yes |
| Sleep after inactivity | No (always on) | Yes (15 min) |
| Custom domains | Yes | Yes |
| Database integration | Built-in MongoDB plugin | External (MongoDB Atlas) |
| File storage | Ephemeral | Persistent disk available |
| Ease of use | Very easy | Easy |

**Recommendation**: Render is a good alternative if Railway has issues. Both work well for FastAPI applications.

## Next Steps

1. Set up custom domain for backend (optional)
2. Configure SSL/TLS (automatically handled by Render)
3. Set up monitoring and alerts
4. Implement database backups for MongoDB Atlas

## Support

- Render Documentation: https://render.com/docs
- AyuPulseApp Issues: https://github.com/pankajcseaiml/AyuPulseApp/issues
- MongoDB Atlas Support: https://www.mongodb.com/docs/atlas/