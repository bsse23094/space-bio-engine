"""
Space Biology Knowledge Engine - FastAPI Backend
Main API entry point with comprehensive research integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
import os

from app.routes.articles_simple import router as articles_router
from app.routes.data_exploration import router as data_exploration_router
from app.routes.text_preprocessing import router as text_preprocessing_router
from app.routes.visualizations import router as visualizations_router
from app.routes.enhanced_search import router as enhanced_search_router
from app.config import settings

# Initialize FastAPI app with comprehensive documentation
app = FastAPI(
    title="Space Biology Knowledge Engine API",
    description="""
    ## 🚀 Space Biology Knowledge Engine API
    
    A comprehensive API for searching, analyzing, and visualizing space biology research articles.
    
    ### 🔍 Key Features:
    - **Semantic Search**: Find articles using AI-powered semantic similarity
    - **Advanced Filtering**: Filter by topics, years, word count, and more
    - **Interactive Visualizations**: Charts, graphs, word clouds, and network analysis
    - **Topic Analysis**: LDA-based topic modeling and clustering
    - **Temporal Analysis**: Publication trends and research evolution over time
    
    ### 📊 Research Integration:
    - Based on comprehensive analysis of 624+ space biology publications
    - 9 distinct research topics identified through LDA analysis
    - Temporal trends from 1990-2024
    - Word co-occurrence networks and topic similarity analysis
    
    ### 🎯 Frontend Integration:
    - All endpoints designed for easy frontend consumption
    - Detailed response schemas with frontend usage notes
    - CORS enabled for web application integration
    - Interactive documentation with examples
    
    ### 📈 Visualization Endpoints:
    - Topic distribution charts
    - Temporal trend analysis
    - Word cloud generation
    - Network visualizations
    - Comprehensive statistics
    
    ### 🔎 Search Capabilities:
    - Keyword search
    - Semantic similarity search
    - Advanced filtering
    - Search suggestions
    - Trending topics analysis
    """,
    version="2.0.0",
    contact={
        "name": "Space Biology Knowledge Engine",
        "email": "contact@spacebio-engine.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Local development
        "https://bsse23094.github.io",  # GitHub Pages production
        "https://*.onrender.com",  # Render.com deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers with comprehensive API organization
app.include_router(articles_router, prefix="/api/v1", tags=["📄 Articles"])
app.include_router(data_exploration_router, prefix="/api/v1", tags=["🔍 Data Exploration"])
app.include_router(text_preprocessing_router, prefix="/api/v1", tags=["📝 Text Processing"])
app.include_router(visualizations_router, prefix="/api/v1", tags=["📊 Visualizations"])
app.include_router(enhanced_search_router, prefix="/api/v1", tags=["🔎 Enhanced Search"])

@app.get("/", tags=["🏠 Root"])
async def root():
    """
    Root endpoint with API information
    
    Frontend Integration:
    - Use for API health checks
    - Display API version and status
    - Link to documentation
    """
    return {
        "message": "🚀 Space Biology Knowledge Engine API",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Semantic Search",
            "Interactive Visualizations", 
            "Topic Analysis",
            "Temporal Trends",
            "Network Analysis"
        ],
        "docs": "/docs",
        "redoc": "/redoc",
        "research_data": {
            "total_articles": "624+",
            "topics_identified": 9,
            "year_range": "1990-2024",
            "analysis_complete": True
        }
    }

@app.get("/health", tags=["🏠 Root"])
async def health_check():
    """
    Comprehensive health check endpoint
    
    Frontend Integration:
    - Use for monitoring API status
    - Check service availability
    - Display system status
    """
    try:
        # Check if data files exist
        data_files = [
            "../datasets/sb_publications_clean.csv",
            "../datasets/topics.csv",
            "../datasets/embeddings.npy"
        ]
        
        missing_files = []
        for file_path in data_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        status = "healthy" if not missing_files else "degraded"
        
        return {
            "status": status,
            "service": "space-bio-api",
            "version": "2.0.0",
            "data_status": {
                "publications_data": "available" if os.path.exists(data_files[0]) else "missing",
                "topics_data": "available" if os.path.exists(data_files[1]) else "missing", 
                "embeddings_data": "available" if os.path.exists(data_files[2]) else "missing"
            },
            "missing_files": missing_files,
            "features_enabled": {
                "semantic_search": len(missing_files) == 0,
                "visualizations": len(missing_files) == 0,
                "topic_analysis": os.path.exists(data_files[1]),
                "basic_search": True
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "space-bio-api",
            "error": str(e)
        }

@app.get("/api/v1/stats", tags=["📊 Visualizations"])
async def get_api_stats():
    """
    Get API usage statistics and system information
    
    Frontend Integration:
    - Use for admin dashboard
    - Display system metrics
    - Monitor API performance
    """
    try:
        import pandas as pd
        
        # Load basic stats
        df_path = "../datasets/sb_publications_clean.csv"
        if not os.path.exists(df_path):
            df_path = "datasets/sb_publications_clean.csv"
            
        if os.path.exists(df_path):
            df = pd.read_csv(df_path)
            
            # Extract year if not present
            if 'year' not in df.columns and 'link' in df.columns:
                df['year'] = df['link'].str.extract(r'(\d{4})')
                df['year'] = pd.to_numeric(df['year'], errors='coerce')
                df['year'] = df['year'].where((df['year'] >= 1990) & (df['year'] <= 2024))
            
            stats = {
                "total_articles": len(df),
                "articles_with_topics": len(df[df['topic'].notna() & (df['topic'] != -1)]) if 'topic' in df.columns else 0,
                "articles_with_year": len(df[df['year'].notna()]) if 'year' in df.columns else 0,
                "unique_topics": int(df['topic'].nunique() - (1 if -1 in df['topic'].values else 0)) if 'topic' in df.columns else 0,
                "average_word_count": float(df['word_count'].mean()) if 'word_count' in df.columns and df['word_count'].notna().any() else 0,
                "year_range": {
                    "min": int(df['year'].min()) if 'year' in df.columns and df['year'].notna().any() else None,
                    "max": int(df['year'].max()) if 'year' in df.columns and df['year'].notna().any() else None
                }
            }
        else:
            stats = {"error": "Data files not available"}
        
        return {
            "api_version": "2.0.0",
            "data_statistics": stats,
            "endpoints": {
                "articles": "/api/v1/articles",
                "visualizations": "/api/v1/visualizations",
                "search": "/api/v1/search",
                "data_exploration": "/api/v1/data-exploration"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
