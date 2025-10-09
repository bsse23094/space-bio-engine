# 🚀 Space Biology Knowledge Engine - API Documentation

## Overview

The Space Biology Knowledge Engine API provides comprehensive access to space biology research data with advanced search, visualization, and analysis capabilities. Built on FastAPI with detailed documentation and frontend-friendly responses.

## 🎯 Frontend Integration Guide

### Base URL

```
http://localhost:8000/api/v1
```

### Authentication

Currently no authentication required. All endpoints are publicly accessible.

### Response Format

All responses are JSON with consistent structure:

```json
{
  "data": {...},
  "status": "success",
  "message": "Optional message"
}
```

## 📊 Core Endpoints

### 1. Articles Management

#### Get All Articles

```http
GET /api/v1/articles
```

**Parameters:**

- `limit` (int, optional): Number of articles to return (1-100, default: 10)
- `offset` (int, optional): Number of articles to skip (default: 0)

**Response:**

```json
[
  {
    "id": 1,
    "title": "Microgravity Effects on Bone Loss",
    "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3630201/",
    "text": "Original article text",
    "clean_text": "Preprocessed text",
    "word_count": 14,
    "topic": 3,
    "year": 2013,
    "authors": ["Author1", "Author2"],
    "journal": "Nature",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Get Article by ID

```http
GET /api/v1/articles/{article_id}
```

#### Search Articles

```http
GET /api/v1/articles/search?q={query}&limit={limit}
```

**Parameters:**

- `q` (string, required): Search query
- `limit` (int, optional): Maximum results (1-100, default: 10)
- `similarity_threshold` (float, optional): Minimum similarity score (0.0-1.0)

### 2. 🔍 Enhanced Search

#### Semantic Search

```http
POST /api/v1/search/semantic
```

**Request Body:**

```json
{
  "query": "microgravity effects on bone",
  "limit": 10,
  "similarity_threshold": 0.7,
  "use_embeddings": true
}
```

**Frontend Usage:**

- Use for "Find Similar" functionality
- More accurate than keyword search
- Returns semantically similar articles

#### Advanced Search with Filters

```http
POST /api/v1/search/advanced
```

**Request Body:**

```json
{
  "query": "space biology",
  "filters": {
    "topics": [0, 1, 2],
    "years": [2020, 2021, 2022],
    "min_word_count": 10,
    "max_word_count": 50,
    "article_types": ["research"],
    "journals": ["Nature", "Science"]
  },
  "limit": 20,
  "sort_by": "relevance"
}
```

#### Find Similar Articles

```http
GET /api/v1/search/similar/{article_id}?limit={limit}&threshold={threshold}
```

**Frontend Usage:**

- "Related Articles" section
- Article detail page recommendations
- Similarity scores for ranking

#### Search Suggestions

```http
GET /api/v1/search/suggestions?query={partial_query}&limit={limit}
```

**Response:**

```json
{
  "suggestions": [
    "microgravity effects",
    "microgravity bone loss",
    "microgravity muscle atrophy"
  ],
  "query": "micrograv"
}
```

### 3. 📊 Visualizations

#### Topic Distribution

```http
GET /api/v1/visualizations/topic-distribution
```

**Response:**

```json
[
  {
    "topic_id": 0,
    "topic_name": "Spaceflight Research",
    "article_count": 146,
    "percentage": 25.7,
    "top_words": ["spaceflight", "microgravity", "space"]
  }
]
```

**Frontend Usage:**

- Pie charts: Use `percentage` for slice sizes
- Bar charts: Use `article_count` for bar heights
- Tooltips: Display `top_words` for context

#### Temporal Trends

```http
GET /api/v1/visualizations/temporal-trends?start_year={year}&end_year={year}
```

**Response:**

```json
[
  {
    "year": 2020,
    "article_count": 45,
    "topics": {
      "0": 12,
      "1": 8,
      "2": 15
    }
  }
]
```

**Frontend Usage:**

- Line charts: `year` on x-axis, `article_count` on y-axis
- Multi-line charts: Use `topics` dict for topic-specific trends

#### Word Cloud Data

```http
GET /api/v1/visualizations/word-cloud/{topic_id}?max_words={count}
```

**Response:**

```json
{
  "topic_id": 0,
  "words": {
    "spaceflight": 45,
    "microgravity": 32,
    "space": 28
  },
  "title": "Topic 0 Word Cloud"
}
```

**Frontend Usage:**

- Word cloud libraries: WordCloud.js, D3.js
- Word size: Proportional to frequency
- Color: Based on topic or frequency

#### Network Visualization

```http
GET /api/v1/visualizations/network?network_type={type}&min_frequency={freq}&max_nodes={count}
```

**Parameters:**

- `network_type`: "word_cooccurrence" or "topic_similarity"
- `min_frequency`: Minimum word frequency threshold
- `max_nodes`: Maximum nodes to include

**Response:**

```json
{
  "nodes": [
    {
      "id": "spaceflight",
      "label": "spaceflight",
      "size": 45,
      "color": "#ff6b6b"
    }
  ],
  "edges": [
    {
      "source": "spaceflight",
      "target": "microgravity",
      "weight": 0.8,
      "color": "#95a5a6"
    }
  ],
  "title": "Word Co-occurrence Network",
  "layout": "force"
}
```

**Frontend Usage:**

- Network libraries: D3.js, vis.js, Cytoscape.js
- Node size: Based on frequency/importance
- Edge thickness: Based on weight/co-occurrence

#### Comprehensive Statistics

```http
GET /api/v1/visualizations/statistics
```

**Response:**

```json
{
  "total_articles": 624,
  "articles_with_topics": 569,
  "articles_with_year": 624,
  "unique_topics": 9,
  "year_range": {
    "min": 1990,
    "max": 2024
  },
  "average_word_count": 8.5,
  "topic_distribution": [...],
  "temporal_trends": [...]
}
```

**Frontend Usage:**

- Dashboard overview cards
- Main statistics display
- Overview charts

### 4. 📈 Chart Data

#### Generic Chart Data

```http
GET /api/v1/visualizations/chart/{chart_type}?topic_id={id}&year_range={range}
```

**Supported Chart Types:**

- `word_count_distribution`: Histogram of word counts
- `topic_evolution`: Topic trends over time
- `publication_density`: Publications per year
- `topic_coherence`: Topic quality scores

**Response:**

```json
{
  "chart_type": "bar",
  "title": "Topic Distribution",
  "data": {
    "labels": ["Topic 0", "Topic 1"],
    "datasets": [
      {
        "data": [146, 89],
        "label": "Article Count"
      }
    ]
  },
  "x_axis": "Topics",
  "y_axis": "Article Count"
}
```

**Frontend Usage:**

- Compatible with Chart.js, D3.js
- Flexible chart generation
- Data structure optimized for common libraries

## 🎨 Frontend Implementation Examples

### React.js Integration

```javascript
// Fetch topic distribution for pie chart
const fetchTopicDistribution = async () => {
  const response = await fetch("/api/v1/visualizations/topic-distribution");
  const data = await response.json();

  // Use with Chart.js
  const chartData = {
    labels: data.map((topic) => topic.topic_name),
    datasets: [
      {
        data: data.map((topic) => topic.percentage),
        backgroundColor: ["#ff6b6b", "#4ecdc4", "#45b7d1"],
      },
    ],
  };

  return chartData;
};

