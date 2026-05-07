@echo off
echo ============================================
echo AyuPulseApp Frontend Deployment to Vercel
echo ============================================
echo.
echo This script will guide you through deploying the frontend to Vercel.
echo.
echo IMPORTANT: You need a Vercel account (free) at https://vercel.com
echo.
echo Choose deployment method:
echo 1. Vercel Dashboard (Recommended - easiest)
echo 2. Vercel CLI (Advanced)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" goto dashboard
if "%choice%"=="2" goto cli

echo Invalid choice. Exiting.
pause
exit /b 1

:dashboard
echo.
echo ============================================
echo Vercel Dashboard Deployment Instructions
echo ============================================
echo.
echo 1. Go to https://vercel.com/new
echo 2. Sign in with GitHub, GitLab, or email
echo 3. Click "Import Project"
echo 4. Select "Import Git Repository"
echo 5. Enter: https://github.com/pankajcseaiml/AyuPulseApp
echo 6. Click "Continue"
echo 7. Configure project:
echo    - Framework Preset: Vite
echo    - Root Directory: frontend
echo    - Build Command: npm run build
echo    - Output Directory: dist
echo    - Install Command: npm install
echo 8. Add Environment Variables:
echo    - VITE_API_URL: https://your-backend-url.railway.app
echo    - VITE_APP_NAME: AyuPulseApp
echo    - VITE_APP_VERSION: 1.0.0
echo 9. Click "Deploy"
echo.
echo Your site will be live in 1-2 minutes!
echo.
pause
exit /b 0

:cli
echo.
echo ============================================
echo Vercel CLI Deployment
echo ============================================
echo.
echo First, you need to log in to Vercel:
echo.
echo Step 1: Run: vercel login
echo (This will open a browser for authentication)
echo.
echo Step 2: After login, run:
echo   cd frontend
echo   vercel --prod
echo.
echo Step 3: Follow the interactive prompts:
echo   - Set up and deploy: Y
echo   - Which scope: (choose your account)
echo   - Link to existing project: N
echo   - Project name: ayupulseapp
echo   - Directory: . (current directory)
echo.
echo Step 4: Set environment variables when prompted:
echo   - VITE_API_URL: https://your-backend-url.railway.app
echo   - VITE_APP_NAME: AyuPulseApp
echo   - VITE_APP_VERSION: 1.0.0
echo.
echo The deployment will start automatically.
echo.
pause
exit /b 0