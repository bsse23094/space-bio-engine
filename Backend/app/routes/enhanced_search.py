"""
Enhanced Search API routes for Space Biology Knowledge Engine
Provides semantic search, advanced filtering, and similarity search capabilities
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Body
from typing import List, Optional, Dict, Any
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

from app.models.article import (
    Article, ArticleSearchResponse, SimilarityResult,
    AdvancedSearchRequest, EmbeddingSearchRequest, SearchFilters
)
from app.services.enhanced_search_service import EnhancedSearchService

router = APIRouter()

# Dependency to get enhanced search service
def get_search_service():
    return EnhancedSearchService()

@router.post("/search/semantic", response_model=ArticleSearchResponse)
async def semantic_search(
    search_request: EmbeddingSearchRequest = Body(...),
    search_service: EnhancedSearchService = Depends(get_search_service)
):
    """
    Perform semantic search using embeddings
    
    Frontend Integration:
    - Use for "Find Similar" functionality
    - More accurate than keyword search
    - Returns articles semantically similar to query
    
    Request Body:
    {
        "query": "microgravity effects on bone",
        "limit": 10,
        "similarity_threshold": 0.7,
        "use_embeddings": true
    }
    
    Response:
    {
        "articles": [...],
        "total_count": 15,
        "query": "microgravity effects on bone",
        "search_time_ms": 45.2
    }
    """
    try:
        results = await search_service.semantic_search(search_request)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Semantic search error: {str(e)}")

@router.post("/search/advanced", response_model=ArticleSearchResponse)
async def advanced_search(
    search_request: AdvancedSearchRequest = Body(...),
    search_service: EnhancedSearchService = Depends(get_search_service)
):
    """
    Perform advanced search with multiple filters
    
    Frontend Integration:
    - Use for advanced search forms
    - Multiple filter options
    - Sorting capabilities
    
    Request Body:
    {
        "query": "space biology",
        "filters": {
            "topics": [0, 1, 2],
            "years": [2020, 2021, 2022],
            "min_word_count": 10,
            "max_word_count": 50
        },
        "limit": 20,
        "sort_by": "relevance"
    }
    """
    try:
        results = await search_service.advanced_search(search_request)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Advanced search error: {str(e)}")

@router.get("/search/similar/{article_id}", response_model=List[SimilarityResult])
async def find_similar_articles(
    article_id: int,
    limit: int = Query(5, ge=1, le=20),
    threshold: float = Query(0.7, ge=0.0, le=1.0),
    search_service: EnhancedSearchService = Depends(get_search_service)
):
    """
    Find articles similar to a specific article
    
    Frontend Integration:
    - "Related Articles" section
    - Article detail page recommendations
    - Similarity scores for ranking
    
    Parameters:
    - article_id: ID of the reference article
    - limit: Maximum number of similar articles
    - threshold: Minimum similarity score
    
    Example Response:
    [
        {
            "article": {...},
            "similarity_score": 0.85,
            "matched_terms": ["microgravity", "bone", "spaceflight"]
        }
    ]
    """
    try:
        similar_articles = await search_service.find_similar_articles(
            article_id, limit, threshold
        )
        return similar_articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similarity search error: {str(e)}")

@router.get("/search/suggestions")
async def get_search_suggestions(
    query: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=20),
    search_service: EnhancedSearchService = Depends(get_search_service)
):
    """
    Get search suggestions based on partial query
    
    Frontend Integration:
    - Autocomplete functionality
    - Search suggestions dropdown
    - Real-time suggestions as user types
    
    Parameters:
    - query: Partial search query
    - limit: Maximum number of suggestions
    
    Example Response:
    {
        "suggestions": [
            "microgravity effects",
            "microgravity bone loss",
            "microgravity muscle atrophy"
        ],
        "query": "micrograv"
    }
    """
    try:
        suggestions = await search_service.get_search_suggestions(query, limit)
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Suggestions error: {str(e)}")

@router.get("/search/filters")
async def get_search_filters(
    search_service: EnhancedSearchService = Depends(get_search_service)
):
    """
    Get available search filters and their options
    
    Frontend Integration:
    - Populate filter dropdowns
    - Show available options
    - Filter counts for each option
    
    Example Response:
    {
        "topics": [
            {"id": 0, "name": "Spaceflight Research", "count": 146},
            {"id": 1, "name": "Plant Biology", "count": 89}
        ],
        "years": [
            {"year": 2020, "count": 45},
            {"year": 2021, "count": 52}
        ],
        "journals": [
            {"name": "Nature", "count": 23},
            {"name": "Science", "count": 18}
        ]
    }
    """
    try:
        filters = await search_service.get_available_filters()
        return filters
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Filters error: {str(e)}")

@router.get("/search/trending")
async def get_trending_topics(
    time_period: str = Query("month", description="Time period: week, month, year"),
    limit: int = Query(10, ge=1, le=20),
    search_service: EnhancedSearchService = Depends(get_search_service)
):
    """
    Get trending topics and keywords
    
    Frontend Integration:
    - Trending topics widget
    - Popular searches display
    - Research trend analysis
    
    Parameters:
    - time_period: Analysis time period
    - limit: Maximum number of trending items
    
    Example Response:
    {
        "trending_topics": [
            {"topic": "microgravity", "count": 45, "growth": 12.5},
            {"topic": "space biology", "count": 38, "growth": 8.2}
        ],
        "trending_keywords": [
            {"keyword": "bone loss", "count": 23, "growth": 15.3}
        ],
        "time_period": "month"
    }
    """
    try:
        trending = await search_service.get_trending_topics(time_period, limit)
        return trending
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trending topics error: {str(e)}")

@router.get("/search/analytics")
async def get_search_analytics(
    search_service: EnhancedSearchService = Depends(get_search_service)
):
    """
    Get search analytics and insights
    
    Frontend Integration:
    - Search analytics dashboard
    - Popular queries analysis
    - Search performance metrics
    
    Example Response:
    {
        "total_searches": 1250,
        "unique_queries": 890,
        "average_results": 12.5,
        "popular_queries": [
            {"query": "microgravity", "count": 45},
            {"query": "space biology", "count": 38}
        ],
        "search_performance": {
            "average_response_time": 45.2,
            "success_rate": 98.5
        }
    }
    """
    try:
        analytics = await search_service.get_search_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

@router.post("/search/save")
async def save_search_query(
    query: str = Body(..., embed=True),
    filters: Optional[Dict[str, Any]] = Body(None),
    search_service: EnhancedSearchService = Depends(get_search_service)
):
    """
    Save a search query for analytics
    
    Frontend Integration:
    - Track user searches
    - Analytics data collection
    - Search history (if implemented)
    
    Request Body:
    {
        "query": "microgravity bone loss",
        "filters": {
            "topics": [0, 1],
            "years": [2020, 2021]
        }
    }
    """
    try:
        await search_service.save_search_query(query, filters)
        return {"message": "Search query saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Save search error: {str(e)}")

@router.get("/search/history")
async def get_search_history(
    limit: int = Query(10, ge=1, le=50),
    search_service: EnhancedSearchService = Depends(get_search_service)
):
    """
    Get recent search history
    
    Frontend Integration:
    - Recent searches dropdown
    - Search history sidebar
    - Quick access to previous searches
    
    Parameters:
    - limit: Maximum number of recent searches
    
    Example Response:
    {
        "recent_searches": [
            {
                "query": "microgravity effects",
                "timestamp": "2024-01-15T10:30:00Z",
                "result_count": 15
            }
        ]
    }
    """
    try:
        history = await search_service.get_search_history(limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search history error: {str(e)}")
