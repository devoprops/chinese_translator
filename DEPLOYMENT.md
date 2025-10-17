# Deployment Guide

Quick reference for deploying the Chinese Learning App in different environments.

## 🚀 Quick Commands

### Local Development (No Docker)

**Windows:**
```powershell
.\scripts\dev-local.ps1
```

**Linux/Mac:**
```bash
./scripts/dev-local.sh
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

### Docker Development

**Windows:**
```powershell
.\scripts\dev-docker.ps1
```

**Linux/Mac:**
```bash
./scripts/dev-docker.sh
```

**Manual:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Production Local Testing

**Windows:**
```powershell
.\scripts\build-prod-local.ps1
```

**Linux/Mac:**
```bash
./scripts/build-prod-local.sh
```

**Manual:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## 📋 Environment Files Checklist

### Backend
- [ ] `backend/.env.example` (template, committed to git)
- [ ] `backend/.env.local` (local development, not committed)
- [ ] `backend/.env.production` (production, not committed)

### Frontend
- [ ] `frontend/.env.example` (template, committed to git)
- [ ] `frontend/.env.development` (development, not committed)
- [ ] `frontend/.env.production` (production, not committed)

## 🌐 Current Production Setup

### Frontend - Cloudflare Pages
- **URL:** https://devocosm.com/chinese-study/
- **Build Command:** `npm run build`
- **Build Directory:** `build`
- **Root Directory:** `frontend`
- **Environment Variables:**
  - `REACT_APP_API_URL=https://chinese-study-production.up.railway.app`

### Backend - Railway
- **URL:** https://chinese-study-production.up.railway.app
- **Start Command:** `gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 main:app`
- **Root Directory:** `backend`
- **Environment Variables:**
  ```
  FLASK_ENV=production
  FLASK_DEBUG=False
  FLASK_PORT=5000
  HOST=0.0.0.0
  ALLOWED_ORIGINS=https://devocosm.com,https://chinese-study.devocosm.com
  ```

## 🔧 Updating Production

### Frontend (Cloudflare Pages)
1. Update code in `frontend/` directory
2. Commit and push to main branch
3. Cloudflare Pages automatically builds and deploys
4. Monitor build at Cloudflare Pages dashboard

### Backend (Railway)
1. Update code in `backend/` directory
2. Commit and push to main branch
3. Railway automatically builds and deploys
4. Monitor deployment at Railway dashboard
5. Check logs: Railway dashboard → Deployments → View Logs

### Both at Once
```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

Both services will automatically rebuild and redeploy.

## 🐛 Common Issues

### CORS Errors in Production
**Problem:** Frontend can't connect to backend

**Solution:**
1. Check Railway environment variables include frontend URL in `ALLOWED_ORIGINS`
2. Verify frontend is using correct backend URL
3. Check Railway logs for CORS error messages

### Environment Variables Not Applied
**Problem:** Changes to .env files not taking effect

**Solution:**
1. **Local:** Restart development server
2. **Railway:** Go to Variables tab, click "Update Variables"
3. **Cloudflare:** Go to Settings → Environment Variables, update and redeploy

### Docker Build Failures
**Problem:** Docker containers won't build

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose down -v
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build --no-cache
```

### Port Already in Use
**Problem:** Can't start server - port 3000 or 5000 in use

**Solution:**
```powershell
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

## 📊 Deployment Checklist

### Before Deploying to Production
- [ ] Test locally with production build (`build-prod-local`)
- [ ] Verify all environment variables are set correctly
- [ ] Check API endpoints return expected responses
- [ ] Test CORS from production frontend URL
- [ ] Verify health check endpoint works (`/health`)
- [ ] Check console for errors
- [ ] Test on different browsers
- [ ] Verify mobile responsiveness

### After Deployment
- [ ] Visit production URL and verify it loads
- [ ] Test main features (text analysis, translation, etc.)
- [ ] Check browser console for errors
- [ ] Monitor backend logs for errors
- [ ] Test API health endpoint
- [ ] Verify CORS working correctly
- [ ] Check performance (load times, API response times)

## 🔄 Rolling Back

### Cloudflare Pages
1. Go to Cloudflare Pages dashboard
2. Click on your project
3. Go to "Deployments"
4. Find previous working deployment
5. Click "..." → "Rollback to this deployment"

### Railway
1. Go to Railway dashboard
2. Click on your project
3. Go to "Deployments"
4. Find previous working deployment
5. Click "Redeploy"

### Git Revert
```bash
# Revert last commit
git revert HEAD

# Revert specific commit
git revert <commit-hash>

# Push to trigger redeployment
git push origin main
```

## 📈 Monitoring

### Check Backend Health
```bash
curl https://chinese-study-production.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Chinese Learning API is running",
  "environment": "production"
}
```

### Check Frontend
Visit: https://devocosm.com/chinese-study/

Should load without errors in browser console.

### Railway Logs
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# View logs
railway logs
```

## 🆘 Emergency Contacts

- **Railway Status:** https://status.railway.app/
- **Cloudflare Status:** https://www.cloudflarestatus.com/

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Railway Documentation](https://docs.railway.app/)
- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [React Deployment Guide](https://create-react-app.dev/docs/deployment/)

