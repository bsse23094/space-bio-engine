# 🚀 Space Biology Knowledge Engine

A comprehensive web application for exploring, searching, and visualizing space biology research data.

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The Space Biology Knowledge Engine is a full-stack web application that provides:

- **Backend**: FastAPI server with comprehensive REST API
- **Frontend**: Angular application with modern UI
- **Data Analysis**: 624+ space biology research articles
- **Visualizations**: Interactive charts, graphs, and network analysis
- **Search**: Advanced semantic search with AI-powered similarity

## 🚀 Quick Start

### One-Command Startup

#### Windows

```cmd
start_app.bat
```

#### Linux/Mac

```bash
./start_app.sh
```

That's it! The script will:

1. ✅ Set up virtual environment for backend
2. ✅ Install all dependencies
3. ✅ Start backend server (port 8000)
4. ✅ Start frontend server (port 4200)
5. ✅ Open the application in your browser

### Access the Application

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
