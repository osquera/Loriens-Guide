@echo off
REM Deployment script for Lórien's Guide to Cloudflare Pages

echo ================================================
echo Lórien's Guide - Cloudflare Pages Deployment
echo ================================================
echo.

echo.
echo [1/3] Verifying frontend files...
if not exist "frontend\index.html" (
    echo [ERROR] frontend\index.html not found!
    echo Make sure you're running this from the project root.
    pause
    exit /b 1
)

if not exist "frontend\app.js" (
    echo [ERROR] frontend\app.js not found!
    pause
    exit /b 1
)

if not exist "frontend\styles.css" (
    echo [ERROR] frontend\styles.css not found!
    pause
    exit /b 1
)

echo [OK] All frontend files found.
echo.

echo [2/3] Deploying to Cloudflare Pages...
echo.
wrangler pages deploy frontend --project-name=loriens-guide

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo [SUCCESS] Deployment completed!
    echo ================================================
    echo.
    echo Your app is now live at:
    echo https://loriens-guide.pages.dev
    echo.
    echo Next steps:
    echo 1. Update API_BASE_URL in frontend/app.js with your backend URL
    echo 2. Configure custom domain in Cloudflare Dashboard (optional)
    echo 3. Test the app on mobile devices
    echo.
    echo View your deployment:
    echo https://dash.cloudflare.com/pages
    echo.
) else (
    echo.
    echo [ERROR] Deployment failed!
    echo Check the error messages above.
    echo.
)

echo [3/3] Done!
pause
