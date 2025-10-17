# Chinese Learning Web App

A web application for studying traditional Chinese texts with parallel text display, pinyin, and character-by-character analysis.

**Live Application**: [https://devocosm.com/chinese-study/](https://devocosm.com/chinese-study/)

## Features

- **Split-pane interface**: Chinese text on left, analysis on right
- **Sentence highlighting**: Click to select sentences for detailed analysis
- **Pinyin display**: Automatic pinyin generation for selected text
- **Translation layers**: 
  - Full English translation
  - Character-by-character literal translation
- **Navigation**: Forward/back buttons for sentence-by-sentence progression
- **Character analysis**: Right-click for additional character information

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API calls
- **Nginx** for production serving (in Docker)

### Backend
- **Python Flask** for API server
- **jieba** for Chinese text segmentation
- **pypinyin** for pinyin generation
- **python-dotenv** for environment management
- **gunicorn** for production serving

### Infrastructure
- **Docker** & **Docker Compose** for containerization
- **Cloudflare Pages** for frontend hosting
- **Railway** for backend hosting

## Project Structure

```
chinese-learning-app/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   └── types/           # TypeScript types
│   ├── public/
│   ├── Dockerfile           # Frontend Docker configuration
│   ├── nginx.conf           # Nginx configuration for production
│   ├── .env.development     # Development environment variables
│   ├── .env.production      # Production environment variables
│   └── package.json
├── backend/                  # Python Flask backend
│   ├── app/
│   │   ├── routes.py        # API routes
│   │   └── services/        # Business logic
│   ├── Dockerfile           # Backend Docker configuration
│   ├── .env.local           # Local environment variables
│   ├── .env.production      # Production environment variables
│   ├── requirements.txt
│   └── main.py
├── scripts/                  # Deployment scripts
│   ├── dev-local.ps1/.sh    # Start local development (no Docker)
│   ├── dev-docker.ps1/.sh   # Start Docker development
│   └── build-prod-local.ps1/.sh  # Build production locally
├── docker-compose.yml        # Main Docker Compose configuration
├── docker-compose.dev.yml    # Development overrides
├── docker-compose.prod.yml   # Production overrides
└── README.md
```

## Quick Start

### Option 1: Local Development (Recommended for Development)

**Windows:**
```powershell
.\scripts\dev-local.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/dev-local.sh
./scripts/dev-local.sh
```

This will:
- Start Flask backend on `http://localhost:5000`
- Start React frontend on `http://localhost:3000`
- Enable hot-reload for both services

### Option 2: Docker Development

**Windows:**
```powershell
.\scripts\dev-docker.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/dev-docker.sh
./scripts/dev-docker.sh
```

This will:
- Build and start Docker containers
- Enable hot-reload through volume mounts
- Backend on `http://localhost:5000`
- Frontend on `http://localhost:3000`

### Option 3: Production Build (Local Testing)

**Windows:**
```powershell
.\scripts\build-prod-local.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/build-prod-local.sh
./scripts/build-prod-local.sh
```

This will:
- Build optimized production Docker images
- Run production environment locally
- Backend on `http://localhost:5000`
- Frontend on `http://localhost:3000`

## Environment Configuration

### Backend Environment Variables

Located in `backend/.env.local` (development) or `backend/.env.production` (production):

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000

# CORS Allowed Origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,https://devocosm.com,https://chinese-study.devocosm.com

# Application Settings
HOST=0.0.0.0
```

### Frontend Environment Variables

Located in `frontend/.env.development` (development) or `frontend/.env.production` (production):

```bash
# API URL for backend
REACT_APP_API_URL=http://localhost:5000
```

For production:
```bash
REACT_APP_API_URL=https://chinese-study-production.up.railway.app
```

## Manual Setup (Without Scripts)

### Backend Setup
1. Create virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment file:
   ```bash
   cp .env.example .env.local
   ```

4. Run the server:
   ```bash
   python main.py
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Copy environment file:
   ```bash
   cp .env.example .env.development
   ```

3. Start development server:
   ```bash
   npm start
   ```

## Docker Commands Reference

### Development with Docker

Start development environment:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Stop and remove containers:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
```

Rebuild containers:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

### Production with Docker

Build production images:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
```

Start production environment:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

Run in detached mode:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop production environment:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
```

## Deployment to Production

### Current Deployment Setup

- **Frontend**: Cloudflare Pages at [https://devocosm.com/chinese-study/](https://devocosm.com/chinese-study/)
- **Backend**: Railway at [https://chinese-study-production.up.railway.app](https://chinese-study-production.up.railway.app)

### Cloudflare Pages (Frontend)

1. **Build Settings**:
   - Build command: `npm run build`
   - Build output directory: `build`
   - Root directory: `frontend`

2. **Environment Variables**:
   - `REACT_APP_API_URL=https://chinese-study-production.up.railway.app`

3. **Deploy**:
   - Push to main branch
   - Cloudflare Pages automatically builds and deploys

### Railway (Backend)

1. **Create New Project**:
   - Connect your GitHub repository
   - Select the `backend` directory as root

2. **Environment Variables**:
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   FLASK_PORT=5000
   HOST=0.0.0.0
   ALLOWED_ORIGINS=https://devocosm.com,https://chinese-study.devocosm.com
   ```

3. **Settings**:
   - Start Command: `gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 main:app`
   - Watch Paths: `backend/**`

4. **Deploy**:
   - Railway automatically deploys on push to main branch

### Alternative Deployment Options

#### Using Docker (Any Platform)

1. Build images:
   ```bash
   docker build -t chinese-learning-backend ./backend
   docker build -t chinese-learning-frontend ./frontend
   ```

2. Push to container registry (Docker Hub, GCR, ECR, etc.)

3. Deploy to:
   - **AWS ECS/EKS**
   - **Google Cloud Run**
   - **Azure Container Instances**
   - **DigitalOcean App Platform**
   - **Fly.io**

#### Traditional Hosting

**Backend (VPS/Dedicated Server)**:
1. Install Python 3.11+
2. Clone repository
3. Set up virtual environment
4. Install dependencies
5. Configure systemd service
6. Set up Nginx reverse proxy
7. Configure SSL with Let's Encrypt

**Frontend (Static Hosting)**:
1. Build React app: `npm run build`
2. Upload `build/` folder to:
   - **Netlify**
   - **Vercel**
   - **AWS S3 + CloudFront**
   - **GitHub Pages**
   - Any static file host

## API Endpoints

### Text Processing
- `POST /api/analyze` - Analyze Chinese text and return pinyin, translation, and character breakdown
- `GET /api/health` - Health check endpoint

### Response Format

```json
{
  "sentence": "这是一个例子",
  "pinyin": "zhè shì yī gè lì zi",
  "translation": "This is an example",
  "characters": [
    {
      "char": "这",
      "pinyin": "zhè",
      "meaning": "this"
    }
  ]
}
```

## Troubleshooting

### Port Already in Use

**Backend (Port 5000)**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

**Frontend (Port 3000)**:
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

### Docker Issues

**Docker not starting**:
- Make sure Docker Desktop is running
- Check Docker daemon status: `docker info`

**Containers not communicating**:
- Ensure both containers are on the same network
- Check `docker-compose.yml` network configuration
- Verify CORS origins include the frontend container

**Build failures**:
- Clear Docker cache: `docker system prune -a`
- Remove all containers: `docker-compose down -v`
- Rebuild from scratch: `docker-compose build --no-cache`

### Environment Variables Not Loading

1. Check file names: `.env.local`, `.env.development`, `.env.production`
2. Verify file encoding (should be UTF-8)
3. No quotes around values in .env files
4. Restart development server after changing .env files

### CORS Errors

1. Check backend `ALLOWED_ORIGINS` includes your frontend URL
2. Verify frontend is requesting the correct API URL
3. Check browser console for specific CORS error messages

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Chinese text segmentation: [jieba](https://github.com/fxsjy/jieba)
- Pinyin conversion: [pypinyin](https://github.com/mozillazg/python-pinyin)
- Frontend framework: [React](https://reactjs.org/)
- Backend framework: [Flask](https://flask.palletsprojects.com/)