// Semantic search
const performSemanticSearch = async (query) => {
  const response = await fetch("/api/v1/search/semantic", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: query,
      limit: 10,
      similarity_threshold: 0.7,
    }),
  });

  return await response.json();
};
```

### Vue.js Integration

```javascript
// Vue component for word cloud
export default {
  data() {
    return {
      wordCloudData: null,
    };
  },
  async mounted() {
    await this.loadWordCloud(0); // Load word cloud for topic 0
  },
  methods: {
    async loadWordCloud(topicId) {
      const response = await fetch(
        `/api/v1/visualizations/word-cloud/${topicId}`
      );
      this.wordCloudData = await response.json();

      // Use with WordCloud.js
      this.generateWordCloud();
    },
    generateWordCloud() {
      // Implementation with WordCloud.js
      WordCloud(document.getElementById("wordcloud"), {
        list: Object.entries(this.wordCloudData.words).map(([word, freq]) => [
          word,
          freq,
        ]),
        weightFactor: 10,
        color: "random-dark",
      });
    },
  },
};
```

### Angular Integration

```typescript
// Angular service for API calls
@Injectable()
export class SpaceBioApiService {
  private baseUrl = "/api/v1";

  constructor(private http: HttpClient) {}

  // Get temporal trends for line chart
  getTemporalTrends(
    startYear?: number,
    endYear?: number
  ): Observable<TemporalAnalysis[]> {
    let params = new HttpParams();
    if (startYear) params = params.set("start_year", startYear.toString());
    if (endYear) params = params.set("end_year", endYear.toString());

    return this.http.get<TemporalAnalysis[]>(
      `${this.baseUrl}/visualizations/temporal-trends`,
      { params }
    );
  }

