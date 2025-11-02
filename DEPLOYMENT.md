# Backend Deployment Guide

This guide covers deploying the FastAPI backend to various platforms.

## Prerequisites

1. **Environment Variables**
   - `GOOGLE_API_KEY`: Your Google Gemini API key (required)

2. **Update CORS Settings**
   - After deployment, update `app.py` to include your Vercel frontend URL in `allow_origins`

## Option 1: Render.com (Recommended - Free Tier Available)

### Steps:

1. **Create a Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `backend` folder as the root directory

3. **Configure the Service**
   - **Name**: `ai-legal-backend` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free tier is fine to start

4. **Add Environment Variables**
   - In the dashboard, go to "Environment"
   - Add: `GOOGLE_API_KEY` = `your-api-key-here`

5. **Update CORS in app.py**
   - Add your Render URL to `allow_origins`:
   ```python
   allow_origins=[
       "http://localhost:3000",
       "https://your-vercel-app.vercel.app",
       "https://your-render-url.onrender.com"
   ]
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (first deploy takes 5-10 minutes)

---

## Option 2: Railway.app (Easy & Fast)

### Steps:

1. **Create a Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Service**
   - Railway auto-detects Python
   - Select the `backend` folder
   - Add `requirements.txt` (already created)

4. **Set Start Command**
   - Go to "Settings" → "Deploy"
   - Add start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables**
   - Go to "Variables" tab
   - Add: `GOOGLE_API_KEY` = `your-api-key-here`

6. **Update CORS**
   - Add your Railway domain to `allow_origins` in `app.py`

7. **Deploy**
   - Railway auto-deploys on git push

---

## Option 3: Fly.io (Good Performance)

### Steps:

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Create App**
   ```bash
   cd backend
   fly launch
   ```

4. **Add Environment Variable**
   ```bash
   fly secrets set GOOGLE_API_KEY=your-api-key-here
   ```

5. **Deploy**
   ```bash
   fly deploy
   ```

---

## Option 4: PythonAnywhere (Free Tier Available)

### Steps:

1. **Create Account**
   - Go to https://www.pythonanywhere.com
   - Sign up for free account

2. **Upload Files**
   - Use Files tab to upload your backend folder
   - Or use Git: `git clone https://github.com/your-repo.git`

3. **Create Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" → "Python 3.10"

4. **Configure**
   - Edit WSGI file to point to your app:
   ```python
   import sys
   sys.path.insert(0, '/home/username/backend')
   from app import app
   ```

5. **Set Environment Variables**
   - Create `.env` file or use bash console to export:
   ```bash
   export GOOGLE_API_KEY=your-api-key
   ```

6. **Install Dependencies**
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

7. **Reload Web App**
   - Click "Reload" button

---

## Update CORS After Deployment

After deploying, update `backend/app.py`:

```python
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Keep for local development
        "https://your-vercel-app.vercel.app",  # Your Vercel frontend
        "https://your-backend-url.onrender.com"  # Your backend URL (if needed)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Update Frontend API URL

In `ai-legal/src/pages/ToolPage.jsx`, update the API URL:

```javascript
const response = await fetch('https://your-backend-url.onrender.com/api/summarize', {
    // ... rest of the code
});
```

Or use environment variables (recommended):

1. Create `.env` file in `ai-legal/`:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

2. Update fetch:
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   const response = await fetch(`${API_URL}/api/summarize`, {
   ```

---

## Testing Your Deployment

1. **Check Backend Health**
   - Visit: `https://your-backend-url.onrender.com/`
   - Should see: `{"message": "Legal Document Summarizer API"}`

2. **Test API Endpoint**
   - Use Postman or curl to test `/api/summarize`
   - Make sure CORS is working

3. **Check Logs**
   - Most platforms provide logs in dashboard
   - Check for any errors during deployment

---

## Troubleshooting

### Common Issues:

1. **CORS Errors**
   - Make sure your frontend URL is in `allow_origins`
   - Check for trailing slashes

2. **Environment Variables Not Loading**
   - Verify variable names match exactly
   - Some platforms need restart after adding vars

3. **Build Fails**
   - Check Python version (should be 3.8+)
   - Verify all dependencies in `requirements.txt`

4. **Module Not Found**
   - Ensure `source/` folder is included in deployment
   - Check relative imports

5. **Port Issues**
   - Use `$PORT` environment variable (platforms provide this)
   - Default to 8000 if not available

---

## Recommended: Render.com

Render.com is recommended because:
- ✅ Free tier available
- ✅ Easy GitHub integration
- ✅ Automatic SSL certificates
- ✅ Good documentation
- ✅ Easy environment variable management

Your backend URL will look like: `https://ai-legal-backend.onrender.com`

