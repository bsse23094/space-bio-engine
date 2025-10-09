# Space Biology Knowledge Engine - Quick Start Guide

## 🚀 How to Run the Application

### 1. Quick Start (Recommended)

Simply double-click or run:

```cmd
start_app.bat
```

This will:

- ✅ Start the backend API server
- ✅ Start the frontend web application
- ✅ Open your browser automatically

**That's it!** 🎉

### 2. What You'll See

After running the script, two command windows will open:

**Window 1: Backend Server**

```
Starting FastAPI server...
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete
```

**Window 2: Frontend Server**

```
** Angular Live Development Server is listening on localhost:4200
√ Compiled successfully.
```

### 3. Access the Application

The application will automatically open in your browser at:
**http://localhost:4200**

If it doesn't open automatically, just click the link above or manually navigate to it.

### 4. Additional URLs

- **Backend API Docs**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health
- **API Statistics**: http://localhost:8000/api/v1/stats

### 5. Stopping the Application

Simply close both command windows (Backend and Frontend).

Or press `Ctrl+C` in each window.

### 6. Troubleshooting

If you encounter any issues:

1. **Run the verification script**:

   ```cmd
   verify_setup.bat
   ```

2. **Check ports**:

   - Backend uses port 8000
   - Frontend uses port 4200
   - Make sure these ports are not in use

3. **Reinstall dependencies**:
   ```cmd
   cd Backend
   rmdir /s .venv
   cd ..\Frontend
   rmdir /s node_modules
   cd ..
   start_app.bat
   ```

### 7. Manual Startup (Alternative)

If you prefer to start services separately:

**Backend:**

```cmd
cd Backend
start.bat
```

**Frontend:**

```cmd
cd Frontend
npm start
```

---

## 📁 Project Structure

```
Space-Biology-Knowledge-Engine/
├── start_app.bat        ← Run this to start everything!
├── verify_setup.bat     ← Check if system is ready
├── Backend/             ← FastAPI server
├── Frontend/            ← Angular application
└── datasets/            ← Research data
```

## 🎯 First Time Setup

The startup script handles everything automatically, but if needed:

1. Python 3.8+ must be installed
2. Node.js 16+ must be installed
3. Run `start_app.bat`
4. Wait for dependencies to install (first time only)
5. Application opens in browser

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Check `Backend/README.md` for backend-specific help
- Check `Backend/API_DOCUMENTATION.md` for API details

---

**Enjoy exploring space biology research!** 🚀🔬
