# Cloudflare Pages Deployment Guide

This guide explains how to deploy the Chinese Study app frontend to Cloudflare Pages at `https://devocosm.com/chinese-study/`

## Prerequisites

- Cloudflare account with Pages enabled
- Domain `devocosm.com` connected to Cloudflare
- Node.js and npm installed locally (for building)

## Deployment Structure

The app is part of the DevoCosm website:
```
devocosm.com/
├── index.html              (Main landing page)
├── apps.html               (Apps listing page)
├── listo.html              (Listo app page)
├── privacy_policy.html     (Privacy policy)
└── chinese-study/          (Chinese Study React app)
    ├── index.html
    ├── static/
    │   ├── css/
    │   └── js/
    └── _redirects
```

## Method 1: Build Locally and Upload

### Step 1: Build the Frontend

```bash
cd frontend
npm install
npm run build
```

This creates the production build in `frontend/build/`

### Step 2: Prepare Deployment Folder

The `build` folder should contain:
- `index.html` - Main app entry point
- `static/` - CSS, JS, and other assets
- `_redirects` - Cloudflare routing rules
- `asset-manifest.json` - Build manifest

### Step 3: Deploy to Cloudflare Pages

**Option A: Via Cloudflare Dashboard**
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Pages
2. Select your `devocosm.com` project
3. Click "Create deployment"
4. Upload the contents of `frontend/build/` to the `chinese-study` directory
5. Confirm deployment

**Option B: Via Wrangler CLI**
```bash
# Install Wrangler (if not already installed)
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy the build folder
cd frontend
wrangler pages deploy build --project-name=devocosm --branch=main
```

## Method 2: Connect GitHub for Auto-Deploy

### Step 1: Connect Repository

1. Go to Cloudflare Dashboard → Pages
2. Create new project → Connect to Git
3. Select your GitHub account and repository: `devoprops/chinese_translator`
4. Configure build settings:

### Step 2: Build Configuration

**Framework preset**: `Create React App`

**Build settings**:
- **Build command**: `cd frontend && npm install && npm run build`
- **Build output directory**: `frontend/build`
- **Root directory**: `/` (leave blank)
- **Environment variables**: (none needed for frontend-only build)

### Step 3: Advanced Settings

**Custom domain**: 
- Primary: `devocosm.com`
- Subdomain: Ensure `chinese-study` is set as a subdirectory route

**Branch deployments**:
- Production branch: `master`
- Enable automatic deployments: `ON`

## Method 3: Manual File Structure (Current Setup)

If the DevoCosm main site is manually managed:

### Step 1: Build the React App

```bash
cd frontend
npm run build
```

### Step 2: Upload to Cloudflare

Structure your Cloudflare Pages deployment like this:

```
/
├── index.html                    (from devocosm_html/)
├── apps.html                     (from devocosm_html/)
├── listo.html                    (from devocosm_html/)
├── privacy_policy.html           (from devocosm_html/)
└── chinese-study/
    ├── index.html                (from frontend/build/)
    ├── asset-manifest.json       (from frontend/build/)
    ├── _redirects                (from frontend/build/)
    └── static/                   (from frontend/build/static/)
        ├── css/
        │   └── main.6e2b65fc.css
        └── js/
            └── main.61784ac1.js
```

### Step 3: Copy Files

```powershell
# PowerShell script to prepare deployment folder
New-Item -ItemType Directory -Force -Path "deploy"
New-Item -ItemType Directory -Force -Path "deploy/chinese-study"

# Copy DevoCosm main site files
Copy-Item "devocosm_html/*" -Destination "deploy/" -Recurse

# Copy Chinese Study app build
Copy-Item "frontend/build/*" -Destination "deploy/chinese-study/" -Recurse

# Now upload the 'deploy' folder to Cloudflare Pages
```

**Bash equivalent**:
```bash
#!/bin/bash
mkdir -p deploy/chinese-study

# Copy DevoCosm main site files
cp -r devocosm_html/* deploy/

# Copy Chinese Study app build
cp -r frontend/build/* deploy/chinese-study/

# Now upload the 'deploy' folder to Cloudflare Pages
```

## Verification

After deployment, verify:

1. **Main site**: `https://devocosm.com/` loads correctly
2. **Apps page**: `https://devocosm.com/apps.html` shows Chinese Study app
3. **Chinese Study app**: `https://devocosm.com/chinese-study/` loads the React app
4. **Backend connection**: App can connect to Railway backend at `https://chinese-study-production.up.railway.app`

## Troubleshooting

### Issue: 404 on Chinese Study Routes

**Problem**: Navigating within the app causes 404 errors

**Solution**: Ensure `_redirects` file is in the build output:
```
/*    /index.html   200
```

### Issue: Assets Not Loading

**Problem**: CSS/JS files return 404

**Solution**: Check that `package.json` has correct `homepage` field:
```json
"homepage": "/chinese-study"
```

### Issue: API Calls Failing

**Problem**: Frontend can't connect to backend

**Solution**: Verify `frontend/src/config.ts` has correct API URL:
```typescript
export const config = {
  apiUrl: 'https://chinese-study-production.up.railway.app'
};
```

## Environment-Specific Configuration

The frontend automatically uses the correct API URL based on build environment:

- **Development**: `http://localhost:5000`
- **Production**: `https://chinese-study-production.up.railway.app`

This is configured in `frontend/src/config.ts` and `frontend/.env.development`.

## Manual Deployment Script (PowerShell)

```powershell
# deploy-cloudflare.ps1
Write-Host "[*] Building frontend..."
cd frontend
npm install
npm run build
cd ..

Write-Host "[*] Preparing deployment folder..."
Remove-Item -Recurse -Force deploy -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path "deploy/chinese-study"

Write-Host "[*] Copying DevoCosm site files..."
Copy-Item "devocosm_html/*" -Destination "deploy/" -Recurse

Write-Host "[*] Copying Chinese Study app..."
Copy-Item "frontend/build/*" -Destination "deploy/chinese-study/" -Recurse

Write-Host "[+] Deployment folder ready at: deploy/"
Write-Host "[i] Upload this folder to Cloudflare Pages"
```

## Next Steps

1. Build the frontend: `npm run build` in `frontend/` directory
2. Choose your deployment method (manual upload or GitHub auto-deploy)
3. Upload to Cloudflare Pages
4. Verify the app works at `https://devocosm.com/chinese-study/`
5. Test backend connectivity

## Support

For issues with:
- **Frontend deployment**: Check Cloudflare Pages logs
- **Backend connectivity**: Check Railway logs
- **Build errors**: Check `frontend/` build output

Repository: https://github.com/devoprops/chinese_translator

