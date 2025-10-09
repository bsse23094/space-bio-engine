"""
Database configuration and connection management
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import os
from app.config import settings
from app.models.article import Article, ArticleCreate, ArticleUpdate

class DatabaseManager:
    """Database manager for SQLite operations"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.database_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create articles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    authors TEXT,  -- JSON array of authors
                    journal TEXT,
                    publication_date TEXT,
                    doi TEXT,
                    pmc_id TEXT,
                    abstract TEXT,
                    full_text TEXT,
                    keywords TEXT,  -- JSON array of keywords
                    article_type TEXT DEFAULT 'research',
                    url TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON articles(title)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pmc_id ON articles(pmc_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_doi ON articles(doi)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_article_type ON articles(article_type)")
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        finally:
            conn.close()
    
    def create_article(self, article: ArticleCreate) -> Article:
        """Create a new article"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO articles (
                    title, authors, journal, publication_date, doi, pmc_id,
                    abstract, keywords, article_type, url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article.title,
                json.dumps(article.authors),
                article.journal,
                article.publication_date.isoformat() if article.publication_date else None,
                article.doi,
                article.pmc_id,
                article.abstract,
                json.dumps(article.keywords),
                article.article_type.value,
                article.url
            ))
            
            article_id = cursor.lastrowid
            conn.commit()
            
            return self.get_article_by_id(article_id)
    
    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        """Get article by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_article(row)
            return None
    
    def get_all_articles(self, limit: int = 100, offset: int = 0) -> List[Article]:
        """Get all articles with pagination"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM articles 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            rows = cursor.fetchall()
            return [self._row_to_article(row) for row in rows]
    
    def search_articles(self, query: str, limit: int = 50) -> List[Article]:
        """Search articles by title and abstract"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute("""
                SELECT * FROM articles 
                WHERE title LIKE ? OR abstract LIKE ?
                ORDER BY title
                LIMIT ?
            """, (search_term, search_term, limit))
            
            rows = cursor.fetchall()
            return [self._row_to_article(row) for row in rows]
    
    def update_article(self, article_id: int, article_update: ArticleUpdate) -> Optional[Article]:
        """Update an article"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            if article_update.title is not None:
                update_fields.append("title = ?")
                values.append(article_update.title)
            
            if article_update.authors is not None:
                update_fields.append("authors = ?")
                values.append(json.dumps(article_update.authors))
            
            if article_update.journal is not None:
                update_fields.append("journal = ?")
                values.append(article_update.journal)
            
            if article_update.publication_date is not None:
                update_fields.append("publication_date = ?")
                values.append(article_update.publication_date.isoformat())
            
            if article_update.doi is not None:
                update_fields.append("doi = ?")
                values.append(article_update.doi)
            
            if article_update.pmc_id is not None:
                update_fields.append("pmc_id = ?")
                values.append(article_update.pmc_id)
            
            if article_update.abstract is not None:
                update_fields.append("abstract = ?")
                values.append(article_update.abstract)
            
            if article_update.keywords is not None:
                update_fields.append("keywords = ?")
                values.append(json.dumps(article_update.keywords))
            
            if article_update.article_type is not None:
                update_fields.append("article_type = ?")
                values.append(article_update.article_type.value)
            
            if article_update.url is not None:
                update_fields.append("url = ?")
                values.append(article_update.url)
            
            if not update_fields:
                return self.get_article_by_id(article_id)
            
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(article_id)
            
            query = f"UPDATE articles SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            
            if cursor.rowcount > 0:
                conn.commit()
                return self.get_article_by_id(article_id)
            return None
    
    def delete_article(self, article_id: int) -> bool:
        """Delete an article"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def _row_to_article(self, row) -> Article:
        """Convert database row to Article model"""
        return Article(
            id=row['id'],
            title=row['title'],
            authors=json.loads(row['authors']) if row['authors'] else [],
            journal=row['journal'],
            publication_date=row['publication_date'],
            doi=row['doi'],
            pmc_id=row['pmc_id'],
            abstract=row['abstract'],
            full_text=row['full_text'],
            keywords=json.loads(row['keywords']) if row['keywords'] else [],
            article_type=row['article_type'],
            url=row['url'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )

# Global database manager instance
db_manager = DatabaseManager()
