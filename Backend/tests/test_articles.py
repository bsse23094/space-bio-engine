"""
Test cases for article functionality
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from app.models.article import Article, ArticleCreate, ArticleUpdate, ArticleType
from app.services.article_service import ArticleService
from app.database.db import DatabaseManager
from app.utils.text_cleaner import TextCleaner
from app.utils.nlp_utils import NLPProcessor

class TestArticleService:
    """Test cases for ArticleService"""
    
    @pytest.fixture
    def mock_db_manager(self):
        """Mock database manager"""
        return Mock(spec=DatabaseManager)
    
    @pytest.fixture
    def article_service(self, mock_db_manager):
        """Article service instance with mocked dependencies"""
        return ArticleService(mock_db_manager)
    
    @pytest.fixture
    def sample_article(self):
        """Sample article for testing"""
        return Article(
            id=1,
            title="Space Biology Research",
            authors=["John Doe", "Jane Smith"],
            journal="Space Science Journal",
            abstract="This is a test abstract about space biology.",
            keywords=["space", "biology", "research"],
            article_type=ArticleType.RESEARCH
        )
    
    @pytest.fixture
    def sample_article_create(self):
        """Sample article creation data"""
        return ArticleCreate(
            title="Space Biology Research",
            authors=["John Doe", "Jane Smith"],
            journal="Space Science Journal",
            abstract="This is a test abstract about space biology.",
            keywords=["space", "biology", "research"],
            article_type=ArticleType.RESEARCH
        )
    
    @pytest.mark.asyncio
    async def test_get_all_articles(self, article_service, mock_db_manager, sample_article):
        """Test getting all articles"""
        mock_db_manager.get_all_articles.return_value = [sample_article]
        
        result = await article_service.get_all_articles(limit=10, offset=0)
        
        assert len(result) == 1
        assert result[0].title == "Space Biology Research"
        mock_db_manager.get_all_articles.assert_called_once_with(limit=10, offset=0)
    
    @pytest.mark.asyncio
    async def test_get_article_by_id(self, article_service, mock_db_manager, sample_article):
        """Test getting article by ID"""
        mock_db_manager.get_article_by_id.return_value = sample_article
        
        result = await article_service.get_article_by_id(1)
        
        assert result is not None
        assert result.title == "Space Biology Research"
        mock_db_manager.get_article_by_id.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_get_article_by_id_not_found(self, article_service, mock_db_manager):
        """Test getting non-existent article"""
        mock_db_manager.get_article_by_id.return_value = None
        
        result = await article_service.get_article_by_id(999)
        
        assert result is None
        mock_db_manager.get_article_by_id.assert_called_once_with(999)
    
    @pytest.mark.asyncio
    async def test_create_article(self, article_service, mock_db_manager, sample_article_create, sample_article):
        """Test creating an article"""
        mock_db_manager.create_article.return_value = sample_article
        
        result = await article_service.create_article(sample_article_create)
        
        assert result is not None
        assert result.title == "Space Biology Research"
        mock_db_manager.create_article.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_search_articles(self, article_service, mock_db_manager, sample_article):
        """Test searching articles"""
        from app.models.article import ArticleSearchRequest
        
        mock_db_manager.search_articles.return_value = [sample_article]
        
        search_request = ArticleSearchRequest(query="space biology", limit=10)
        result = await article_service.search_articles(search_request)
        
        assert len(result) == 1
        assert result[0].title == "Space Biology Research"
        mock_db_manager.search_articles.assert_called_once_with("space biology", 10)
    
    @pytest.mark.asyncio
    async def test_delete_article(self, article_service, mock_db_manager):
        """Test deleting an article"""
        mock_db_manager.delete_article.return_value = True
        
        result = await article_service.delete_article(1)
        
        assert result is True
        mock_db_manager.delete_article.assert_called_once_with(1)

class TestTextCleaner:
    """Test cases for TextCleaner"""
    
    @pytest.fixture
    def text_cleaner(self):
        """Text cleaner instance"""
        return TextCleaner()
    
    def test_clean_text(self, text_cleaner):
        """Test basic text cleaning"""
        dirty_text = "  This is a TEST text with   extra spaces!  "
        cleaned = text_cleaner.clean_text(dirty_text)
        
        assert cleaned == "this is a test text with extra spaces!"
    
    def test_remove_html_tags(self, text_cleaner):
        """Test HTML tag removal"""
        html_text = "<p>This is <b>bold</b> text</p>"
        cleaned = text_cleaner.remove_html_tags(html_text)
        
        assert cleaned == "This is bold text"
    
    def test_remove_urls(self, text_cleaner):
        """Test URL removal"""
        text_with_urls = "Check out https://example.com for more info"
        cleaned = text_cleaner.remove_urls(text_with_urls)
        
        assert cleaned == "Check out  for more info"
    
    def test_extract_words(self, text_cleaner):
        """Test word extraction"""
        text = "This is a test sentence with punctuation!"
        words = text_cleaner.extract_words(text)
        
        assert "this" in words
        assert "test" in words
        assert "punctuation" not in words  # Should be filtered out
    
    def test_remove_stop_words(self, text_cleaner):
        """Test stop word removal"""
        words = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
        filtered = text_cleaner.remove_stop_words(words)
        
        assert "the" not in filtered
        assert "over" not in filtered
        assert "quick" in filtered
        assert "fox" in filtered

class TestNLPProcessor:
    """Test cases for NLPProcessor"""
    
    @pytest.fixture
    def nlp_processor(self):
        """NLP processor instance"""
        return NLPProcessor()
    
    def test_tokenize(self, nlp_processor):
        """Test text tokenization"""
        text = "This is a test sentence!"
        tokens = nlp_processor._tokenize(text)
        
        assert "this" in tokens
        assert "test" in tokens
        assert "!" not in tokens  # Punctuation should be removed
    
    @pytest.mark.asyncio
    async def test_extract_keywords(self, nlp_processor):
        """Test keyword extraction"""
        text = "Space biology research in microgravity environments"
        keywords = await nlp_processor.extract_keywords(text, max_keywords=5)
        
        assert len(keywords) <= 5
        assert "space" in keywords
        assert "biology" in keywords
    
    @pytest.mark.asyncio
    async def test_get_embedding(self, nlp_processor):
        """Test embedding generation"""
        text = "This is a test text for embedding"
        embedding = await nlp_processor.get_embedding(text)
        
        assert embedding is not None
        assert isinstance(embedding, type(nlp_processor._tokenize("test")))  # Should be numpy array
    
    def test_calculate_text_similarity(self, nlp_processor):
        """Test text similarity calculation"""
        text1 = "Space biology research"
        text2 = "Biology research in space"
        
        # This is a synchronous method, so we don't need async
        similarity = nlp_processor.calculate_text_similarity(text1, text2)
        
        assert 0.0 <= similarity <= 1.0
    
    def test_extract_named_entities(self, nlp_processor):
        """Test named entity extraction"""
        text = "Contact us at test@example.com or visit https://example.com"
        entities = nlp_processor.extract_named_entities(text)
        
        assert len(entities) >= 2  # Should find email and URL
        assert any(entity["label"] == "EMAIL" for entity in entities)
        assert any(entity["label"] == "URL" for entity in entities)

# Integration tests
class TestIntegration:
    """Integration tests"""
    
    @pytest.mark.asyncio
    async def test_full_article_workflow(self):
        """Test complete article workflow"""
        # This would test the full workflow from creation to search
        # For now, it's a placeholder for future integration tests
        pass
