# 🚀 Space Biology Knowledge Engine - Backend

## Overview

A comprehensive FastAPI backend for the Space Biology Knowledge Engine, providing advanced search, visualization, and analysis capabilities for space biology research data.

## ✨ Features

### 🔍 Advanced Search

- **Semantic Search**: AI-powered similarity search using embeddings
- **Advanced Filtering**: Filter by topics, years, word count, journals, and more
- **Search Suggestions**: Real-time autocomplete functionality
- **Similarity Search**: Find related articles based on content similarity

### 📊 Interactive Visualizations

- **Topic Distribution**: Pie charts and bar charts showing research topics
- **Temporal Analysis**: Publication trends over time
- **Word Clouds**: Visual representation of key terms
- **Network Analysis**: Word co-occurrence and topic similarity networks
- **Comprehensive Statistics**: Dataset overview and insights

### 📄 Article Management

- **CRUD Operations**: Create, read, update, delete articles
- **Bulk Operations**: Efficient handling of large datasets
- **Metadata Extraction**: Automatic extraction of publication details

### 🎯 Frontend Integration

- **CORS Enabled**: Ready for web application integration
- **Detailed Documentation**: Comprehensive API docs with examples
- **Type Safety**: Pydantic models for request/response validation
- **Error Handling**: Consistent error responses

## 🏗️ Architecture

```
Backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── models/
│   │   └── article.py          # Pydantic data models
│   ├── routes/
│   │   ├── articles.py         # Article management endpoints
│   │   ├── data_exploration.py # Data exploration endpoints
│   │   ├── text_preprocessing.py # Text processing endpoints
│   │   ├── visualizations.py   # Visualization endpoints
│   │   └── enhanced_search.py  # Advanced search endpoints
│   ├── services/
│   │   ├── article_service.py  # Article business logic
│   │   ├── data_exploration_service.py # Data analysis logic
│   │   ├── text_preprocessing_service.py # Text processing logic
│   │   ├── visualization_service.py # Visualization data generation
│   │   └── enhanced_search_service.py # Search functionality
│   ├── database/
│   │   └── db.py              # Database connection and management
│   └── utils/
│       ├── nlp_utils.py        # NLP utility functions
│       └── text_cleaner.py    # Text cleaning utilities
├── requirements.txt            # Python dependencies
├── API_DOCUMENTATION.md       # Comprehensive API documentation
├── start.bat                   # Windows startup script
└── start.sh                    # Linux/Mac startup script
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Python 3.9+ recommended)
- **pip** (comes with Python)
- **Git** (for cloning the repository)

### 🎯 One-Click Startup

The easiest way to get started is using our automated startup scripts:

#### Windows Users

```cmd
# Navigate to Backend directory
cd Space-Biology-Knowledge-Engine\Backend

# Run the startup script
.\start.bat
# or
start.bat
```

#### Linux/Mac Users

```bash
# Navigate to Backend directory
cd Space-Biology-Knowledge-Engine/Backend

# Run the startup script
./start.sh
```

**⚠️ Important**: Make sure you're in the `Backend` directory when running these scripts!

**That's it!** The script will automatically:

- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Check data files
- ✅ Start the FastAPI server
- ✅ Open API documentation

### 📋 Manual Installation (Alternative)

If you prefer manual setup or the scripts don't work:

1. **Clone the repository**

```bash
git clone <repository-url>
cd Space-Biology-Knowledge-Engine/Backend
```

2. **Create virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Start the server**

```bash
# Method 1: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Method 2: Using Python module
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Method 3: Using Python directly
python app/main.py
```

### 🌐 Access the API

Once the server is running, you can access:

| Service                  | URL                                | Description            |
| ------------------------ | ---------------------------------- | ---------------------- |
| 📖 **API Documentation** | http://localhost:8000/docs         | Interactive Swagger UI |
| 📚 **Alternative Docs**  | http://localhost:8000/redoc        | ReDoc documentation    |
| ❤️ **Health Check**      | http://localhost:8000/health       | Server status          |
| 📊 **API Stats**         | http://localhost:8000/api/v1/stats | Usage statistics       |
| 🏠 **Root Endpoint**     | http://localhost:8000/             | API information        |

### 🔧 Troubleshooting Startup Issues

#### Common Issues and Solutions

**1. Python Not Found**

```bash
# Check Python installation
python --version
# or
python3 --version

# If not installed, download from: https://python.org
```

**2. Port Already in Use**

```bash
# Use a different port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Or kill the process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**3. Permission Denied (Linux/Mac)**

```bash
# Make script executable
chmod +x start.sh

# Or run with bash
bash start.sh
```

**4. Virtual Environment Issues**

```bash
# Delete and recreate virtual environment
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Then run startup script again
```

**5. Dependencies Installation Failed**

