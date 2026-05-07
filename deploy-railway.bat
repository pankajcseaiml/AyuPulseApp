@echo off
echo ========================================
echo AyuPulseApp Backend Deployment to Railway
echo ========================================
echo.

echo Step 1: Verify railway.json configuration
if not exist "railway.json" (
    echo ERROR: railway.json not found at repository root
    echo Please ensure railway.json exists at the root (not in backend/)
    pause
    exit /b 1
)

echo ✓ railway.json found at repository root
echo.

echo Step 2: Check requirements.txt
if not exist "backend\requirements.txt" (
    echo ERROR: requirements.txt not found in backend directory
    pause
    exit /b 1
)

echo ✓ requirements.txt found
echo.

echo Step 3: Check MongoDB Atlas configuration
echo.
echo IMPORTANT: Before deploying to Railway:
echo 1. Create a MongoDB Atlas cluster (free tier available)
echo 2. Get your connection string
echo 3. Whitelist all IPs (0.0.0.0/0) for testing
echo.
echo MongoDB Atlas setup steps:
echo 1. Go to https://www.mongodb.com/cloud/atlas
echo 2. Create free cluster
echo 3. Create database user
echo 4. Get connection string
echo 5. Add IP whitelist (Network Access)
echo.

echo Step 4: Railway Deployment Instructions
echo.
echo OPTION A: Deploy via Railway Dashboard (Recommended)
echo 1. Go to https://railway.app
echo 2. Sign up/login with GitHub
echo 3. Click "New Project" -> "Deploy from GitHub repo"
echo 4. Select "pankajcseaiml/AyuPulseApp"
echo 5. Railway will auto-detect railway.json at root
echo 6. Add environment variables (see backend/.env.production)
echo 7. Deploy
echo.
echo OPTION B: Deploy via Railway CLI
echo 1. Install: npm i -g @railway/cli
echo 2. Login: railway login
echo 3. Navigate to repository root (where railway.json is)
echo 4. Initialize: railway init
echo 5. Deploy: railway up
echo 6. Set variables: railway variables set MONGODB_URL "your_connection_string"
echo.

echo Step 5: After Railway Deployment
echo 1. Get your Railway backend URL (e.g., https://ayupulse-backend.up.railway.app)
echo 2. Update Vercel environment variable VITE_API_URL with this URL
echo 3. Test at https://ayu-pulse-app.vercel.app
echo.

echo Step 6: Quick Test
echo After deployment, test your backend with:
echo curl https://your-railway-backend.up.railway.app/health
echo Should return: {"status":"healthy","version":"1.0.0"}
echo.

echo For detailed instructions, see deploy-railway.md
echo.
pause