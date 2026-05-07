@echo off
echo =========================================
echo AyuPulseApp Deployment Assistant
echo =========================================
echo.
echo This script will guide you through deploying AyuPulseApp.
echo Please follow these steps in order:
echo.

REM Step 1: Check prerequisites
echo Step 1: Checking prerequisites...
echo ---------------------------------

REM Check if git is installed
where git >nul 2>nul
if %errorlevel% equ 0 (
    echo ✓ Git is installed
) else (
    echo ✗ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

REM Check if node is installed
where node >nul 2>nul
if %errorlevel% equ 0 (
    echo ✓ Node.js is installed
) else (
    echo ✗ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

REM Check if python is installed
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo ✓ Python is installed
) else (
    echo ✗ Python is not installed. Please install Python 3.10+ first.
    pause
    exit /b 1
)

echo.
echo Step 2: MongoDB Atlas Setup
echo ---------------------------
echo.
echo 1. Go to https://www.mongodb.com/cloud/atlas
echo 2. Sign up for a free account
echo 3. Create a FREE tier cluster (M0 Sandbox)
echo 4. Configure Database Access:
echo    - Go to 'Database Access' → 'Add New Database User'
echo    - Create username and password
echo    - Set privileges: 'Read and write to any database'
echo 5. Configure Network Access:
echo    - Go to 'Network Access' → 'Add IP Address'
echo    - Add '0.0.0.0/0' (allow from anywhere)
echo 6. Get Connection String:
echo    - Go to 'Database' → 'Connect' → 'Connect your application'
echo    - Copy the connection string
echo    - Replace ^<password^> with your actual password
echo.
pause

echo.
echo Step 3: Railway Backend Deployment
echo ----------------------------------
echo.
echo 1. Go to https://railway.app/
echo 2. Sign up with GitHub
echo 3. Create New Project → 'Deploy from GitHub repo'
echo 4. Select the AyuPulseApp repository
echo 5. Configure Backend Service:
echo    - Set root directory to 'backend'
echo    - Railway will auto-detect Python
echo 6. Set Environment Variables in Railway dashboard:
echo.
echo Copy and paste these variables:
echo ---------------------------------
(
echo MONGODB_URL=your_mongodb_atlas_connection_string_here
echo DATABASE_NAME=ayupulse
echo SECRET_KEY=generate_a_secure_random_key_here
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=30
echo DEBUG=False
echo BACKEND_CORS_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:5173
echo MAX_UPLOAD_SIZE=10485760
echo ALLOWED_IMAGE_TYPES=image/jpeg,image/png,image/jpg
echo PORT=8000
)
echo ---------------------------------
echo.
echo 7. Deploy and note your backend URL (e.g., https://ayupulse-backend.up.railway.app)
echo.
pause

echo.
echo Step 4: Vercel Frontend Deployment
echo ----------------------------------
echo.
echo 1. Go to https://vercel.com/
echo 2. Sign up with GitHub
echo 3. Import your GitHub repository
echo 4. Configure Build Settings:
echo    - Root directory: 'frontend'
echo    - Build Command: 'npm run build'
echo    - Output Directory: 'dist'
echo 5. Set Environment Variables in Vercel dashboard:
echo.
echo Copy and paste these variables:
echo ---------------------------------
(
echo VITE_API_URL=https://your-railway-backend-url.up.railway.app
echo VITE_APP_NAME=AyuPulse
echo VITE_APP_VERSION=1.0.0
)
echo ---------------------------------
echo.
echo 6. Deploy and note your frontend URL (e.g., https://ayupulse.vercel.app)
echo.
pause

echo.
echo Step 5: Final Configuration
echo ---------------------------
echo.
echo 1. Update CORS in Railway Backend:
echo    - Go back to Railway dashboard
echo    - Update BACKEND_CORS_ORIGINS to include your Vercel URL
echo    - Example: 'https://ayupulse.vercel.app,http://localhost:5173'
echo.
echo 2. Test your deployment:
echo    - Backend API: https://your-railway-backend-url.up.railway.app/docs
echo    - Frontend: https://your-vercel-app.vercel.app
echo    - Health check: https://your-railway-backend-url.up.railway.app/health
echo.
echo 3. Create initial admin user:
echo    Use the demo admin account:
echo    - Username: admin
echo    - Password: admin123
echo.
echo =========================================
echo Deployment Complete!
echo =========================================
echo.
echo Your AyuPulseApp is now deployed:
echo - Frontend: https://your-vercel-app.vercel.app
echo - Backend: https://your-railway-backend-url.up.railway.app
echo - Database: MongoDB Atlas (cloud)
echo.
echo For troubleshooting, see DEPLOYMENT.md
echo.
pause