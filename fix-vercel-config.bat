@echo off
echo ============================================
echo Fix Vercel Configuration for AyuPulseApp
echo ============================================
echo.
echo Your frontend is deployed at: https://ayu-pulse-app.vercel.app
echo But it's showing "Network Error" because it can't connect to backend.
echo.
echo Solution 1: Deploy backend to Railway (Recommended)
echo Solution 2: Use ngrok to expose local backend (Temporary)
echo.
set /p choice="Choose solution (1 or 2): "

if "%choice%"=="1" goto railway
if "%choice%"=="2" goto ngrok

echo Invalid choice. Exiting.
pause
exit /b 1

:railway
echo.
echo ============================================
echo Deploy Backend to Railway
echo ============================================
echo.
echo 1. Go to https://railway.app
echo 2. Sign in with GitHub
echo 3. Click "New Project" -> "Deploy from GitHub repo"
echo 4. Select your AyuPulseApp repository
echo 5. Railway will auto-detect Python backend
echo 6. Set these environment variables in Railway dashboard:
echo.
echo    MONGODB_URL=mongodb+srv://...
echo    SECRET_KEY=your-secret-key-here
echo    BACKEND_CORS_ORIGINS=https://ayu-pulse-app.vercel.app
echo.
echo 7. Wait for deployment to complete
echo 8. Get your backend URL (e.g., https://ayupulse-backend.railway.app)
echo 9. Go to Vercel dashboard: https://vercel.com/dashboard
echo 10. Select ayu-pulse-app project
echo 11. Go to Settings -> Environment Variables
echo 12. Add/Update VITE_API_URL with your Railway backend URL
echo 13. Redeploy the frontend
echo.
echo Your app will now work!
pause
exit /b 0

:ngrok
echo.
echo ============================================
echo Use ngrok for Temporary Backend Access
echo ============================================
echo.
echo 1. Install ngrok: https://ngrok.com/download
echo 2. Start your local backend (already running on port 8000)
echo 3. In a new terminal, run: ngrok http 8000
echo 4. Copy the ngrok URL (e.g., https://abc123.ngrok.io)
echo 5. Go to Vercel dashboard: https://vercel.com/dashboard
echo 6. Select ayu-pulse-app project
echo 7. Go to Settings -> Environment Variables
echo 8. Add/Update VITE_API_URL with your ngrok URL
echo 9. Redeploy the frontend
echo.
echo Note: ngrok URLs expire. For permanent solution, use Railway.
pause
exit /b 0