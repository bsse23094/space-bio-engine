# 🚀 Space Biology Knowledge Engine

[![GitHub Pages](https://img.shields.io/badge/demo-live-brightgreen)](https://bsse23094.github.io/space-bio-engine)
[![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![Angular](https://img.shields.io/badge/angular-18-red)](https://angular.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A state-of-the-art web application for exploring, searching, and visualizing NASA space biology research data. Built with modern web technologies and powered by advanced semantic search algorithms.

![Dashboard Preview](docs/dashboard-preview.png)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The **Space Biology Knowledge Engine** is a comprehensive research platform that provides scientists, researchers, and space enthusiasts with powerful tools to explore over **624 curated space biology publications** from NASA's Open Science Data Repository. 

### Key Capabilities

- **🔍 Semantic Search**: TF-IDF powered search engine with cosine similarity ranking
- **📊 Data Visualization**: Interactive charts showing temporal trends, topic distributions, and research statistics
- **📚 Article Management**: Browse, filter, and explore research articles with rich metadata
- **🎨 Modern UI**: Sleek, minimal design with smooth animations and responsive layout
- **⚡ Fast Performance**: Optimized backend with singleton service pattern and efficient data loading
- **🌐 RESTful API**: Comprehensive FastAPI backend with automatic documentation

## ✨ Features

### Dashboard
- **Real-time Statistics**: Total articles, topics coverage, and research metrics
- **Topic Distribution**: Visual breakdown of research areas (Plant Biology, Microbiology, Bone & Muscle, etc.)
- **Temporal Trends**: Line chart showing publication trends over time with smooth animations
- **Quick Access**: Direct navigation to articles and search functionality

### Search Engine
- **Semantic Search**: Find articles based on meaning, not just keywords
- **Result Ranking**: Articles ranked by relevance using TF-IDF vectorization
- **Rich Metadata**: View titles, authors, publication years, topics, and journal information
- **Direct Links**: Quick access to original PubMed Central articles

### Articles Browser
- **Paginated Display**: Efficient loading of large datasets
- **Numbered Cards**: Elegant card-based layout with fade-in animations
- **Full Metadata**: Access complete article information including abstracts and keywords
- **External Links**: One-click access to source articles

### Visualizations
- **Interactive Charts**: Built with Chart.js for smooth, responsive visualizations
- **Word Clouds**: Topic-based word clouds for visual exploration
- **Network Analysis**: Explore relationships between research topics and themes


## 🎬 Demo

**Live Demo**: [https://bsse23094.github.io/space-bio-engine](https://bsse23094.github.io/space-bio-engine)

**API Documentation**: [Backend API Docs](https://your-backend-url.onrender.com/docs)

## 🚀 Quick Start

### Prerequisites
- **Python 3.13+** (Backend)
- **Node.js 18+** (Frontend)
- **npm 9+** (Package manager)

### One-Command Startup

#### Windows

```cmd
start_app.bat
```

#### Linux/Mac

```bash
chmod +x start_app.sh
./start_app.sh
```

The startup script will automatically:

1. ✅ Create Python virtual environment
2. ✅ Install backend dependencies
3. ✅ Install frontend dependencies  
4. ✅ Start backend server on `http://localhost:8000`
5. ✅ Start frontend server on `http://localhost:4200`
6. ✅ Open application in your default browser

### Access Points

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Angular Frontend                     │
│              (Port 4200 - Development)                  │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐   │
│  │Dashboard │  │  Search  │  │  Articles Browser  │   │
│  └──────────┘  └──────────┘  └────────────────────┘   │
│         │              │                 │              │
│         └──────────────┴─────────────────┘              │
│                        │                                │
│                   API Service                           │
└────────────────────────┼────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                        │
│              (Port 8000 - API Server)                   │
│  ┌──────────────┐  ┌─────────────────────────────┐    │
│  │   Routes     │  │    Services                  │    │
│  │ ─────────    │  │ ────────────                 │    │
│  │ /articles    │  │ EnhancedSearchService        │    │
│  │ /search      │  │ VisualizationService         │    │
│  │ /visual      │  │ ArticleService               │    │
│  └──────────────┘  └─────────────────────────────┘    │
│                              │                          │
│                              ▼                          │
│  ┌────────────────────────────────────────────────┐   │
│  │         Data Layer                              │   │
│  │  ─────────────────                              │   │
│  │  • CSV: 624 Articles (datasets/)                │   │
│  │  • Embeddings: 384-dim vectors (artifacts/)     │   │
│  │  • TF-IDF Matrix: 1000 features                 │   │
│  │  • Topics: 8 research categories                │   │
│  └────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Interaction** → Angular Frontend receives input
2. **API Request** → HTTP request sent to FastAPI backend
3. **Service Processing** → Backend services process data using:
   - TF-IDF vectorization for semantic search
   - Pandas DataFrames for data manipulation
   - Scikit-learn for similarity calculations
4. **Response** → JSON data returned to frontend
5. **Rendering** → Angular components display results with Chart.js visualizations

## 🛠️ Technology Stack

### Frontend
- **Framework**: Angular 18 (Standalone Components)
- **Language**: TypeScript 5.5+
- **Styling**: SCSS with custom design system
- **Charts**: Chart.js 4.x
- **HTTP Client**: Angular HttpClient with RxJS
- **Fonts**: Elms Sans, Syncopate
- **Icons**: Material Symbols Outlined

### Backend
- **Framework**: FastAPI 0.100+
- **Language**: Python 3.13
- **Data Processing**: 
  - Pandas 2.x (Data manipulation)
  - NumPy (Numerical operations)
- **Machine Learning**:
  - Scikit-learn (TF-IDF, cosine similarity)
- **Server**: Uvicorn (ASGI server)
- **Validation**: Pydantic v2

### Database & Storage
- **Articles**: CSV (624 publications)
- **Embeddings**: NumPy binary format (.npy)
- **Metadata**: JSON
- **Topics**: CSV with keywords

### DevOps
- **Version Control**: Git + GitHub
- **Frontend Hosting**: GitHub Pages
- **Backend Hosting**: Render.com / Railway.app
- **CI/CD**: GitHub Actions### Access the Application

Once started, you can access:

- **Web Application**: http://localhost:4200
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health
- **API Stats**: http://localhost:8000/api/v1/stats

## 🏗️ Architecture

```
Space-Biology-Knowledge-Engine/
├── Backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py          # API entry point
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   └── models/          # Data models
│   └── requirements.txt     # Python dependencies
│
├── Frontend/                # Angular frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── features/    # Feature modules
│   │   │   └── core/        # Core services
│   │   └── environments/    # Environment configs
│   └── package.json         # NPM dependencies
│
├── datasets/                # Research data
│   ├── sb_publications_clean.csv
│   ├── topics.csv
│   ├── embeddings.npy
│   └── metadata.json
│
├── start_app.bat            # Windows startup script
└── start_app.sh             # Linux/Mac startup script
```

## ✨ Features

### Backend Features

- 📊 **Comprehensive REST API**
  - Article management (CRUD operations)
  - Advanced search with filters
  - Semantic similarity search
  - Visualization data endpoints
- 🔍 **Search Capabilities**
  - Keyword search
  - Semantic embedding search
  - Advanced filtering (topics, years, word count)
  - Search suggestions and autocomplete
- 📈 **Visualization Data**
  - Topic distribution
  - Temporal trends analysis
  - Word cloud generation
  - Network visualizations
  - Comprehensive statistics

### Frontend Features

- 🎨 **Modern Angular UI**
  - Responsive design
  - Interactive dashboard
  - Real-time search
- 📊 **Data Visualization**
  - Charts and graphs
  - Topic distribution
  - Publication trends
- 🔎 **Search Interface**
  - Advanced filters
  - Real-time results
  - Article details

## 📦 Requirements

### Backend

- Python 3.8+ (Python 3.9+ recommended)
- pip
- Virtual environment support

### Frontend

- Node.js 16+ (with npm)
- Angular CLI 20+

### Data

- Space biology research dataset (included in `datasets/` directory)

## 💻 Installation

### Automatic Installation (Recommended)

Run the startup script - it handles everything:

```cmd
# Windows
start_app.bat

# Linux/Mac
./start_app.sh
```

### Manual Installation

#### 1. Backend Setup

```bash
cd Backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Frontend Setup

```bash
cd Frontend

# Install dependencies
npm install
```

## 🎯 Running the Application

### Method 1: One-Command Startup (Easiest)

**Windows:**

```cmd
start_app.bat
```

**Linux/Mac:**

```bash
./start_app.sh
```

### Method 2: Manual Startup

#### Start Backend

```bash
cd Backend
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Frontend (in a new terminal)

```bash
cd Frontend
npm start
```

### Method 3: Individual Components

**Backend Only:**

```bash
cd Backend
.\start.bat  # Windows
./start.sh   # Linux/Mac
```

**Frontend Only:**

```bash
cd Frontend
npm start
```

## 📖 API Documentation

### Interactive API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key API Endpoints

#### Articles

- `GET /api/v1/articles` - Get all articles (paginated)
- `GET /api/v1/articles/{id}` - Get specific article
- `GET /api/v1/articles/search` - Search articles

#### Search

- `POST /api/v1/search/semantic` - Semantic similarity search
- `POST /api/v1/search/advanced` - Advanced search with filters
- `GET /api/v1/search/suggestions` - Search suggestions

#### Visualizations

- `GET /api/v1/visualizations/topic-distribution` - Topic distribution data
- `GET /api/v1/visualizations/temporal-trends` - Publication trends
- `GET /api/v1/visualizations/statistics` - Comprehensive statistics
- `GET /api/v1/visualizations/word-cloud/{topic_id}` - Word cloud data

For complete API documentation, see [Backend/API_DOCUMENTATION.md](Backend/API_DOCUMENTATION.md)

## 🔧 Configuration

### Backend Configuration

Edit `Backend/app/config.py` or use environment variables:

```bash
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True
```

### Frontend Configuration

Edit `Frontend/src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiBase: "http://localhost:8000/api/v1",
};
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Backend Port Already in Use

```bash
# Check what's using port 8000
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -ti:8000

# Kill the process or use a different port
python -m uvicorn app.main:app --reload --port 8001
```

#### 2. Frontend Port Already in Use

```bash
# Angular will automatically try the next available port
# Or specify a custom port:
ng serve --port 4201
```

#### 3. Module Not Found Errors (Backend)

```bash
cd Backend
.venv\Scripts\activate
pip install -r requirements.txt --force-reinstall
```

#### 4. Dependencies Installation Failed (Frontend)

```bash
cd Frontend
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 5. Data Files Missing

The application needs these files in the `datasets/` directory:

- `sb_publications_clean.csv`
- `topics.csv`
- `embeddings.npy`
- `metadata.json`

If missing, the API will still work but with limited functionality.

#### 6. CORS Errors

Make sure the backend is running before starting the frontend. The frontend is configured to proxy API requests to the backend.

#### 7. Virtual Environment Issues

```bash
# Delete and recreate virtual environment
cd Backend
rm -rf .venv  # Linux/Mac
rmdir /s .venv  # Windows

# Then run the startup script again
```

### Getting Help

1. **Check Backend Health**: http://localhost:8000/health
2. **Check Backend Logs**: Look at the backend terminal window
3. **Check Frontend Console**: Open browser DevTools (F12)
4. **API Documentation**: http://localhost:8000/docs

## 📊 Data Overview

The application includes analysis of:

- **Total Articles**: 624+ space biology research publications
- **Topics Identified**: 9 distinct research topics via LDA analysis
- **Year Range**: 1990-2024
- **Features**:
  - Topic modeling and clustering
  - Temporal trend analysis
  - Word co-occurrence networks
  - Semantic similarity search

## 🚀 Development

### Backend Development

```bash
cd Backend
.venv\Scripts\activate
python -m uvicorn app.main:app --reload --log-level debug
```

### Frontend Development

```bash
cd Frontend
ng serve --open
```

### Running Tests

**Backend:**

```bash
cd Backend
pytest
```

**Frontend:**

```bash
cd Frontend
ng test
```

## 🌐 Deployment

### Frontend Deployment (GitHub Pages)

#### Prerequisites
- GitHub repository set up
- GitHub Pages enabled in repository settings

#### Steps

1. **Build for Production**
```bash
cd Frontend
npm run build -- --configuration production --base-href /space-bio-engine/
```

2. **Deploy to GitHub Pages**
```bash
# Install Angular CLI globally if needed
npm install -g @angular/cli

# Deploy using Angular CLI
ng deploy --base-href=/space-bio-engine/
```

Or manually:
```bash
# Install gh-pages
npm install -g angular-cli-ghpages

# Deploy
npx angular-cli-ghpages --dir=dist/frontend/browser
```

3. **Access Your Site**
- URL: `https://[username].github.io/space-bio-engine`
- Example: `https://bsse23094.github.io/space-bio-engine`

#### GitHub Pages Configuration
- **Source**: Deploy from `gh-pages` branch
- **Custom Domain**: Optional
- **Enforce HTTPS**: Recommended

### Backend Deployment (Render.com - Free Tier)

#### Prerequisites
- Render.com account (free)
- GitHub repository connected

#### Steps

1. **Create `render.yaml`** (if not exists)
```yaml
services:
  - type: web
    name: space-bio-backend
    env: python
    buildCommand: pip install -r Backend/requirements.txt
    startCommand: cd Backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.13.0
```

2. **Deploy on Render.com**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Select "New Web Service"
   - Choose your repository
   - Configure:
     - **Name**: `space-bio-backend`
     - **Environment**: Python 3
     - **Build Command**: `pip install -r Backend/requirements.txt`
     - **Start Command**: `cd Backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - **Plan**: Free

3. **Environment Variables**
   - `PYTHON_VERSION`: 3.13.0
   - `PORT`: Auto-assigned by Render

4. **Access Your API**
   - URL: `https://space-bio-backend.onrender.com`
   - Docs: `https://space-bio-backend.onrender.com/docs`

#### Alternative: Railway.app

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
railway login
```

2. **Deploy**
```bash
cd Backend
railway init
railway up
```

3. **Set Environment**
```bash
railway variables set PYTHON_VERSION=3.13.0
```

#### Update Frontend API URL

After backend deployment, update the frontend API endpoint:

**File**: `Frontend/src/environments/environment.prod.ts`
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://space-bio-backend.onrender.com/api/v1'
};
```

Rebuild and redeploy frontend after changing API URL.

### CORS Configuration

Ensure backend allows frontend domain:

**File**: `Backend/app/main.py`
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bsse23094.github.io",
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Continuous Deployment

#### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install and Build
        run: |
          cd Frontend
          npm ci
          npm run build -- --configuration production
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./Frontend/dist/frontend/browser
```

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📞 Support

- **Backend Documentation**: `Backend/README.md`
- **API Documentation**: `Backend/API_DOCUMENTATION.md`
- **Frontend Documentation**: `Frontend/README.md`

---

**Built with ❤️ for space biology research**

_FastAPI + Angular + Python + TypeScript_
