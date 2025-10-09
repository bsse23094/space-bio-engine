"""
Simple Article API routes that read from CSV files
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import time
import pandas as pd
import os

router = APIRouter()

def load_articles_data():
    """Load articles from CSV file"""
    csv_path = "../datasets/sb_publications_clean.csv"
    if not os.path.exists(csv_path):
        csv_path = "datasets/sb_publications_clean.csv"
    
    if not os.path.exists(csv_path):
        return None
    
    return pd.read_csv(csv_path)

@router.get("/articles")
async def get_articles(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all articles with pagination"""
    try:
        df = load_articles_data()
        
        if df is None:
            return []
        
        # Apply pagination
        results_df = df.iloc[offset:offset+limit]
        
        # Convert to list of dictionaries
        articles = []
        for idx, row in results_df.iterrows():
            # Extract year from link if available
            year = None
            link_str = str(row.get('link', ''))
            if link_str and '/articles/PMC' in link_str:
                import re
                year_match = re.search(r'/articles/PMC\d+/(\d{4})/', link_str)
                if year_match:
                    year = int(year_match.group(1))
            
            articles.append({
                "id": int(idx),
                "title": str(row.get('title', '')),
                "link": link_str if pd.notna(row.get('link')) else None,
                "text": str(row.get('text', ''))[:500] if pd.notna(row.get('text')) else None,  # Truncate for performance
                "clean_text": str(row.get('clean_text', ''))[:500] if pd.notna(row.get('clean_text')) else None,
                "word_count": int(row.get('word_count', 0)) if pd.notna(row.get('word_count')) else 0,
                "topic": int(row.get('topic', -1)) if pd.notna(row.get('topic')) else -1,
                "year": year,
            })
        
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading articles: {str(e)}")

@router.get("/articles/search")
async def search_articles(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100)
):
    """Search articles by keyword using CSV data"""
    try:
        start_time = time.time()
        
        df = load_articles_data()
        
        if df is None:
            return {
                "articles": [],
                "total_count": 0,
                "query": q,
                "search_time_ms": 0,
                "message": "No data available"
            }
        
        # Simple text search in title and clean_text
        query_lower = q.lower()
        
        # Create search mask
        title_mask = df['title'].fillna('').str.lower().str.contains(query_lower, regex=False)
        text_mask = df['clean_text'].fillna('').str.lower().str.contains(query_lower, regex=False)
        mask = title_mask | text_mask
        
        results_df = df[mask].head(limit)
        
        # Convert to list of dictionaries
        articles = []
        for idx, row in results_df.iterrows():
            # Extract year from link if available
            year = None
            link_str = str(row.get('link', ''))
            if link_str and '/articles/PMC' in link_str:
                import re
                year_match = re.search(r'/articles/PMC\d+/(\d{4})/', link_str)
                if year_match:
                    year = int(year_match.group(1))
            
            articles.append({
                "id": int(idx),
                "title": str(row.get('title', '')),
                "link": link_str if pd.notna(row.get('link')) else None,
                "text": str(row.get('text', ''))[:500] if pd.notna(row.get('text')) else None,
                "clean_text": str(row.get('clean_text', ''))[:500] if pd.notna(row.get('clean_text')) else None,
                "word_count": int(row.get('word_count', 0)) if pd.notna(row.get('word_count')) else 0,
                "topic": int(row.get('topic', -1)) if pd.notna(row.get('topic')) else -1,
                "year": year,
            })
        
        search_time = (time.time() - start_time) * 1000
        
        return {
            "articles": articles,
            "total_count": len(articles),
            "query": q,
            "search_time_ms": search_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@router.get("/articles/{article_id}")
async def get_article(article_id: int):
    """Get a specific article by ID"""
    try:
        df = load_articles_data()
        
        if df is None:
            raise HTTPException(status_code=404, detail="Data not available")
        
        # Find article by index (ID)
        if article_id >= len(df):
            raise HTTPException(status_code=404, detail="Article not found")
        
        row = df.iloc[article_id]
        
        # Extract year from link if available
        year = None
        link_str = str(row.get('link', ''))
        if link_str and '/articles/PMC' in link_str:
            import re
            year_match = re.search(r'/articles/PMC\d+/(\d{4})/', link_str)
            if year_match:
                year = int(year_match.group(1))
        
        return {
            "id": article_id,
            "title": str(row.get('title', '')),
            "link": link_str if pd.notna(row.get('link')) else None,
            "text": str(row.get('text', '')) if pd.notna(row.get('text')) else None,
            "clean_text": str(row.get('clean_text', '')) if pd.notna(row.get('clean_text')) else None,
            "word_count": int(row.get('word_count', 0)) if pd.notna(row.get('word_count')) else 0,
            "topic": int(row.get('topic', -1)) if pd.notna(row.get('topic')) else -1,
            "year": year,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

