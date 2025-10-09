"""
Data exploration service for analyzing CSV datasets
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import json
import os
from pathlib import Path
from datetime import datetime
import asyncio
from collections import Counter
import re

from app.config import settings
from app.models.article import Article, ArticleCreate

class DataExplorationService:
    """Service for data exploration and analysis"""
    
    def __init__(self):
        self.data_dir = Path(settings.data_dir)
        self.csv_path = Path(settings.csv_file_path)
        self._dataset_cache = None
        self._analysis_cache = {}
    
    async def load_dataset(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """Load dataset from CSV file"""
        if file_path:
            csv_path = Path(file_path)
        else:
            csv_path = self.csv_path
        
        if not csv_path.exists():
            raise FileNotFoundError(f"Dataset not found at {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
            self._dataset_cache = df
            return df
        except Exception as e:
            raise Exception(f"Error loading dataset: {str(e)}")
    
    async def get_dataset_overview(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Get basic dataset overview"""
        if df is None:
            df = await self.load_dataset()
        
        overview = {
            "shape": df.shape,
            "columns": list(df.columns),
            "data_types": df.dtypes.to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "total_cells": df.size,
            "non_null_cells": df.count().sum(),
            "null_cells": df.isnull().sum().sum()
        }
        
        return overview
    
    async def analyze_data_quality(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Analyze data quality and completeness"""
        if df is None:
            df = await self.load_dataset()
        
        quality_analysis = {
            "missing_values": {},
            "duplicate_rows": df.duplicated().sum(),
            "completeness_score": 0.0,
            "column_analysis": {}
        }
        
        # Analyze missing values
        missing_data = df.isnull().sum()
        missing_percent = (missing_data / len(df)) * 100
        
        for col in df.columns:
            quality_analysis["missing_values"][col] = {
                "count": int(missing_data[col]),
                "percentage": float(missing_percent[col])
            }
        
        # Calculate overall completeness score
        total_cells = df.size
        non_null_cells = df.count().sum()
        quality_analysis["completeness_score"] = float((non_null_cells / total_cells) * 100)
        
        # Analyze each column
        for col in df.columns:
            col_analysis = {
                "dtype": str(df[col].dtype),
                "unique_values": int(df[col].nunique()),
                "missing_count": int(missing_data[col]),
                "missing_percentage": float(missing_percent[col])
            }
            
            # Add specific analysis based on data type
            if df[col].dtype == 'object':
                col_analysis["avg_length"] = float(df[col].astype(str).str.len().mean())
                col_analysis["min_length"] = int(df[col].astype(str).str.len().min())
                col_analysis["max_length"] = int(df[col].astype(str).str.len().max())
            elif pd.api.types.is_numeric_dtype(df[col]):
                col_analysis["mean"] = float(df[col].mean()) if not df[col].isnull().all() else None
                col_analysis["std"] = float(df[col].std()) if not df[col].isnull().all() else None
                col_analysis["min"] = float(df[col].min()) if not df[col].isnull().all() else None
                col_analysis["max"] = float(df[col].max()) if not df[col].isnull().all() else None
            
            quality_analysis["column_analysis"][col] = col_analysis
        
        return quality_analysis
    
    async def analyze_text_content(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Analyze text content in the dataset"""
        if df is None:
            df = await self.load_dataset()
        
        text_analysis = {
            "text_columns": [],
            "column_analysis": {}
        }
        
        # Identify text columns
        text_columns = df.select_dtypes(include=['object']).columns.tolist()
        text_analysis["text_columns"] = text_columns
        
        for col in text_columns:
            col_data = df[col].dropna()
            if len(col_data) == 0:
                continue
            
            analysis = {
                "non_null_count": int(col_data.count()),
                "avg_length": float(col_data.str.len().mean()),
                "min_length": int(col_data.str.len().min()),
                "max_length": int(col_data.str.len().max()),
                "sample_text": str(col_data.iloc[0])[:200] if len(col_data) > 0 else ""
            }
            
            # Analyze word counts if text is long enough
            if analysis["avg_length"] > 10:
                word_counts = col_data.str.split().str.len()
                analysis["avg_words"] = float(word_counts.mean())
                analysis["min_words"] = int(word_counts.min())
                analysis["max_words"] = int(word_counts.max())
            
            text_analysis["column_analysis"][col] = analysis
        
        return text_analysis
    
    async def analyze_publication_trends(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Analyze publication trends over time"""
        if df is None:
            df = await self.load_dataset()
        
        trends_analysis = {
            "has_date_column": False,
            "date_column": None,
            "year_range": None,
            "publications_by_year": {},
            "total_years": 0
        }
        
        # Look for date columns
        date_columns = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['date', 'year', 'time', 'published']):
                date_columns.append(col)
        
        if not date_columns:
            return trends_analysis
        
        trends_analysis["has_date_column"] = True
        trends_analysis["date_column"] = date_columns[0]
        
        # Analyze the first date column found
        date_col = date_columns[0]
        date_data = df[date_col].dropna()
        
        if len(date_data) == 0:
            return trends_analysis
        
        # Try to extract years
        years = []
        for date_val in date_data:
            if pd.isna(date_val):
                continue
            
            # Try different date formats
            try:
                if isinstance(date_val, str):
                    # Look for 4-digit year
                    year_match = re.search(r'\b(19|20)\d{2}\b', str(date_val))
                    if year_match:
                        years.append(int(year_match.group()))
                else:
                    # Try to convert to datetime
                    if hasattr(date_val, 'year'):
                        years.append(date_val.year)
            except:
                continue
        
        if years:
            year_counts = Counter(years)
            trends_analysis["publications_by_year"] = dict(sorted(year_counts.items()))
            trends_analysis["year_range"] = {
                "min": min(years),
                "max": max(years)
            }
            trends_analysis["total_years"] = len(set(years))
        
        return trends_analysis
    
    async def analyze_journal_distribution(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Analyze journal distribution"""
        if df is None:
            df = await self.load_dataset()
        
        journal_analysis = {
            "has_journal_column": False,
            "journal_column": None,
            "total_journals": 0,
            "top_journals": {},
            "journal_distribution": {}
        }
        
        # Look for journal column
        journal_columns = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['journal', 'publication', 'source']):
                journal_columns.append(col)
        
        if not journal_columns:
            return journal_analysis
        
        journal_analysis["has_journal_column"] = True
        journal_analysis["journal_column"] = journal_columns[0]
        
        journal_col = journal_columns[0]
        journal_data = df[journal_col].dropna()
        
        if len(journal_data) == 0:
            return journal_analysis
        
        journal_counts = journal_data.value_counts()
        journal_analysis["total_journals"] = len(journal_counts)
        journal_analysis["top_journals"] = journal_counts.head(10).to_dict()
        journal_analysis["journal_distribution"] = journal_counts.to_dict()
        
        return journal_analysis
    
    async def analyze_author_distribution(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Analyze author distribution"""
        if df is None:
            df = await self.load_dataset()
        
        author_analysis = {
            "has_author_column": False,
            "author_column": None,
            "total_authors": 0,
            "top_authors": {},
            "author_distribution": {}
        }
        
        # Look for author column
        author_columns = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['author', 'writer', 'creator']):
                author_columns.append(col)
        
        if not author_columns:
            return author_analysis
        
        author_analysis["has_author_column"] = True
        author_analysis["author_column"] = author_columns[0]
        
        author_col = author_columns[0]
        author_data = df[author_col].dropna()
        
        if len(author_data) == 0:
            return author_analysis
        
        # Parse authors (handle different separators)
        all_authors = []
        for authors_str in author_data:
            if pd.isna(authors_str):
                continue
            
            # Try different separators
            if ';' in str(authors_str):
                authors = [author.strip() for author in str(authors_str).split(';')]
            elif ',' in str(authors_str):
                authors = [author.strip() for author in str(authors_str).split(',')]
            else:
                authors = [str(authors_str).strip()]
            
            all_authors.extend(authors)
        
        if all_authors:
            author_counts = Counter(all_authors)
            author_analysis["total_authors"] = len(author_counts)
            author_analysis["top_authors"] = dict(author_counts.most_common(10))
            author_analysis["author_distribution"] = dict(author_counts)
        
        return author_analysis
    
    async def get_comprehensive_analysis(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive dataset analysis"""
        df = await self.load_dataset(file_path)
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "file_path": str(file_path or self.csv_path),
            "overview": await self.get_dataset_overview(df),
            "data_quality": await self.analyze_data_quality(df),
            "text_content": await self.analyze_text_content(df),
            "publication_trends": await self.analyze_publication_trends(df),
            "journal_distribution": await self.analyze_journal_distribution(df),
            "author_distribution": await self.analyze_author_distribution(df)
        }
        
        return analysis
    
    async def export_cleaned_dataset(self, df: Optional[pd.DataFrame] = None, 
                                   output_path: Optional[str] = None) -> str:
        """Export cleaned dataset"""
        if df is None:
            df = await self.load_dataset()
        
        if output_path is None:
            output_path = self.data_dir / "SB_publication_PMC_cleaned.csv"
        
        # Basic cleaning
        cleaned_df = df.copy()
        
        # Remove completely empty rows
        cleaned_df = cleaned_df.dropna(how='all')
        
        # Save cleaned dataset
        cleaned_df.to_csv(output_path, index=False)
        
        return str(output_path)
    
    async def get_sample_data(self, df: Optional[pd.DataFrame] = None, n: int = 5) -> List[Dict[str, Any]]:
        """Get sample data from dataset"""
        if df is None:
            df = await self.load_dataset()
        
        sample_df = df.head(n)
        return sample_df.to_dict('records')
