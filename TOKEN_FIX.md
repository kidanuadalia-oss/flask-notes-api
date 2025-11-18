# Token Permission Issue - Fix Required

Your token is being rejected with 403 errors. Here's how to fix it:

## Step 1: Create a NEW Token with Full Permissions

1. Go to: https://github.com/settings/tokens
2. **Delete** your current token (or create a new one)
3. Click "Generate new token" → "Generate new token (classic)"
4. Fill in:
   - **Note:** `Flask Notes API - Full Access`
   - **Expiration:** Your choice (90 days recommended)
   - **Repository access:** Select **"All repositories"** (IMPORTANT!)
   - **Permissions:** Under "Repository permissions", check:
     - ✅ **Contents** (Read and write) - THIS IS CRITICAL
     - ✅ **Metadata** (Read) - usually auto-checked
5. Scroll down and click **"Generate token"**
6. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)

## Step 2: Use the New Token

Once you have the new token, run:

```bash
cd /Users/adaliakidanu/Downloads/flask-notes-api
git push -u origin main
```

When prompted:
- Username: `kidanuadalia-oss`
- Password: [paste your NEW token]

## Alternative: Initialize via GitHub Website

If token still doesn't work:

1. Go to: https://github.com/kidanuadalia-oss/flask-notes-api
2. Click "Add file" → "Create new file"
3. Name it: `README.md`
4. Content: `# Flask Notes API`
5. Click "Commit new file"
6. Then run: `git pull origin main --allow-unrelated-histories`
7. Then run: `git push -u origin main`

---

**The key issue:** Your current token likely doesn't have "Contents: Write" permission enabled.

