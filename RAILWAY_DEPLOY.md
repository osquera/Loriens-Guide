# Railway Deployment - Quick Start

## 🚂 Deploy Backend to Railway in 5 Minutes

### Step 1: Sign up for Railway
Go to [railway.app](https://railway.app) and sign in with GitHub

### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `Loriens-Guide` repository
4. Railway auto-detects Python and starts deploying

### Step 3: Add Environment Variables
In Railway Dashboard → Project → Variables tab, add:

```
HACKATHON_API_KEY=your_key_here
HACKATHON_API_SECRET=your_secret_here
VLM_API_URL=https://api.mdi.milestonesys.com
PORT=5000
```

### Step 4: Get Your URL
Railway provides a URL like:
```
https://loriens-guide-production.up.railway.app
```

Copy this URL!

### Step 5: Update Frontend
Edit `frontend/app.js` line ~200:

```javascript
const CONFIG = {
    backendUrl: 'https://your-app.up.railway.app', // ← Update this
    // ...
};
```

Commit and push - Cloudflare Pages will auto-deploy the updated frontend.

## Done! ✅

Your app is now fully deployed:
- Frontend: https://loriensguide.osquera.com
- Backend: https://your-app.up.railway.app

## Troubleshooting

### Check backend is running:
```bash
curl https://your-app.up.railway.app/api/health
```

Should return: `{"status": "healthy"}`

### View logs:
Railway Dashboard → Deployments → View Logs

### Redeploy:
Just push to GitHub - Railway auto-deploys
