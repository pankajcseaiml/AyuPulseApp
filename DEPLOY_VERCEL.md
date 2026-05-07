# Deploy AyuPulseApp Frontend to Vercel

This guide provides step-by-step instructions to deploy the AyuPulseApp React frontend to Vercel.

## Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com) (free tier available)
3. **Backend API**: Your FastAPI backend should be deployed (e.g., on Railway) and accessible via a public URL

## Step 1: Prepare Your Frontend Code

Ensure your frontend code is ready for production:

1. **Check environment variables** in `frontend/.env.example`:
   ```env
   VITE_API_URL=https://your-railway-backend-url.up.railway.app
   VITE_APP_NAME=AyuPulse
   VITE_APP_VERSION=1.0.0
   ```

2. **Verify build works locally**:
   ```bash
   cd frontend
   npm run build
   ```
   
   This should create a `dist` folder with production-ready files.

## Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com)** and sign in with your GitHub account.

2. **Click "Add New" → "Project"**.

3. **Import your GitHub repository**:
   - Select the AyuPulseApp repository
   - Vercel will automatically detect it as a Vite/React project

4. **Configure Project Settings**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)

5. **Configure Environment Variables**:
   - Click "Environment Variables"
   - Add the following variables:
     - `VITE_API_URL`: Your backend API URL (e.g., `https://ayupulse-backend.up.railway.app`)
     - `VITE_APP_NAME`: `AyuPulse`
     - `VITE_APP_VERSION`: `1.0.0`

6. **Click "Deploy"**:
   - Vercel will build and deploy your application
   - You'll get a URL like `https://ayupulse.vercel.app`

### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

4. **Deploy to Vercel**:
   ```bash
   vercel
   ```
   
   Follow the interactive prompts:
   - Set up and deploy: `Y`
   - Which scope: Select your account
   - Link to existing project: `N`
   - Project name: `ayupulse-frontend` (or your preferred name)
   - Directory: `.`
   - Override settings: Accept defaults

5. **Set environment variables**:
   ```bash
   vercel env add VITE_API_URL
   vercel env add VITE_APP_NAME
   vercel env add VITE_APP_VERSION
   ```

6. **Deploy to production**:
   ```bash
   vercel --prod
   ```

## Step 3: Configure Custom Domain (Optional)

1. **Go to your project dashboard** on Vercel
2. **Click "Domains"** in the sidebar
3. **Add your domain** (e.g., `ayupulse.yourdomain.com`)
4. **Follow DNS configuration instructions**

## Step 4: Update Backend CORS Settings

After deploying the frontend, update your backend CORS settings to allow the Vercel domain:

1. **Go to your Railway backend dashboard**
2. **Edit environment variables**:
   - Add your Vercel URL to `BACKEND_CORS_ORIGINS`:
     ```
     https://ayupulse.vercel.app,http://localhost:5173
     ```
3. **Redeploy the backend** if necessary

## Step 5: Test the Deployment

1. **Visit your Vercel URL** (e.g., `https://ayupulse.vercel.app`)
2. **Test all functionality**:
   - Login with demo accounts
   - Create predictions
   - Test role-based access
   - Verify API calls to backend

## Step 6: Configure Automatic Deployments

1. **Enable GitHub integration** in Vercel project settings
2. **Configure branch deployments**:
   - Production: `main` branch
   - Preview: All other branches
3. **Set up webhooks** for automatic deployments on push

## Environment Variables Reference

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `VITE_API_URL` | Backend API URL (REQUIRED) | `https://ayupulse-backend.up.railway.app` |
| `VITE_APP_NAME` | Application name | `AyuPulse` |
| `VITE_APP_VERSION` | Application version | `1.0.0` |

## Troubleshooting

### Common Issues:

1. **Build fails**:
   - Check Node.js version (requires 16+)
   - Run `npm install` locally to check for dependency issues
   - Check build logs in Vercel dashboard

2. **API calls failing**:
   - Verify `VITE_API_URL` is correct
   - Check backend CORS settings
   - Test backend API directly

3. **Environment variables not loading**:
   - Rebuild after adding environment variables
   - Check variable names (must start with `VITE_` for Vite)
   - Clear browser cache

4. **Routing issues (404 on refresh)**:
   - Vercel's `vercel.json` configuration handles SPA routing
   - Ensure `rewrites` configuration is correct

### Vercel Dashboard Features:

- **Analytics**: Monitor traffic and performance
- **Logs**: View real-time deployment and runtime logs
- **Functions**: Serverless functions (if needed)
- **Edge Config**: Global configuration management
- **Integrations**: Connect to monitoring, analytics, etc.

## Maintenance

1. **Regular updates**:
   - Keep dependencies updated with `npm update`
   - Deploy updates by pushing to connected GitHub branch

2. **Monitoring**:
   - Use Vercel Analytics for performance monitoring
   - Set up error tracking (Sentry, etc.)

3. **Backup**:
   - GitHub repository serves as code backup
   - Database backups handled by MongoDB Atlas/Railway

## Support

- **Vercel Documentation**: https://vercel.com/docs
- **Vite Deployment Guide**: https://vitejs.dev/guide/static-deploy.html#vercel
- **Project Issues**: Check GitHub repository issues

## Next Steps

After deploying the frontend:
1. Deploy backend to Railway (see `DEPLOYMENT.md`)
2. Set up MongoDB Atlas database
3. Configure domain and SSL certificates
4. Set up monitoring and alerts

Your AyuPulseApp frontend is now live on Vercel! 🎉