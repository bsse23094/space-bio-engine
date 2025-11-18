from app.services.enhanced_search_service import EnhancedSearchService
from app.models.article import EmbeddingSearchRequest
import asyncio

async def main():
    s = EnhancedSearchService()
    req = EmbeddingSearchRequest(query='bone', limit=3)
    result = await s.semantic_search(req)
    print(f'\nResults: {result.total_count}')
    if result.total_count > 0:
        for i, article in enumerate(result.articles):
            print(f'{i+1}. {article.title}')

if __name__ == '__main__':
    asyncio.run(main())