```bash
# Update pip first
pip install --upgrade pip

# Install dependencies one by one
pip install fastapi
pip install uvicorn
pip install pandas
pip install numpy
# ... continue with other packages
```

**6. Data Files Missing**

```bash
# Check if data files exist
ls -la ../datasets/  # Linux/Mac
dir ..\datasets\  # Windows

# The API will still work with limited functionality
```

**7. "No module named 'app'" Error**

```bash
# This happens when you're in the wrong directory
# Make sure you're in the Backend directory:
cd Space-Biology-Knowledge-Engine/Backend  # Linux/Mac
cd Space-Biology-Knowledge-Engine\Backend    # Windows

# Then run the startup script
./start.sh     # Linux/Mac
.\start.bat    # Windows
```

**8. Script Not Found Error**

```bash
# Make sure you're in the correct directory
pwd  # Linux/Mac - should show .../Backend
dir  # Windows - should show start.bat file

# If scripts are missing, you can start manually:
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 🚀 Production Deployment

For production deployment:

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn (Linux/Mac)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Or use Docker (recommended)
docker build -t space-bio-api .
docker run -p 8000:8000 space-bio-api
```

### 📱 Development Mode

For development with auto-reload:

```bash
# Start with debug logging
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# Start with specific log file
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-config logging.conf
```

## 📊 API Endpoints

### Core Endpoints

#### Articles

- `GET /api/v1/articles` - Get all articles (paginated)
- `GET /api/v1/articles/{id}` - Get article by ID
- `POST /api/v1/articles` - Create new article
- `PUT /api/v1/articles/{id}` - Update article
- `DELETE /api/v1/articles/{id}` - Delete article
- `GET /api/v1/articles/search` - Search articles

#### Enhanced Search

- `POST /api/v1/search/semantic` - Semantic similarity search
- `POST /api/v1/search/advanced` - Advanced search with filters
- `GET /api/v1/search/similar/{id}` - Find similar articles
- `GET /api/v1/search/suggestions` - Get search suggestions
- `GET /api/v1/search/filters` - Get available filters
- `GET /api/v1/search/trending` - Get trending topics

#### Visualizations

- `GET /api/v1/visualizations/topic-distribution` - Topic distribution data
- `GET /api/v1/visualizations/temporal-trends` - Publication trends over time
- `GET /api/v1/visualizations/word-cloud/{topic_id}` - Word cloud data
- `GET /api/v1/visualizations/network` - Network visualization data
- `GET /api/v1/visualizations/statistics` - Comprehensive statistics
- `GET /api/v1/visualizations/topics` - Topic information
- `GET /api/v1/visualizations/chart/{type}` - Generic chart data

### System Endpoints

- `GET /` - API information and status
- `GET /health` - Health check with data status
- `GET /api/v1/stats` - API usage statistics

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the Backend directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./space_bio.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True

# Data Paths
DATA_PATH=../../datasets/
EMBEDDINGS_PATH=../../datasets/embeddings.npy
METADATA_PATH=../../datasets/metadata.json

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### Data Requirements

The API expects the following data files in the `../datasets/` directory (relative to Backend folder):

- `sb_publications_clean.csv` - Main publications dataset
- `topics.csv` - Topic modeling results
- `embeddings.npy` - Pre-computed embeddings
- `metadata.json` - Additional metadata

## 📱 Frontend Integration

### React.js Example

```javascript
// Fetch topic distribution
const fetchTopicDistribution = async () => {
  const response = await fetch("/api/v1/visualizations/topic-distribution");
  const data = await response.json();
  return data;
};

// Semantic search
const searchArticles = async (query) => {
  const response = await fetch("/api/v1/search/semantic", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: query,
      limit: 10,
      similarity_threshold: 0.7,
    }),
  });
  return await response.json();
};
```

### Vue.js Example

```javascript
// Vue component
export default {
  data() {
    return {
      articles: [],
      loading: false,
    };
  },
  async mounted() {
    await this.loadArticles();
  },
  methods: {
    async loadArticles() {
      this.loading = true;
      const response = await fetch("/api/v1/articles?limit=20");
      this.articles = await response.json();
      this.loading = false;
    },
  },
};
```

## 🧪 Testing

### 🎯 Automated API Testing

We provide automated test scripts to verify all API endpoints are working correctly:

#### Windows Users

```cmd
# Run the test script
test_api.bat
```

#### Linux/Mac Users

```bash
# Run the test script
./test_api.sh
```

**The test script will automatically:**

- ✅ Check if the server is running
- ✅ Test all basic endpoints (health, docs, etc.)
- ✅ Test all API endpoints (articles, search, visualizations)
- ✅ Test POST endpoints (semantic search, advanced search)
- ✅ Provide a comprehensive test report

### 📋 Manual Testing

