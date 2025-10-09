"""
Enhanced Search Service for Space Biology Knowledge Engine
Provides semantic search, advanced filtering, and similarity search capabilities
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import os
from typing import List, Dict, Any, Optional
import re
from collections import Counter
import time

from app.models.article import (
    Article, ArticleSearchResponse, SimilarityResult,
    AdvancedSearchRequest, EmbeddingSearchRequest, SearchFilters
)

class EnhancedSearchService:
    """
    Enhanced search service with semantic capabilities
    
    Frontend Integration Notes:
    - All methods return data structures optimized for frontend consumption
    - Includes similarity scores and relevance metrics
    - Supports advanced filtering and sorting
    """
    
    def __init__(self):
        self.data_path = "../datasets/sb_publications_clean.csv"
        self.embeddings_path = "../datasets/embeddings.npy"
        self.metadata_path = "../datasets/metadata.json"
        
        # Load data
        self.df = None
        self.embeddings = None
        self.metadata = None
        self.vectorizer = None
        self.tfidf_matrix = None
        self._load_data()
    
    def _load_data(self):
        """Load datasets for search functionality"""
        try:
            # Load main publications data
            if os.path.exists(self.data_path):
                self.df = pd.read_csv(self.data_path)
                # Extract year from links
                self.df['year'] = self.df['link'].str.extract(r'PMC(\d{4})')
                self.df['year'] = pd.to_numeric(self.df['year'], errors='coerce')
                self.df['year'] = self.df['year'].where(
                    (self.df['year'] >= 1990) & (self.df['year'] <= 2024)
                )
            
            # Load embeddings
            if os.path.exists(self.embeddings_path):
                self.embeddings = np.load(self.embeddings_path)
            
            # Load metadata
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
            
            # Initialize TF-IDF vectorizer for text search
            if self.df is not None and 'clean_text' in self.df.columns:
                self.vectorizer = TfidfVectorizer(
                    max_features=1000,
                    stop_words='english',
                    ngram_range=(1, 2)
                )
                texts = self.df['clean_text'].fillna('').tolist()
                self.tfidf_matrix = self.vectorizer.fit_transform(texts)
                
        except Exception as e:
            print(f"Error loading search data: {e}")
    
    async def semantic_search(self, search_request: EmbeddingSearchRequest) -> ArticleSearchResponse:
        """
        Perform semantic search using embeddings
        
        Frontend Usage:
        - "Find Similar" functionality
        - More accurate than keyword search
        - Returns articles semantically similar to query
        """
        if self.df is None or self.embeddings is None:
            return ArticleSearchResponse(
                articles=[],
                total_count=0,
                query=search_request.query,
                search_time_ms=0
            )
        
        start_time = time.time()
        
        try:
            # For now, use TF-IDF similarity as fallback
            # In production, you would use actual semantic embeddings
            query_vector = self.vectorizer.transform([search_request.query])
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get top similar articles
            top_indices = np.argsort(similarities)[::-1]
            
            # Filter by similarity threshold
            filtered_indices = []
            for idx in top_indices:
                if similarities[idx] >= search_request.similarity_threshold:
                    filtered_indices.append(idx)
                if len(filtered_indices) >= search_request.limit:
                    break
            
            # Convert to articles
            articles = []
            for idx in filtered_indices:
                row = self.df.iloc[idx]
                article = Article(
                    id=int(idx),
                    title=row['title'],
                    link=row.get('link'),
                    text=row.get('text'),
                    clean_text=row.get('clean_text'),
                    word_count=row.get('word_count'),
                    topic=row.get('topic'),
                    year=row.get('year')
                )
                articles.append(article)
            
            search_time = (time.time() - start_time) * 1000
            
            return ArticleSearchResponse(
                articles=articles,
                total_count=len(articles),
                query=search_request.query,
                search_time_ms=round(search_time, 2)
            )
            
        except Exception as e:
            return ArticleSearchResponse(
                articles=[],
                total_count=0,
                query=search_request.query,
                search_time_ms=0
            )
    
    async def advanced_search(self, search_request: AdvancedSearchRequest) -> ArticleSearchResponse:
        """
        Perform advanced search with multiple filters
        
        Frontend Usage:
        - Advanced search forms
        - Multiple filter options
        - Sorting capabilities
        """
        if self.df is None:
            return ArticleSearchResponse(
                articles=[],
                total_count=0,
                query=search_request.query,
                search_time_ms=0
            )
        
        start_time = time.time()
        
        try:
            # Start with all articles
            filtered_df = self.df.copy()
            
            # Apply text search
            if search_request.query:
                query_lower = search_request.query.lower()
                text_mask = (
                    filtered_df['title'].str.lower().str.contains(query_lower, na=False) |
                    filtered_df['clean_text'].str.lower().str.contains(query_lower, na=False)
                )
                filtered_df = filtered_df[text_mask]
            
            # Apply filters
            if search_request.filters:
                filters = search_request.filters
                
                # Topic filter
                if filters.topics:
                    filtered_df = filtered_df[filtered_df['topic'].isin(filters.topics)]
                
                # Year filter
                if filters.years:
                    filtered_df = filtered_df[filtered_df['year'].isin(filters.years)]
                
                # Word count filter
                if filters.min_word_count is not None:
                    filtered_df = filtered_df[filtered_df['word_count'] >= filters.min_word_count]
                
                if filters.max_word_count is not None:
                    filtered_df = filtered_df[filtered_df['word_count'] <= filters.max_word_count]
                
                # Article type filter
                if filters.article_types:
                    filtered_df = filtered_df[filtered_df['article_type'].isin(filters.article_types)]
                
                # Journal filter
                if filters.journals:
                    filtered_df = filtered_df[filtered_df['journal'].isin(filters.journals)]
            
            # Sort results
            if search_request.sort_by == "date":
                filtered_df = filtered_df.sort_values('year', ascending=False, na_position='last')
            elif search_request.sort_by == "word_count":
                filtered_df = filtered_df.sort_values('word_count', ascending=False, na_position='last')
            elif search_request.sort_by == "topic":
                filtered_df = filtered_df.sort_values('topic', na_position='last')
            else:  # relevance - use similarity score
                if search_request.query and self.vectorizer is not None:
                    query_vector = self.vectorizer.transform([search_request.query])
                    similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
                    filtered_df['similarity'] = similarities[filtered_df.index]
                    filtered_df = filtered_df.sort_values('similarity', ascending=False)
            
            # Limit results
            limited_df = filtered_df.head(search_request.limit)
            
            # Convert to articles
            articles = []
            for _, row in limited_df.iterrows():
                article = Article(
                    id=int(row.name),
                    title=row['title'],
                    link=row.get('link'),
                    text=row.get('text'),
                    clean_text=row.get('clean_text'),
                    word_count=row.get('word_count'),
                    topic=row.get('topic'),
                    year=row.get('year')
                )
                articles.append(article)
            
            search_time = (time.time() - start_time) * 1000
            
            return ArticleSearchResponse(
                articles=articles,
                total_count=len(filtered_df),
                query=search_request.query,
                search_time_ms=round(search_time, 2)
            )
            
        except Exception as e:
            return ArticleSearchResponse(
                articles=[],
                total_count=0,
                query=search_request.query,
                search_time_ms=0
            )
    
    async def find_similar_articles(self, article_id: int, limit: int = 5, 
                                  threshold: float = 0.7) -> List[SimilarityResult]:
        """
        Find articles similar to a specific article
        
        Frontend Usage:
        - "Related Articles" section
        - Article detail page recommendations
        - Similarity scores for ranking
        """
        if self.df is None or self.embeddings is None:
            return []
        
        try:
            # Get the reference article
            if article_id >= len(self.df):
                return []
            
            ref_article = self.df.iloc[article_id]
            
            # Calculate similarities
            if self.embeddings is not None and len(self.embeddings) > article_id:
                ref_embedding = self.embeddings[article_id].reshape(1, -1)
                similarities = cosine_similarity(ref_embedding, self.embeddings).flatten()
            else:
                # Fallback to TF-IDF similarity
                if self.vectorizer is not None:
                    ref_text = ref_article.get('clean_text', '')
                    ref_vector = self.vectorizer.transform([ref_text])
                    similarities = cosine_similarity(ref_vector, self.tfidf_matrix).flatten()
                else:
                    return []
            
            # Get top similar articles (excluding the reference article)
            similar_indices = np.argsort(similarities)[::-1]
            similar_indices = [idx for idx in similar_indices if idx != article_id]
            
            # Filter by threshold and limit
            results = []
            for idx in similar_indices:
                if similarities[idx] >= threshold and len(results) < limit:
                    row = self.df.iloc[idx]
                    
                    # Extract matched terms (simplified)
                    matched_terms = self._extract_matched_terms(
                        ref_article.get('title', ''), 
                        row.get('title', '')
                    )
                    
                    article = Article(
                        id=int(idx),
                        title=row['title'],
                        link=row.get('link'),
                        text=row.get('text'),
                        clean_text=row.get('clean_text'),
                        word_count=row.get('word_count'),
                        topic=row.get('topic'),
                        year=row.get('year')
                    )
                    
                    results.append(SimilarityResult(
                        article=article,
                        similarity_score=round(float(similarities[idx]), 3),
                        matched_terms=matched_terms
                    ))
            
            return results
            
        except Exception as e:
            return []
    
    def _extract_matched_terms(self, text1: str, text2: str) -> List[str]:
        """Extract common terms between two texts"""
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        common_words = words1.intersection(words2)
        
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        return [word for word in common_words if word not in stop_words and len(word) > 2][:5]
    
    async def get_search_suggestions(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get search suggestions based on partial query
        
        Frontend Usage:
        - Autocomplete functionality
        - Search suggestions dropdown
        - Real-time suggestions as user types
        """
        if self.df is None or len(query) < 2:
            return {"suggestions": [], "query": query}
        
        try:
            suggestions = []
            query_lower = query.lower()
            
            # Get suggestions from titles
            titles = self.df['title'].dropna().unique()
            
            for title in titles:
                title_lower = title.lower()
                if query_lower in title_lower:
                    # Extract relevant part
                    words = title.split()
                    for i, word in enumerate(words):
                        if query_lower in word.lower():
                            # Get context around the match
                            start = max(0, i - 2)
                            end = min(len(words), i + 3)
                            suggestion = ' '.join(words[start:end])
                            suggestions.append(suggestion)
                            break
            
            # Remove duplicates and limit
            suggestions = list(dict.fromkeys(suggestions))[:limit]
            
            return {
                "suggestions": suggestions,
                "query": query
            }
            
        except Exception as e:
            return {"suggestions": [], "query": query}
    
    async def get_available_filters(self) -> Dict[str, Any]:
        """
        Get available search filters and their options
        
        Frontend Usage:
        - Populate filter dropdowns
        - Show available options
        - Filter counts for each option
        """
        if self.df is None:
            return {"topics": [], "years": [], "journals": []}
        
        try:
            # Topic filters
            topics = []
            topic_counts = self.df['topic'].value_counts()
            for topic_id, count in topic_counts.items():
                if topic_id != -1:  # Skip unassigned
                    topics.append({
                        "id": int(topic_id),
                        "name": f"Topic {int(topic_id)}",
                        "count": int(count)
                    })
            
            # Year filters
            years = []
            year_counts = self.df['year'].value_counts().sort_index()
            for year, count in year_counts.items():
                if pd.notna(year):
                    years.append({
                        "year": int(year),
                        "count": int(count)
                    })
            
            # Journal filters
            journals = []
            if 'journal' in self.df.columns:
                journal_counts = self.df['journal'].value_counts()
                for journal, count in journal_counts.items():
                    if pd.notna(journal):
                        journals.append({
                            "name": journal,
                            "count": int(count)
                        })
            
            return {
                "topics": topics,
                "years": years,
                "journals": journals
            }
            
        except Exception as e:
            return {"topics": [], "years": [], "journals": []}
    
    async def get_trending_topics(self, time_period: str = "month", 
                                limit: int = 10) -> Dict[str, Any]:
        """
        Get trending topics and keywords
        
        Frontend Usage:
        - Trending topics widget
        - Popular searches display
        - Research trend analysis
        """
        if self.df is None:
            return {"trending_topics": [], "trending_keywords": [], "time_period": time_period}
        
        try:
            # For now, return static trending data
            # In production, you would analyze temporal patterns
            
            # Trending topics (based on article count)
            topic_counts = self.df['topic'].value_counts()
            trending_topics = []
            for topic_id, count in topic_counts.head(limit).items():
                if topic_id != -1:
                    trending_topics.append({
                        "topic": f"Topic {int(topic_id)}",
                        "count": int(count),
                        "growth": round(np.random.uniform(5, 20), 1)  # Placeholder
                    })
            
            # Trending keywords (from titles)
            all_titles = ' '.join(self.df['title'].dropna().tolist())
            words = re.findall(r'\b[a-zA-Z]{4,}\b', all_titles.lower())
            word_counts = Counter(words)
            
            trending_keywords = []
            for word, count in word_counts.most_common(limit):
                trending_keywords.append({
                    "keyword": word,
                    "count": count,
                    "growth": round(np.random.uniform(5, 25), 1)  # Placeholder
                })
            
            return {
                "trending_topics": trending_topics,
                "trending_keywords": trending_keywords,
                "time_period": time_period
            }
            
        except Exception as e:
            return {"trending_topics": [], "trending_keywords": [], "time_period": time_period}
    
    async def get_search_analytics(self) -> Dict[str, Any]:
        """
        Get search analytics and insights
        
        Frontend Usage:
        - Search analytics dashboard
        - Popular queries analysis
        - Search performance metrics
        """
        if self.df is None:
            return {
                "total_searches": 0,
                "unique_queries": 0,
                "average_results": 0,
                "popular_queries": [],
                "search_performance": {
                    "average_response_time": 0,
                    "success_rate": 0
                }
            }
        
        try:
            # For now, return mock analytics
            # In production, you would track actual search metrics
            
            return {
                "total_searches": 1250,
                "unique_queries": 890,
                "average_results": 12.5,
                "popular_queries": [
                    {"query": "microgravity", "count": 45},
                    {"query": "space biology", "count": 38},
                    {"query": "bone loss", "count": 32},
                    {"query": "muscle atrophy", "count": 28},
                    {"query": "spaceflight", "count": 25}
                ],
                "search_performance": {
                    "average_response_time": 45.2,
                    "success_rate": 98.5
                }
            }
            
        except Exception as e:
            return {
                "total_searches": 0,
                "unique_queries": 0,
                "average_results": 0,
                "popular_queries": [],
                "search_performance": {
                    "average_response_time": 0,
                    "success_rate": 0
                }
            }
    
    async def save_search_query(self, query: str, filters: Optional[Dict[str, Any]] = None):
        """
        Save a search query for analytics
        
        Frontend Usage:
        - Track user searches
        - Analytics data collection
        - Search history (if implemented)
        """
        # In production, you would save this to a database
        # For now, just log it
        print(f"Search query saved: {query}, filters: {filters}")
    
    async def get_search_history(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get recent search history
        
        Frontend Usage:
        - Recent searches dropdown
        - Search history sidebar
        - Quick access to previous searches
        """
        # In production, you would retrieve from database
        # For now, return mock data
        return {
            "recent_searches": [
                {
                    "query": "microgravity effects",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "result_count": 15
                },
                {
                    "query": "space biology research",
                    "timestamp": "2024-01-15T09:15:00Z",
                    "result_count": 23
                },
                {
                    "query": "bone loss space",
                    "timestamp": "2024-01-14T16:45:00Z",
                    "result_count": 8
                }
            ]
        }
