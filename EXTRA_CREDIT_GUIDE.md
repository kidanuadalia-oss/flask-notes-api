# Extra Credit Setup Guide

This guide will help you get the +10 extra credit points:
- Cloud deployment with stable URL (+5 points)
- Observability/CI build (+5 points)

## Part 1: CI/CD Pipeline (+5 points)

### Option A: Add via GitHub UI (Easiest)

1. Go to your repository: https://github.com/kidanuadalia-oss/flask-notes-api
2. Click "Add file" → "Create new file"
3. Type the path: `.github/workflows/ci.yml`
4. Copy the entire contents from the file `.github/workflows/ci.yml` in your local repo
5. Click "Commit new file"
6. The CI will start running automatically!

### Option B: Update Token and Push

1. Go to https://github.com/settings/tokens
2. Find your token (or create a new one)
3. Edit it and check the box for **"workflow"** scope
4. Save the token
5. Then push:
   ```bash
   git push https://kidanuadalia-oss:YOUR_NEW_TOKEN@github.com/kidanuadalia-oss/flask-notes-api.git main
   ```

### Verify CI is Working

1. Go to your repo on GitHub
2. Click the "Actions" tab
3. You should see a workflow run
4. It should show green checkmarks when tests pass

## Part 2: Cloud Deployment (+5 points)

### Step 1: Set up MongoDB Atlas (Free)

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for a free account
3. Create a new cluster (choose the free M0 tier)
4. Wait for cluster to finish creating (~5 minutes)
5. Click "Connect" → "Connect your application"
6. Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
7. Create a database user:
   - Click "Database Access" → "Add New Database User"
   - Username: `flasknotes` (or whatever you want)
   - Password: Generate a secure password (save it!)
   - Database User Privileges: "Read and write to any database"
   - Click "Add User"
8. Whitelist IP addresses:
   - Click "Network Access" → "Add IP Address"
   - Click "Allow Access from Anywhere" (0.0.0.0/0)
   - Click "Confirm"
9. Update your connection string:
   - Replace `<username>` with your database username
   - Replace `<password>` with your database password
   - Add `/notes` at the end: `mongodb+srv://username:password@cluster.mongodb.net/notes`

### Step 2: Deploy to Render.com (Free)

1. Go to https://render.com
2. Sign up with your GitHub account
3. Click "New +" → "Web Service"
4. Connect your repository:
   - Select "kidanuadalia-oss/flask-notes-api"
   - Branch: `main`
5. Configure the service:
   - **Name:** `flask-notes-api` (or whatever you want)
   - **Environment:** `Docker`
   - **Region:** Choose closest to you (e.g., "Oregon (US West)")
   - **Branch:** `main`
   - **Root Directory:** Leave empty
   - **Dockerfile Path:** `Dockerfile` (default)
6. Set environment variables (click "Advanced"):
   ```
   FLASK_ENV=production
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/notes?retryWrites=true&w=majority
   PORT=8080
   ```
   (Replace with your actual MongoDB connection string from Step 1)
7. Configure health check:
   - Health Check Path: `/health`
8. Click "Create Web Service"
9. Wait 5-10 minutes for the first deployment
10. You'll get a URL like: `https://flask-notes-api.onrender.com`

### Step 3: Test Your Deployment

```bash
# Health check
curl https://your-app.onrender.com/health

# Create a note
curl -X POST https://your-app.onrender.com/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Test from Render", "body": "This works!"}'

# Get all notes
curl https://your-app.onrender.com/notes
```

### Step 4: Update README

1. Edit `README.md`
2. Find the "Links" section
3. Replace `[Deploy using instructions above, then add your URL here]` with your actual Render URL
4. Commit and push:
   ```bash
   git add README.md
   git commit -m "Add deployment URL"
   git push
   ```

## Verification Checklist

- [ ] CI workflow file added to `.github/workflows/ci.yml`
- [ ] CI shows green checkmarks in GitHub Actions tab
- [ ] MongoDB Atlas cluster created and running
- [ ] Render.com service deployed and running
- [ ] Health check endpoint works: `curl https://your-app.onrender.com/health`
- [ ] Can create notes via the deployed API
- [ ] Deployment URL added to README.md

## Troubleshooting

**CI not running?**
- Make sure the workflow file is in `.github/workflows/ci.yml`
- Check the "Actions" tab for any error messages
- Verify your tests pass locally: `pytest tests/ -v`

**Render deployment fails?**
- Check the build logs in Render dashboard
- Verify MONGO_URI is correct (no typos)
- Make sure MongoDB Atlas IP whitelist includes Render IPs (or 0.0.0.0/0)

**MongoDB connection errors?**
- Verify username/password in connection string
- Check IP whitelist in MongoDB Atlas
- Make sure database name `/notes` is at the end of connection string

## What You'll Get

✅ **+5 points** for CI/CD pipeline (automated testing)
✅ **+5 points** for cloud deployment (stable URL on Render.com)
✅ **Total: +10 extra credit points!**

Good luck! 🚀

