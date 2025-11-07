# Backend Deployment Guide - Railway

Simple guide to deploy Lórien's Guide backend to Railway.

## Why Railway?

- ✅ Free tier ($5 credit/month)
- ✅ One-command deployment
- ✅ Automatic HTTPS
- ✅ Easy environment variables
- ✅ GitHub auto-deploy

## Prerequisites

- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))
- Your code pushed to GitHub

## Step 1: Prepare Your Project

Ensure these files exist in your repo:

**requirements.txt** (should already exist)
**Procfile** (create if missing):
```
web: gunicorn backend.app:app
```

**runtime.txt** (create if missing):
```
python-3.12.0
```

## Step 2: Deploy to Railway

### Option A: Railway Dashboard (Easiest)

1. Go to [railway.app](https://railway.app) and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `Loriens-Guide` repository
5. Railway will auto-detect Python and deploy

### Option B: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway init

# Deploy
railway up
```

## Step 3: Set Environment Variables

In Railway Dashboard → Your Project → Variables:

```
HACKATHON_API_KEY=your_key_here
HACKATHON_API_SECRET=your_secret_here
VLM_API_URL=https://api.mdi.milestonesys.com
PORT=5000
```

## Step 4: Get Your Backend URL

Railway will provide a URL like:
```
https://loriens-guide-production.up.railway.app
```

Copy this URL - you'll need it for the frontend.

## Step 5: Update Frontend

Update `frontend/app.js` with your Railway backend URL:

```javascript
const CONFIG = {
    backendUrl: 'https://your-app.up.railway.app',
    // ... rest of config
};
```

Commit and push to update your Cloudflare Pages frontend.

## Troubleshooting

### Build fails
- Check `requirements.txt` has all dependencies
- Verify Python version in `runtime.txt`

### App crashes on start
- Check Railway logs: Dashboard → Deployments → View Logs
- Verify environment variables are set
- Ensure `Procfile` uses correct path: `backend.app:app`

### API calls fail
- Test health endpoint: `https://your-app.up.railway.app/api/health`
- Check CORS settings in `backend/app.py`
- Verify environment variables

## Monitoring

Railway Dashboard provides:
- Deployment logs
- Runtime metrics (CPU, memory)
- Request metrics
- Crash alerts

## Updating Your App

Railway auto-deploys when you push to GitHub:

```bash
git add .
git commit -m "Update backend"
git push
```

Railway will automatically rebuild and deploy.

### 5. Test the API

```bash
# In another terminal
python example_client.py
```

## Production Deployment

### Using Gunicorn (Recommended)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

1. Create a `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

2. Build and run:
```bash
docker build -t loriens-guide .
docker run -p 5000:5000 --env-file .env loriens-guide
```

### Environment Variables

Ensure these are set in your production environment:

- `VLM_API_URL`: Your VLM API endpoint
- `VLM_API_KEY`: Your VLM API authentication key
- `PORT`: Port to run the server on (default: 5000)

## Cloud Deployment

### AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize:
```bash
eb init -p python-3.12 loriens-guide
```

3. Create environment:
```bash
eb create loriens-guide-env
```

4. Set environment variables:
```bash
eb setenv VLM_API_KEY=your_key VLM_API_URL=your_url
```

5. Deploy:
```bash
eb deploy
```

### Google Cloud Run

1. Create `Dockerfile` (see above)

2. Build and push:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/loriens-guide
```

3. Deploy:
```bash
gcloud run deploy loriens-guide \
  --image gcr.io/PROJECT_ID/loriens-guide \
  --platform managed \
  --set-env-vars VLM_API_KEY=your_key,VLM_API_URL=your_url
```

### Heroku

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy:
```bash
heroku create loriens-guide
heroku config:set VLM_API_KEY=your_key
heroku config:set VLM_API_URL=your_url
git push heroku main
```

## Video Storage

For production, consider using cloud storage for video files:

### AWS S3

1. Upload videos to S3 bucket
2. Update `cameras.json` with S3 URLs:
```json
{
  "video_clip_url": "https://your-bucket.s3.amazonaws.com/videos/library_lobby.mp4"
}
```

### Google Cloud Storage

1. Upload videos to GCS bucket
2. Update `cameras.json` with GCS URLs:
```json
{
  "video_clip_url": "https://storage.googleapis.com/your-bucket/videos/library_lobby.mp4"
}
```

## Monitoring

Consider adding:

- **Application monitoring**: New Relic, DataDog, or Sentry
- **Log aggregation**: CloudWatch, Stackdriver, or ELK stack
- **Uptime monitoring**: Pingdom, UptimeRobot, or StatusCake

## Security Considerations

1. **API Key Security**: Never commit API keys to version control
2. **HTTPS**: Use HTTPS in production (configure reverse proxy)
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **CORS**: Configure CORS appropriately for your mobile app
5. **Input Validation**: Already implemented, but review regularly

## Scaling

For high traffic:

1. **Horizontal Scaling**: Run multiple instances behind a load balancer
2. **Caching**: Cache VLM responses for common questions
3. **CDN**: Use CDN for video delivery
4. **Database**: Consider moving cameras.json to a database for better management

## Troubleshooting

### Server won't start
- Check Python version (3.12+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check port is not already in use

### VLM API errors
- Verify API key is correct
- Check API URL is reachable
- Review API rate limits

### Camera not found
- Verify coordinates are correct
- Check cameras.json is properly formatted
- Ensure at least one camera exists

## Support

For issues or questions:
- Check the README.md for documentation
- Review the example_client.py for usage examples
- Open an issue on GitHub
