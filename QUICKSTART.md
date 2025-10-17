# Quick Start Guide

Choose your development mode and get started in seconds!

## 🚀 For First-Time Setup

### Windows
```powershell
# Clone the repository (if not already done)
git clone <repository-url>
cd "Translate_and memorize"

# Start local development
.\scripts\dev-local.ps1
```

### Linux/Mac
```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd "Translate_and memorize"

# Start local development
./scripts/dev-local.sh
```

**That's it!** The script will:
- ✅ Set up Python virtual environment
- ✅ Install all dependencies
- ✅ Create environment files
- ✅ Start backend on http://localhost:5000
- ✅ Start frontend on http://localhost:3000

## 📦 Development Modes

### 1. Local Development (Recommended)
**Best for:** Day-to-day development, fastest reload

**Windows:** `.\scripts\dev-local.ps1`  
**Linux/Mac:** `./scripts/dev-local.sh`

- Native Python and Node.js
- Fastest hot-reload
- Easiest to debug
- No Docker required

### 2. Docker Development
**Best for:** Testing in isolated environment, matching production

**Windows:** `.\scripts\dev-docker.ps1`  
**Linux/Mac:** `./scripts/dev-docker.sh`

- Containerized environment
- Hot-reload enabled
- Matches production closely
- Requires Docker Desktop

### 3. Production Build (Local)
**Best for:** Testing production build before deployment

**Windows:** `.\scripts\build-prod-local.ps1`  
**Linux/Mac:** `./scripts/build-prod-local.sh`

- Optimized production build
- Tests production configuration
- Nginx + Gunicorn
- Requires Docker Desktop

## 🔧 Common Tasks

### Making Changes
1. Edit files in `backend/` or `frontend/`
2. Changes auto-reload in development mode
3. Check browser console and terminal for errors

### Stopping Servers
- **Local mode:** Close the terminal windows or press Ctrl+C
- **Docker mode:** Press Ctrl+C in the terminal running docker-compose

### Viewing Logs
- **Local mode:** Check the terminal windows
- **Docker mode:** `docker-compose logs -f`

### Restarting Everything
- **Local mode:** Close terminals and re-run the dev script
- **Docker mode:** `docker-compose down` then re-run the dev script

## 🌐 URLs

### Development
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Health Check: http://localhost:5000/health

### Production
- Frontend: https://devocosm.com/chinese-study/
- Backend: https://chinese-study-production.up.railway.app
- Health Check: https://chinese-study-production.up.railway.app/health

## 📝 Environment Variables

### Backend (`backend/.env.local`)
```bash
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
HOST=0.0.0.0
ALLOWED_ORIGINS=http://localhost:3000,https://devocosm.com
```

### Frontend (`frontend/.env.development`)
```bash
REACT_APP_API_URL=http://localhost:5000
```

**Note:** Environment files are created automatically by the dev scripts!

## 🐛 Quick Troubleshooting

### Port Already in Use
```powershell
# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac - Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Docker Not Starting
1. Make sure Docker Desktop is running
2. Try: `docker info` to verify Docker is accessible

### Changes Not Showing
1. Check browser console for errors
2. Try hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
3. Clear browser cache
4. Restart development server

### Dependencies Out of Date
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## 📚 Need More Help?

- **Full Setup Guide:** See `README.md`
- **Deployment Guide:** See `DEPLOYMENT.md`
- **What Changed:** See `CHANGES.md`

## ⚡ Pro Tips

1. **Keep terminals visible** - Easier to spot errors
2. **Check health endpoint** - Verify backend is running: http://localhost:5000/health
3. **Browser DevTools** - F12 to see network requests and console errors
4. **Git before big changes** - Commit working code before major changes
5. **Test production builds** - Use `build-prod-local` before deploying

## 🎯 Typical Workflow

### Daily Development
```bash
1. Pull latest changes:        git pull
2. Start dev environment:      .\scripts\dev-local.ps1
3. Make changes in your editor
4. Test in browser:            http://localhost:3000
5. Commit when happy:          git commit -m "Description"
```

### Before Deployment
```bash
1. Test production build:      .\scripts\build-prod-local.ps1
2. Verify everything works
3. Commit changes:             git add . && git commit -m "Ready for deploy"
4. Push to GitHub:             git push origin main
5. Watch auto-deployment on Railway/Cloudflare dashboards
```

---

**Happy Coding! 🎉**

For detailed documentation, see `README.md` and `DEPLOYMENT.md`.

