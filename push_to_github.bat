@echo off
echo ============================================
echo AyuPulseApp - Push to GitHub
echo ============================================
echo.
echo This script will help you push the AyuPulseApp project to GitHub.
echo.
echo Before running this script:
echo 1. Go to https://github.com/pankajcseaiml
echo 2. Click the "+" icon in the top-right and select "New repository"
echo 3. Name it "AyuPulseApp" (or any name you prefer)
echo 4. Keep it public or private as desired
echo 5. DO NOT initialize with README, .gitignore, or license
echo 6. Click "Create repository"
echo.
echo After creating the repository, you'll see a page with Git commands.
echo Copy the repository URL (it should look like:
echo   https://github.com/pankajcseaiml/AyuPulseApp.git)
echo.
set /p REPO_URL="Enter the GitHub repository URL: "

echo.
echo Setting remote repository to %REPO_URL%
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo.
echo Pushing to GitHub...
git push -u origin master

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo SUCCESS! Project pushed to GitHub.
    echo ============================================
    echo.
    echo Your project is now available at:
    echo   %REPO_URL%
    echo.
    echo Both backend and frontend servers are running:
    echo   Backend: http://localhost:8000
    echo   Frontend: http://localhost:5173
    echo   API Docs: http://localhost:8000/docs
) else (
    echo.
    echo ============================================
    echo ERROR: Failed to push to GitHub.
    echo ============================================
    echo.
    echo Possible issues:
    echo 1. Repository URL is incorrect
    echo 2. GitHub repository not created yet
    echo 3. Authentication required
    echo.
    echo For authentication, you may need to:
    echo - Use GitHub Personal Access Token
    echo - Or use SSH key authentication
)

pause