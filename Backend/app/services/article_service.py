"""
Article service with business logic and NLP operations
"""

import json
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from app.models.article import (
    Article, ArticleCreate, ArticleUpdate, ArticleSearchRequest, 
    SimilarityResult
)
from app.database.db import DatabaseManager
from app.utils.nlp_utils import NLPProcessor
from app.utils.text_cleaner import TextCleaner

class ArticleService:
    """Service layer for article operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.nlp_processor = NLPProcessor()
        self.text_cleaner = TextCleaner()
        self._embeddings_cache = {}
    
    async def get_all_articles(self, limit: int = 100, offset: int = 0) -> List[Article]:
        """Get all articles with pagination"""
        return self.db_manager.get_all_articles(limit=limit, offset=offset)
    
    async def get_article_by_id(self, article_id: int) -> Optional[Article]:
        """Get article by ID"""
        return self.db_manager.get_article_by_id(article_id)
    
    async def create_article(self, article: ArticleCreate) -> Article:
        """Create a new article with preprocessing"""
        # Clean and preprocess text
        if article.abstract:
            article.abstract = self.text_cleaner.clean_text(article.abstract)
        
        if article.title:
            article.title = self.text_cleaner.clean_text(article.title)
        
        # Extract keywords if not provided
        if not article.keywords and article.abstract:
            article.keywords = await self.nlp_processor.extract_keywords(article.abstract)
        
        return self.db_manager.create_article(article)
    
    async def update_article(self, article_id: int, article_update: ArticleUpdate) -> Optional[Article]:
        """Update an article"""
        # Clean text fields if provided
        if article_update.abstract:
            article_update.abstract = self.text_cleaner.clean_text(article_update.abstract)
        
        if article_update.title:
            article_update.title = self.text_cleaner.clean_text(article_update.title)
        
        return self.db_manager.update_article(article_id, article_update)
    
    async def delete_article(self, article_id: int) -> bool:
        """Delete an article"""
        return self.db_manager.delete_article(article_id)
    
    async def search_articles(self, search_request: ArticleSearchRequest) -> List[Article]:
        """Search articles using keyword matching"""
        # Basic keyword search
        articles = self.db_manager.search_articles(search_request.query, search_request.limit)
        
        # If similarity threshold is provided, perform semantic search
        if search_request.similarity_threshold:
            semantic_results = await self._semantic_search(
                search_request.query, 
                search_request.similarity_threshold,
                search_request.limit
            )
            # Combine and deduplicate results
            article_ids = {article.id for article in articles}
            semantic_articles = [result.article for result in semantic_results 
                               if result.article.id not in article_ids]
            articles.extend(semantic_articles[:search_request.limit - len(articles)])
        
        return articles
    
    async def find_similar_articles(self, article_id: int, limit: int = 5, threshold: float = 0.7) -> List[SimilarityResult]:
        """Find similar articles using embeddings"""
        article = await self.get_article_by_id(article_id)
        if not article:
            return []
        
        # Get article embedding
        article_text = f"{article.title} {article.abstract or ''}"
        article_embedding = await self.nlp_processor.get_embedding(article_text)
        
        if article_embedding is None:
            return []
        
        # Get all articles for comparison
        all_articles = await self.get_all_articles(limit=1000)
        similarities = []
        
        for other_article in all_articles:
            if other_article.id == article_id:
                continue
            
            other_text = f"{other_article.title} {other_article.abstract or ''}"
            other_embedding = await self.nlp_processor.get_embedding(other_text)
            
            if other_embedding is not None:
                similarity = self._cosine_similarity(article_embedding, other_embedding)
                
                if similarity >= threshold:
                    # Find matching terms
                    matched_terms = await self._find_matching_terms(
                        article_text, other_text
                    )
                    
                    similarities.append(SimilarityResult(
                        article=other_article,
                        similarity_score=similarity,
                        matched_terms=matched_terms
                    ))
        
        # Sort by similarity score and return top results
        similarities.sort(key=lambda x: x.similarity_score, reverse=True)
        return similarities[:limit]
    
    async def get_articles_by_topic(self, topic_id: int, limit: int = 10) -> List[Article]:
        """Get articles by topic/cluster (placeholder implementation)"""
        # This would integrate with topic modeling results
        # For now, return articles with similar keywords
        all_articles = await self.get_all_articles(limit=1000)
        
        # Simple topic-based filtering (would be replaced with actual topic modeling)
        topic_keywords = {
            1: ["space", "microgravity", "gravity"],
            2: ["radiation", "cosmic", "radiation"],
            3: ["cell", "cellular", "biology"],
            4: ["plant", "botany", "growth"],
            5: ["animal", "behavior", "physiology"]
        }
        
        keywords = topic_keywords.get(topic_id, [])
        if not keywords:
            return []
        
        topic_articles = []
        for article in all_articles:
            article_text = f"{article.title} {article.abstract or ''}".lower()
            if any(keyword.lower() in article_text for keyword in keywords):
                topic_articles.append(article)
                if len(topic_articles) >= limit:
                    break
        
        return topic_articles
    
    async def get_article_stats(self) -> Dict[str, Any]:
        """Get article statistics"""
        all_articles = await self.get_all_articles(limit=10000)
        
        stats = {
            "total_articles": len(all_articles),
            "articles_with_abstracts": len([a for a in all_articles if a.abstract]),
            "articles_with_doi": len([a for a in all_articles if a.doi]),
            "articles_with_pmc_id": len([a for a in all_articles if a.pmc_id]),
            "article_types": {},
            "journals": {},
            "publication_years": {}
        }
        
        # Count article types
        for article in all_articles:
            article_type = article.article_type
            stats["article_types"][article_type] = stats["article_types"].get(article_type, 0) + 1
            
            if article.journal:
                stats["journals"][article.journal] = stats["journals"].get(article.journal, 0) + 1
            
            if article.publication_date:
                year = article.publication_date.year if hasattr(article.publication_date, 'year') else None
                if year:
                    stats["publication_years"][str(year)] = stats["publication_years"].get(str(year), 0) + 1
        
        return stats
    
    async def _semantic_search(self, query: str, threshold: float, limit: int) -> List[SimilarityResult]:
        """Perform semantic search using embeddings"""
        query_embedding = await self.nlp_processor.get_embedding(query)
        if query_embedding is None:
            return []
        
        all_articles = await self.get_all_articles(limit=1000)
        similarities = []
        
        for article in all_articles:
            article_text = f"{article.title} {article.abstract or ''}"
            article_embedding = await self.nlp_processor.get_embedding(article_text)
            
            if article_embedding is not None:
                similarity = self._cosine_similarity(query_embedding, article_embedding)
                
                if similarity >= threshold:
                    matched_terms = await self._find_matching_terms(query, article_text)
                    similarities.append(SimilarityResult(
                        article=article,
                        similarity_score=similarity,
                        matched_terms=matched_terms
                    ))
        
        similarities.sort(key=lambda x: x.similarity_score, reverse=True)
        return similarities[:limit]
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    async def _find_matching_terms(self, text1: str, text2: str) -> List[str]:
        """Find matching terms between two texts"""
        # Simple implementation - would be enhanced with better NLP
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Filter out common stop words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        matching_words = (words1 & words2) - stop_words
        
        return list(matching_words)[:5]  # Return top 5 matching terms
