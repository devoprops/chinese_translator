# Chinese Learning Web App

A web application for studying traditional Chinese texts with parallel text display, pinyin, and character-by-character analysis.

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

### Backend
- **Python Flask** for API server
- **jieba** for Chinese text segmentation
- **pypinyin** for pinyin generation
- **requests** for web scraping
- **BeautifulSoup** for HTML parsing

## Project Structure

```
chinese-learning-app/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   ├── types/           # TypeScript types
│   │   └── utils/           # Utility functions
│   ├── public/
│   └── package.json
├── backend/                  # Python Flask backend
│   ├── app/
│   │   ├── routes/          # API routes
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utility functions
│   ├── requirements.txt
│   └── main.py
├── data/                     # Text data and translations
└── README.md
```

## Setup Instructions

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

3. Run the server:
   ```bash
   python main.py
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start development server:
   ```bash
   npm start
   ```

## Deployment

### Cloudflare Pages (Frontend)
1. Connect your GitHub repository to Cloudflare Pages
2. Set build command: `npm run build`
3. Set build output directory: `build`

### Backend Deployment Options
1. **Railway** - Easy Python deployment
2. **Render** - Free tier available
3. **Heroku** - Traditional choice
4. **Vercel** - Serverless functions

## API Endpoints

- `GET /api/text/:id` - Get text content by ID
- `GET /api/translate` - Translate Chinese text to English
- `GET /api/pinyin` - Generate pinyin for Chinese text
- `GET /api/characters/:char` - Get character information

## Development Roadmap

### Phase 1: Basic Structure
- [ ] Set up React frontend with split-pane layout
- [ ] Create Flask backend with basic API endpoints
- [ ] Implement text display and sentence selection

### Phase 2: Core Features
- [ ] Add pinyin generation
- [ ] Implement English translation
- [ ] Create character-by-character analysis

### Phase 3: Enhanced Features
- [ ] Add navigation controls
- [ ] Implement character lookup
- [ ] Add text highlighting

### Phase 4: Polish & Deploy
- [ ] Improve UI/UX
- [ ] Add error handling
- [ ] Deploy to production



