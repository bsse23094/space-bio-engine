"""
NLP utilities for text processing and embeddings
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import re
from collections import Counter
import asyncio
import json
import os
from app.config import settings

class NLPProcessor:
    """NLP processing utilities"""
    
    def __init__(self):
        self.stop_words = self._load_stop_words()
        self.embeddings_cache = {}
        self.embeddings_file = settings.embeddings_path
    
    def _load_stop_words(self) -> set:
        """Load stop words"""
        # Basic English stop words
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'up', 'down', 'out', 'off', 'over',
            'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
            'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
            'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should',
            'now', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'shall', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
    
    async def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from text using TF-IDF-like approach"""
        if not text:
            return []
        
        # Clean and tokenize text
        words = self._tokenize(text)
        
        # Remove stop words
        words = [word for word in words if word.lower() not in self.stop_words]
        
        # Count word frequencies
        word_counts = Counter(words)
        
        # Get most common words
        keywords = [word for word, count in word_counts.most_common(max_keywords)]
        
        return keywords
    
    async def get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get text embedding (placeholder implementation)"""
        if not text:
            return None
        
        # Check cache first
        text_hash = hash(text)
        if text_hash in self.embeddings_cache:
            return self.embeddings_cache[text_hash]
        
        # Simple bag-of-words embedding as placeholder
        # In production, this would use sentence-transformers or similar
        words = self._tokenize(text)
        words = [word for word in words if word.lower() not in self.stop_words]
        
        # Create simple embedding based on word frequencies
        unique_words = list(set(words))
        embedding = np.zeros(len(unique_words))
        
        for word in words:
            if word in unique_words:
                embedding[unique_words.index(word)] += 1
        
        # Normalize embedding
        if np.linalg.norm(embedding) > 0:
            embedding = embedding / np.linalg.norm(embedding)
        
        # Cache the embedding
        self.embeddings_cache[text_hash] = embedding
        
        return embedding
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        if not text:
            return []
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Filter out very short words
        words = [word for word in words if len(word) > 2]
        
        return words
    
    def calculate_tf_idf(self, documents: List[str]) -> Dict[str, Dict[str, float]]:
        """Calculate TF-IDF scores for documents"""
        if not documents:
            return {}
        
        # Tokenize all documents
        tokenized_docs = [self._tokenize(doc) for doc in documents]
        
        # Create vocabulary
        all_words = set()
        for doc in tokenized_docs:
            all_words.update(doc)
        
        vocabulary = list(all_words)
        
        # Calculate term frequencies
        tf_scores = []
        for doc in tokenized_docs:
            doc_tf = {}
            doc_length = len(doc)
            for word in vocabulary:
                tf = doc.count(word) / doc_length if doc_length > 0 else 0
                doc_tf[word] = tf
            tf_scores.append(doc_tf)
        
        # Calculate inverse document frequencies
        idf_scores = {}
        total_docs = len(tokenized_docs)
        
        for word in vocabulary:
            doc_count = sum(1 for doc in tokenized_docs if word in doc)
            idf = np.log(total_docs / (doc_count + 1))  # Add 1 to avoid division by zero
            idf_scores[word] = idf
        
        # Calculate TF-IDF scores
        tf_idf_scores = {}
        for i, doc_tf in enumerate(tf_scores):
            doc_tf_idf = {}
            for word in vocabulary:
                tf_idf = doc_tf[word] * idf_scores[word]
                doc_tf_idf[word] = tf_idf
            tf_idf_scores[f"doc_{i}"] = doc_tf_idf
        
        return tf_idf_scores
    
    def extract_named_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract named entities from text (simplified implementation)"""
        if not text:
            return []
        
        entities = []
        
        # Simple pattern matching for common entities
        # In production, this would use spaCy or similar
        
        # Email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        for email in emails:
            entities.append({"text": email, "label": "EMAIL"})
        
        # URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        for url in urls:
            entities.append({"text": url, "label": "URL"})
        
        # DOI patterns
        doi_pattern = r'10\.\d{4,}/[^\s]+'
        dois = re.findall(doi_pattern, text)
        for doi in dois:
            entities.append({"text": doi, "label": "DOI"})
        
        return entities
    
    def extract_phrases(self, text: str, min_length: int = 2, max_length: int = 4) -> List[str]:
        """Extract meaningful phrases from text"""
        if not text:
            return []
        
        words = self._tokenize(text)
        phrases = []
        
        # Generate n-grams
        for n in range(min_length, max_length + 1):
            for i in range(len(words) - n + 1):
                phrase = ' '.join(words[i:i+n])
                phrases.append(phrase)
        
        # Filter phrases (remove those with only stop words)
        filtered_phrases = []
        for phrase in phrases:
            phrase_words = phrase.split()
            if any(word.lower() not in self.stop_words for word in phrase_words):
                filtered_phrases.append(phrase)
        
        return filtered_phrases
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using cosine similarity"""
        embedding1 = asyncio.run(self.get_embedding(text1))
        embedding2 = asyncio.run(self.get_embedding(text2))
        
        if embedding1 is None or embedding2 is None:
            return 0.0
        
        # Ensure embeddings have the same dimension
        min_dim = min(len(embedding1), len(embedding2))
        embedding1 = embedding1[:min_dim]
        embedding2 = embedding2[:min_dim]
        
        # Calculate cosine similarity
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """Summarize text by extracting key sentences"""
        if not text:
            return ""
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return text
        
        # Simple scoring based on word frequency
        words = self._tokenize(text)
        word_freq = Counter(words)
        
        sentence_scores = []
        for sentence in sentences:
            sentence_words = self._tokenize(sentence)
            score = sum(word_freq.get(word, 0) for word in sentence_words)
            sentence_scores.append((sentence, score))
        
        # Sort by score and take top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [sentence for sentence, score in sentence_scores[:max_sentences]]
        
        return '. '.join(top_sentences) + '.'
    
    def load_embeddings_from_file(self) -> Dict[str, np.ndarray]:
        """Load embeddings from file"""
        if not os.path.exists(self.embeddings_file):
            return {}
        
        try:
            with open(self.embeddings_file, 'r') as f:
                embeddings_data = json.load(f)
            
            embeddings = {}
            for key, embedding_list in embeddings_data.items():
                embeddings[key] = np.array(embedding_list)
            
            return embeddings
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            return {}
    
    def save_embeddings_to_file(self, embeddings: Dict[str, np.ndarray]):
        """Save embeddings to file"""
        try:
            os.makedirs(os.path.dirname(self.embeddings_file), exist_ok=True)
            
            embeddings_data = {}
            for key, embedding in embeddings.items():
                embeddings_data[key] = embedding.tolist()
            
            with open(self.embeddings_file, 'w') as f:
                json.dump(embeddings_data, f)
        except Exception as e:
            print(f"Error saving embeddings: {e}")
