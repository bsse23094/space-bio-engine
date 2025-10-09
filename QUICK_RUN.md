# 🚀 Quick Run Guide - Space Biology Knowledge Engine

This guide provides the fastest way to get the Space Biology Knowledge Engine up and running.

## Prerequisites

- **Python 3.8+** installed
- **Node.js** and **npm** installed
- **Git** (for cloning the repository)

## 🎯 Quick Start (Recommended)

### Windows Users

Simply double-click or run:
```cmd
start_app.bat
```

### Linux/Mac Users

Run:
```bash
./start_app.sh
```

That's it! The application will:
1. ✅ Set up the backend virtual environment
2. ✅ Install all Python dependencies
3. ✅ Install all Node.js dependencies
4. ✅ Start the backend server (port 8000)
5. ✅ Start the frontend server (port 4200)
6. ✅ Open your browser automatically

---

## 📋 Manual Setup (Alternative)

If you prefer to run each component separately:

### Step 1: Install Backend Dependencies

```bash
cd Backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

```bash
cd Frontend
npm install
```

### Step 3: Start Backend Server

```bash
cd Backend
# Windows
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Linux/Mac
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Wait for: `INFO: Application startup complete.`

### Step 4: Start Frontend Server (New Terminal)

```bash
cd Frontend
npm start
```

Wait for: `Compiled successfully.`

---

## 🌐 Access the Application

Once both servers are running:

- **🌍 Web Application**: http://localhost:4200
- **📖 API Documentation**: http://localhost:8000/docs
- **📚 Alternative API Docs**: http://localhost:8000/redoc
- **❤️ Health Check**: http://localhost:8000/health
- **📊 API Statistics**: http://localhost:8000/api/v1/stats

---

## 🛠️ Troubleshooting

### Backend Won't Start

1. Make sure Python 3.8+ is installed: `python --version`
2. Make sure virtual environment is activated
3. Reinstall dependencies: `pip install -r requirements.txt`
4. Check if port 8000 is already in use

### Frontend Won't Start

1. Make sure Node.js is installed: `node --version`
2. Clear npm cache: `npm cache clean --force`
3. Delete `node_modules` and reinstall: 
   ```bash
   rm -rf node_modules
   npm install
   ```
4. Check if port 4200 is already in use

### Port Already in Use

**Backend (Port 8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Frontend (Port 4200):**
```bash
# Windows
netstat -ano | findstr :4200
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:4200 | xargs kill -9
```

---

## 📦 What's Included

### Backend Features
- FastAPI REST API
- 624+ space biology research articles
- Semantic search with AI embeddings
- Interactive visualizations
- Advanced filtering

### Frontend Features
- Angular 20 application
- Modern responsive UI
- Interactive charts and graphs
- Real-time search
- Network visualizations

---

## 🔄 Development Mode

Both servers run in development mode with hot-reload enabled:
- Backend: Changes to Python files auto-reload the server
- Frontend: Changes to TypeScript/HTML/CSS rebuild automatically

---

## 🎓 Next Steps

1. Explore the API documentation at http://localhost:8000/docs
2. Try the search functionality
3. Browse visualizations
4. Check out the network analysis
5. Read the full documentation in `README.md`

---

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Review `Backend/API_DOCUMENTATION.md` for API details
- Verify setup with `verify_setup.bat` (Windows)

---

**Enjoy exploring space biology research! 🚀🔬**