#### Run Unit Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_articles.py

# Run with coverage
pytest --cov=app tests/
```

#### Test API Endpoints Manually

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test article search
curl "http://localhost:8000/api/v1/articles/search?q=microgravity&limit=5"

# Test semantic search
curl -X POST "http://localhost:8000/api/v1/search/semantic" \
  -H "Content-Type: application/json" \
  -d '{"query": "space biology", "limit": 10}'

# Test visualization endpoints
curl "http://localhost:8000/api/v1/visualizations/topic-distribution"
curl "http://localhost:8000/api/v1/visualizations/statistics"
```

### 🔍 Browser Testing

You can also test the API directly in your browser:

1. **Open API Documentation**: http://localhost:8000/docs
2. **Try the interactive endpoints** in the Swagger UI
3. **Test different parameters** and see real responses
4. **Check the health endpoint**: http://localhost:8000/health

### 📊 Expected Test Results

When running the automated tests, you should see:

```
🧪 Testing Space Biology Knowledge Engine Backend...
[PASS] Server is running!
🔍 Testing Basic Endpoints...
[PASS] Root endpoint - Status: 200
[PASS] Health check - Status: 200
[PASS] API documentation - Status: 200
📊 Testing API Endpoints...
[PASS] API statistics - Status: 200
[PASS] Get articles - Status: 200
[PASS] Topic distribution - Status: 200
🔎 Testing Search Endpoints...
[PASS] Article search - Status: 200
[PASS] Search suggestions - Status: 200
📝 Testing POST Endpoints...
[PASS] Semantic search - Status: 200
[PASS] Advanced search - Status: 200
🎯 Test Summary:
[PASS] Backend API is working correctly!
[SUCCESS] Backend testing completed successfully! 🚀
```

## 📊 Data Models

### Article Model

```python
class Article(BaseModel):
    id: Optional[int] = None
    title: str
    link: Optional[str] = None
    text: Optional[str] = None
    clean_text: Optional[str] = None
    word_count: Optional[int] = None
    topic: Optional[int] = None
    year: Optional[int] = None
    authors: List[str] = []
    journal: Optional[str] = None
    # ... additional fields
```

### Search Request Models

```python
class AdvancedSearchRequest(BaseModel):
    query: str
    filters: Optional[SearchFilters] = None
    limit: int = 10
    similarity_threshold: Optional[float] = None
    sort_by: str = "relevance"
```

## 🔍 Search Capabilities

### Semantic Search

- Uses pre-computed embeddings for similarity
- More accurate than keyword matching
- Supports similarity thresholds

### Advanced Filtering

- **Topics**: Filter by LDA topic clusters
- **Years**: Filter by publication year range
- **Word Count**: Filter by article length
- **Journals**: Filter by journal name
- **Article Types**: Filter by research type

### Search Suggestions

- Real-time autocomplete
- Based on article titles and content
- Configurable suggestion limits

## 📈 Visualization Features

### Chart Types Supported

- **Pie Charts**: Topic distribution
- **Bar Charts**: Article counts, word distributions
- **Line Charts**: Temporal trends
- **Scatter Plots**: Word count vs year analysis
- **Histograms**: Word count distributions
- **Network Graphs**: Word co-occurrence networks

### Data Export

- JSON format for frontend consumption
- CSV export for external analysis
- Configurable data subsets

## 🚀 Performance Optimization

### Caching Strategy

- Cache static data (topics, statistics)
- Implement Redis for production
- Client-side caching recommendations

### Database Optimization

- Indexed search fields
- Efficient pagination
- Query optimization

### API Performance

- Response time monitoring
- Rate limiting (production)
- Connection pooling

## 🔐 Security

### CORS Configuration

- Configurable allowed origins
- Production-ready CORS settings

### Data Privacy

- No personal data storage
- Public research data only
- Secure API endpoints

## 📝 API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Documentation Features

- Detailed endpoint descriptions
- Request/response examples
- Frontend integration notes
- Error code explanations

## 🐛 Troubleshooting

### Common Issues

#### Data Files Not Found

```bash
# Check if data files exist
ls -la ../../datasets/

# Verify file paths in configuration
```

#### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Port Already in Use

```bash
# Use different port
uvicorn app.main:app --port 8001
```

### Debug Mode

```bash
# Enable debug logging
export DEBUG=True
python -m uvicorn app.main:app --reload --log-level debug
```

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create feature branch
3. Install development dependencies
4. Run tests
5. Submit pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings
- Write tests for new features

## 📄 License

MIT License - see LICENSE file for details.

## 📞 Support

- **Documentation**: `/docs` endpoint
- **Issues**: GitHub Issues
- **Email**: contact@spacebio-engine.com

---

_Built with FastAPI, designed for easy frontend integration and comprehensive space biology research analysis._
