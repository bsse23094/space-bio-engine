"""
Configuration settings for the Space Biology Knowledge Engine
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    app_name: str = "Space Biology Knowledge Engine"
    debug: bool = False
    
    # Database Settings
    database_url: Optional[str] = None
    database_path: str = "data/articles.db"
    
    # Data Settings
    data_dir: str = "data"
    csv_file_path: str = "data/SB_publication_PMC.csv"
    embeddings_path: str = "data/embeddings.json"
    
    # NLP Settings
    max_articles: int = 1000
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Search Settings
    similarity_threshold: float = 0.7
    max_search_results: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
