"""
Text cleaning and preprocessing utilities
"""

import re
import string
from typing import List, Optional
import unicodedata

class TextCleaner:
    """Text cleaning and preprocessing utilities"""
    
    def __init__(self):
        self.punctuation_table = str.maketrans('', '', string.punctuation)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:-]', '', text)
        
        # Normalize unicode characters
        text = unicodedata.normalize('NFKD', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def remove_html_tags(self, text: str) -> str:
        """Remove HTML tags from text"""
        if not text:
            return ""
        
        html_pattern = re.compile('<.*?>')
        return html_pattern.sub('', text)
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text"""
        if not text:
            return ""
        
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return url_pattern.sub('', text)
    
    def remove_emails(self, text: str) -> str:
        """Remove email addresses from text"""
        if not text:
            return ""
        
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        return email_pattern.sub('', text)
    
    def clean_abstract(self, abstract: str) -> str:
        """Clean abstract text specifically"""
        if not abstract:
            return ""
        
        # Remove HTML tags
        abstract = self.remove_html_tags(abstract)
        
        # Remove URLs
        abstract = self.remove_urls(abstract)
        
        # Remove emails
        abstract = self.remove_emails(abstract)
        
        # Clean text
        abstract = self.clean_text(abstract)
        
        return abstract
    
    def extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text"""
        if not text:
            return []
        
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def extract_words(self, text: str) -> List[str]:
        """Extract words from text"""
        if not text:
            return []
        
        # Clean text first
        cleaned_text = self.clean_text(text)
        
        # Split into words
        words = cleaned_text.split()
        
        # Filter out empty strings and very short words
        words = [word for word in words if len(word) > 2]
        
        return words
    
    def remove_stop_words(self, words: List[str], custom_stop_words: Optional[List[str]] = None) -> List[str]:
        """Remove stop words from word list"""
        if not words:
            return []
        
        # Default stop words
        default_stop_words = {
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
        
        if custom_stop_words:
            stop_words = default_stop_words.union(set(custom_stop_words))
        else:
            stop_words = default_stop_words
        
        return [word for word in words if word.lower() not in stop_words]
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in text"""
        if not text:
            return ""
        
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
