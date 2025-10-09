"""
Text preprocessing service for cleaning and processing text data
"""

import pandas as pd
import numpy as np
import re
import string
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import pickle
import json
from collections import Counter
import asyncio

# NLP libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tag import pos_tag

# Text processing libraries
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

from app.config import settings
from app.services.data_exploration_service import DataExplorationService

class TextPreprocessingService:
    """Service for text preprocessing and analysis"""
    
    def __init__(self):
        self.data_dir = Path(settings.data_dir)
        self.data_exploration_service = DataExplorationService()
        
        # Initialize NLP tools
        self._initialize_nltk()
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = self._get_stop_words()
        
        # Cache for processed data
        self._processed_cache = {}
        self._tfidf_cache = {}
    
    def _initialize_nltk(self):
        """Initialize NLTK data"""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            print(f"NLTK initialization warning: {e}")
    
    def _get_stop_words(self) -> set:
        """Get stop words including domain-specific ones"""
        try:
            stop_words = set(stopwords.words('english'))
        except:
            # Fallback stop words if NLTK fails
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
                'before', 'after', 'above', 'below', 'up', 'down', 'out', 'off', 'over',
                'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
                'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
                'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should',
                'now', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
                'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
            }
        
        # Add domain-specific stop words
        domain_stop_words = {
            'study', 'studies', 'research', 'analysis', 'results', 'conclusion',
            'abstract', 'introduction', 'method', 'methods', 'data', 'findings',
            'figure', 'fig', 'table', 'tab', 'doi', 'pmc', 'pubmed', 'journal',
            'article', 'paper', 'publication', 'author', 'authors', 'et', 'al',
            'space', 'biology', 'biological', 'cell', 'cells', 'cellular'
        }
        stop_words.update(domain_stop_words)
        
        return stop_words
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if pd.isna(text) or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\\w\\s.,!?;:-]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\\s+', ' ', text)
        
        return text.strip()
    
    def tokenize_text(self, text: str) -> List[str]:
        """Tokenize text into words"""
        if not text:
            return []
        
        try:
            # Use NLTK tokenizer
            tokens = word_tokenize(text)
        except:
            # Fallback to simple split
            tokens = text.split()
        
        # Remove stop words and short words
        tokens = [token for token in tokens if token.lower() not in self.stop_words and len(token) > 2]
        
        return tokens
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Apply stemming to tokens"""
        try:
            return [self.stemmer.stem(token) for token in tokens]
        except:
            return tokens
    
    def lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """Apply lemmatization to tokens"""
        try:
            return [self.lemmatizer.lemmatize(token) for token in tokens]
        except:
            return tokens
    
    async def preprocess_dataset(self, df: Optional[pd.DataFrame] = None, 
                               file_path: Optional[str] = None) -> Dict[str, Any]:
        """Preprocess entire dataset"""
        if df is None:
            df = await self.data_exploration_service.load_dataset(file_path)
        
        preprocessing_results = {
            "original_shape": df.shape,
            "processed_columns": {},
            "text_analysis": {},
            "vocabulary": {},
            "processing_stats": {}
        }
        
        # Identify text columns
        text_columns = df.select_dtypes(include=['object']).columns.tolist()
        
        for col in text_columns:
            print(f"Processing column: {col}")
            
            # Clean text
            df[f'{col}_cleaned'] = df[col].apply(self.clean_text)
            
            # Tokenize
            df[f'{col}_tokens'] = df[f'{col}_cleaned'].apply(self.tokenize_text)
            df[f'{col}_token_count'] = df[f'{col}_tokens'].apply(len)
            
            # Apply stemming
            df[f'{col}_tokens_stemmed'] = df[f'{col}_tokens'].apply(self.stem_tokens)
            
            # Apply lemmatization
            df[f'{col}_tokens_lemmatized'] = df[f'{col}_tokens'].apply(self.lemmatize_tokens)
            
            # Store processing results
            preprocessing_results["processed_columns"][col] = {
                "cleaned_count": int(df[f'{col}_cleaned'].notna().sum()),
                "avg_token_count": float(df[f'{col}_token_count'].mean()),
                "min_token_count": int(df[f'{col}_token_count'].min()),
                "max_token_count": int(df[f'{col}_token_count'].max())
            }
        
        # Create combined text for analysis
        if 'title' in text_columns and 'abstract' in text_columns:
            df['full_text'] = df['title_cleaned'].fillna('') + ' ' + df['abstract_cleaned'].fillna('')
            df['full_text'] = df['full_text'].str.strip()
        elif text_columns:
            df['full_text'] = df[f'{text_columns[0]}_cleaned'].fillna('')
        
        # Analyze vocabulary
        if 'full_text' in df.columns:
            vocabulary_analysis = await self._analyze_vocabulary(df)
            preprocessing_results["vocabulary"] = vocabulary_analysis
        
        # Calculate processing statistics
        preprocessing_results["processing_stats"] = {
            "total_rows": len(df),
            "text_columns_processed": len(text_columns),
            "new_columns_created": len([col for col in df.columns if any(suffix in col for suffix in ['_cleaned', '_tokens', '_stemmed', '_lemmatized'])])
        }
        
        return preprocessing_results, df
    
    async def _analyze_vocabulary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze vocabulary from processed text"""
        # Combine all tokens
        all_tokens = []
        token_columns = [col for col in df.columns if col.endswith('_tokens_lemmatized')]
        
        for col in token_columns:
            for tokens in df[col]:
                all_tokens.extend(tokens)
        
        # Count word frequencies
        word_freq = Counter(all_tokens)
        
        vocabulary_analysis = {
            "total_vocabulary_size": len(word_freq),
            "total_word_count": sum(word_freq.values()),
            "top_words": dict(word_freq.most_common(50)),
            "avg_words_per_document": sum(word_freq.values()) / len(df) if len(df) > 0 else 0
        }
        
        return vocabulary_analysis
    
    async def create_tfidf_matrix(self, df: pd.DataFrame, 
                                text_column: str = 'full_text',
                                max_features: int = 1000) -> Tuple[Any, Any]:
        """Create TF-IDF matrix for topic modeling"""
        # Prepare text for vectorization
        processed_text = []
        for text in df[text_column]:
            if pd.isna(text):
                processed_text.append("")
            else:
                # Use lemmatized tokens if available
                if f'{text_column}_tokens_lemmatized' in df.columns:
                    tokens = df[df[text_column] == text][f'{text_column}_tokens_lemmatized'].iloc[0]
                    processed_text.append(' '.join(tokens))
                else:
                    processed_text.append(str(text))
        
        # Create TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=2,
            max_df=0.8,
            stop_words='english',
            ngram_range=(1, 2)  # Include bigrams
        )
        
        # Fit and transform
        tfidf_matrix = tfidf_vectorizer.fit_transform(processed_text)
        
        return tfidf_matrix, tfidf_vectorizer
    
    async def perform_topic_modeling(self, df: pd.DataFrame, 
                                   n_topics: int = 5,
                                   text_column: str = 'full_text') -> Dict[str, Any]:
        """Perform topic modeling using LDA"""
        # Create TF-IDF matrix
        tfidf_matrix, tfidf_vectorizer = await self.create_tfidf_matrix(df, text_column)
        
        # Perform LDA
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=100
        )
        
        lda.fit(tfidf_matrix)
        
        # Extract topics
        feature_names = tfidf_vectorizer.get_feature_names_out()
        topics = []
        
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topics.append({
                "topic_id": topic_idx,
                "top_words": top_words,
                "word_weights": [topic[i] for i in top_words_idx]
            })
        
        # Assign topics to documents
        doc_topic_probs = lda.transform(tfidf_matrix)
        df['dominant_topic'] = doc_topic_probs.argmax(axis=1)
        df['topic_confidence'] = doc_topic_probs.max(axis=1)
        
        topic_modeling_results = {
            "n_topics": n_topics,
            "topics": topics,
            "document_topic_distribution": doc_topic_probs.tolist(),
            "topic_assignment_stats": {
                "topic_counts": dict(Counter(df['dominant_topic'])),
                "avg_confidence": float(df['topic_confidence'].mean()),
                "min_confidence": float(df['topic_confidence'].min()),
                "max_confidence": float(df['topic_confidence'].max())
            }
        }
        
        return topic_modeling_results, df
    
    async def save_processed_data(self, df: pd.DataFrame, 
                                output_path: Optional[str] = None) -> str:
        """Save processed dataset"""
        if output_path is None:
            output_path = self.data_dir / "SB_publication_PMC_processed.csv"
        
        # Select relevant columns for saving
        columns_to_save = []
        for col in df.columns:
            if any(suffix in col for suffix in ['_cleaned', '_tokens', '_stemmed', '_lemmatized', 'full_text', 'dominant_topic', 'topic_confidence']):
                columns_to_save.append(col)
            elif col in ['title', 'abstract', 'authors', 'journal', 'publication_date', 'doi', 'pmc_id']:
                columns_to_save.append(col)
        
        processed_df = df[columns_to_save]
        processed_df.to_csv(output_path, index=False)
        
        return str(output_path)
    
    async def get_preprocessing_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary of preprocessing results"""
        summary = {
            "dataset_shape": df.shape,
            "text_columns": [col for col in df.columns if col.endswith('_cleaned')],
            "token_columns": [col for col in df.columns if col.endswith('_tokens')],
            "processing_complete": 'full_text' in df.columns,
            "topic_modeling_complete": 'dominant_topic' in df.columns
        }
        
        # Add statistics for each processed column
        for col in df.columns:
            if col.endswith('_token_count'):
                base_col = col.replace('_token_count', '')
                summary[f"{base_col}_stats"] = {
                    "avg_tokens": float(df[col].mean()),
                    "min_tokens": int(df[col].min()),
                    "max_tokens": int(df[col].max()),
                    "total_documents": int(df[col].count())
                }
        
        return summary
