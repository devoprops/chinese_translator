# Chinese Learning Web App - Setup Guide (Windows)

## Quick Start

### Prerequisites
- **Node.js** (v16 or higher) - [Download from nodejs.org](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download from python.org](https://python.org/)
- **Git** - [Download from git-scm.com](https://git-scm.com/)

### 1. Setup Backend (PowerShell)

Open **PowerShell** as Administrator and run:

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The backend will start on `http://localhost:5000`

### 2. Setup Frontend (PowerShell)

Open a **new PowerShell window** and run:

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will start on `http://localhost:3000`

### 3. Alternative: Use the Deployment Script

You can also use the provided PowerShell script:

```powershell
# Run the deployment script
.\deploy.ps1
```

## How to Use

### Copy-Paste Workflow
1. **Copy text** from any Chinese source (website, document, etc.)
2. **Click "Load Text"** in the left pane
3. **Paste the text** into the text area
4. **Click "Load Text"** to process and display
5. **Click on sentences** to analyze them in the right pane
6. **Use navigation buttons** to move between sentences

### Features
- **Safe and secure** - no external requests or web scraping
- **Works with any text source** - copy from anywhere
- **Real-time analysis** - pinyin, translation, and character breakdown
- **Navigation controls** - move through sentences easily

## Project Structure

```
chinese-learning-app/
├── backend/                 # Python Flask API
│   ├── app/
│   │   ├── routes.py       # API endpoints
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── main.py            # Flask app entry point
├── frontend/               # React TypeScript app
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   ├── types/         # TypeScript types
│   │   └── App.tsx        # Main app component
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.js # Tailwind CSS config
├── deploy.ps1             # PowerShell deployment script
└── README.md              # Project documentation
```

## Features Implemented

### ✅ Core Features
- **Copy-paste interface** for safe text input
- **Split-pane interface** with Chinese text on left, analysis on right
- **Clickable sentence selection** with highlighting
- **Pinyin generation** for selected text
- **English translation** display
- **Character-by-character analysis** with meanings
- **Forward/back navigation** buttons
- **Responsive design** with Tailwind CSS

### 🔄 In Progress
- Enhanced character dictionary
- Right-click context menus
- Text search functionality

### 📋 Planned Features
- User progress tracking
- Bookmarking system
- Export functionality
- Audio pronunciation
- Stroke order animations

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/text/:id` | GET | Get text by ID |
| `/api/analyze` | POST | Analyze Chinese text |
| `/api/translate` | POST | Translate to English |
| `/api/pinyin` | POST | Generate pinyin |
| `/api/characters/:char` | GET | Get character info |

## Development Notes

### Backend
- Uses Flask with CORS enabled for frontend communication
- Implements service pattern for clean separation of concerns
- Includes fallback dictionaries for offline functionality
- **No web scraping** - completely safe and respectful
- Ready for integration with external translation APIs

### Frontend
- React 18 with TypeScript for type safety
- Tailwind CSS for styling
- Axios for API communication
- Component-based architecture
- Responsive design
- **Copy-paste interface** for safe text input

## Security & Privacy

### ✅ Safe Features
- **No external requests** - all processing is local
- **No web scraping** - respects source websites
- **Copy-paste only** - user controls what text to analyze
- **No data collection** - text stays on your device
- **Respectful approach** - doesn't interact with source sites

### 🔒 Privacy First
- Text processing happens locally
- No data sent to external services (except for analysis)
- User controls all input and output
- No tracking or analytics

## Windows-Specific Setup

### PowerShell Execution Policy
If you get execution policy errors, run:

```powershell
# Set execution policy to allow local scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python Virtual Environment
On Windows, virtual environment activation uses:

```powershell
# Activate virtual environment
venv\Scripts\Activate.ps1

# Deactivate when done
deactivate
```

### Node.js and npm
Make sure Node.js is installed and in your PATH:

```powershell
# Check Node.js version
node --version

# Check npm version
npm --version
```

## Deployment

### Frontend (Cloudflare Pages)
1. Push code to GitHub repository
2. Connect repository to Cloudflare Pages
3. Set build command: `npm run build`
4. Set build output directory: `build`
5. Deploy

### Backend Options
1. **Railway** (Recommended)
   - Easy Python deployment
   - Automatic HTTPS
   - Good free tier

2. **Render**
   - Free tier available
   - Easy setup
   - Good for Python apps

3. **Heroku**
   - Traditional choice
   - Good documentation
   - Paid service

4. **Vercel**
   - Serverless functions
   - Good for small APIs
   - Free tier available

## Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

### Backend (.env)
```
FLASK_ENV=development
FLASK_DEBUG=1
```

## Troubleshooting (Windows)

### Common Issues

1. **PowerShell Execution Policy**
   ```powershell
   # Fix: Set execution policy
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Python not found**
   ```powershell
   # Fix: Add Python to PATH or use full path
   C:\Users\YourUsername\AppData\Local\Programs\Python\Python39\python.exe
   ```

3. **Node.js not found**
   ```powershell
   # Fix: Reinstall Node.js and restart PowerShell
   ```

4. **CORS Errors**
   - Ensure backend CORS is configured for frontend URL
   - Check that API_BASE_URL is correct

5. **Chinese Text Display**
   - Ensure proper font families are installed
   - Check browser encoding settings

6. **API Connection**
   - Verify backend is running on correct port
   - Check network connectivity
   - Review browser console for errors

### Performance Tips

1. **Backend**
   - Use caching for frequently accessed data
   - Implement pagination for large texts
   - Consider CDN for static assets

2. **Frontend**
   - Implement virtual scrolling for large texts
   - Use React.memo for expensive components
   - Optimize bundle size with code splitting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please respect the original content sources.