  // Advanced search with filters
  advancedSearch(
    request: AdvancedSearchRequest
  ): Observable<ArticleSearchResponse> {
    return this.http.post<ArticleSearchResponse>(
      `${this.baseUrl}/search/advanced`,
      request
    );
  }
}
```

## 🔧 Error Handling

### Standard Error Response

```json
{
  "detail": "Error message",
  "status_code": 500
}
```

### Common HTTP Status Codes

- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (article/resource not found)
- `422`: Validation Error (invalid request body)
- `500`: Internal Server Error

## 📱 Mobile App Integration

### React Native Example

```javascript
// Fetch articles for mobile list
const fetchArticles = async (limit = 20, offset = 0) => {
  try {
    const response = await fetch(
      `http://your-api-domain.com/api/v1/articles?limit=${limit}&offset=${offset}`
    );
    const articles = await response.json();
    return articles;
  } catch (error) {
    console.error("API Error:", error);
    return [];
  }
};

// Search with debouncing
const searchArticles = async (query) => {
  if (query.length < 2) return [];

  const response = await fetch(
    `http://your-api-domain.com/api/v1/articles/search?q=${encodeURIComponent(
      query
    )}`
  );
  return await response.json();
};
```

## 🚀 Performance Tips

### Caching

- Cache visualization data (topics, statistics) for better performance
- Use browser localStorage for search history
- Implement pagination for large datasets

### Optimization

- Use `limit` parameter to control response size
- Implement client-side filtering for better UX
- Use semantic search for better relevance

### Rate Limiting

- Currently no rate limiting implemented
- Consider implementing for production use

## 🔐 Security Considerations

### CORS

- Currently allows all origins (`*`)
- Configure specific origins for production

### Data Privacy

- No personal data stored
- All data is publicly available research articles

## 📊 Data Structure

### Article Model

```typescript
interface Article {
  id?: number;
  title: string;
  link?: string;
  text?: string;
  clean_text?: string;
  word_count?: number;
  topic?: number;
  year?: number;
  authors: string[];
  journal?: string;
  publication_date?: string;
  doi?: string;
  pmc_id?: string;
  abstract?: string;
  keywords: string[];
  article_type: "research" | "review" | "case_study" | "other";
  url?: string;
  created_at?: string;
  updated_at?: string;
}
```

### Topic Distribution

```typescript
interface TopicDistribution {
  topic_id: number;
  topic_name?: string;
  article_count: number;
  percentage: number;
  top_words: string[];
}
```

## 🎯 Best Practices

### Frontend Development

1. **Use TypeScript** for better type safety
2. **Implement error boundaries** for robust error handling
3. **Add loading states** for better UX
4. **Use pagination** for large datasets
5. **Implement search debouncing** for performance

### API Usage

1. **Cache static data** (topics, statistics)
2. **Use appropriate limits** to control response size
3. **Handle errors gracefully** with fallback UI
4. **Implement retry logic** for failed requests
5. **Use semantic search** for better relevance

## 📞 Support

For API support and questions:

- **Documentation**: `/docs` (Swagger UI)
- **Alternative Docs**: `/redoc` (ReDoc)
- **Health Check**: `/health`
- **API Stats**: `/api/v1/stats`

## 🔄 Version History

- **v2.0.0**: Enhanced search, visualizations, comprehensive documentation
- **v1.0.0**: Basic article management and search

---

_This API is designed for easy frontend integration with comprehensive documentation and examples. All endpoints include detailed frontend usage notes and response schemas._
