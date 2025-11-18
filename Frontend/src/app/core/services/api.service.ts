import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Article } from '../models/article.model';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private base = environment.apiBase;

  constructor(private http: HttpClient) {}

  getArticles(limit = 10, offset = 0): Observable<Article[]> {
    let params = new HttpParams().set('limit', String(limit)).set('offset', String(offset));
    return this.http.get<Article[]>(`${this.base}/articles`, { params });
  }

  getArticle(id: number): Observable<Article> {
    return this.http.get<Article>(`${this.base}/articles/${id}`);
  }

  getStatistics(): Observable<any> {
    return this.http.get<any>(`${this.base}/visualizations/statistics`);
  }

  searchArticles(query: string, limit: number = 10): Observable<any> {
    return this.http.post<any>(`${this.base}/search/semantic`, {
      query: query,
      limit: limit,
      similarity_threshold: 0.3,
      use_semantic_search: true
    });
  }

  // Visualization endpoints
  getTopicDistribution(): Observable<any> {
    return this.http.get(`${this.base}/visualizations/topic-distribution`);
  }

  getTemporalTrends(startYear?: number, endYear?: number): Observable<any> {
    let params = new HttpParams();
    if (startYear) params = params.set('start_year', String(startYear));
    if (endYear) params = params.set('end_year', String(endYear));
    return this.http.get(`${this.base}/visualizations/temporal-trends`, { params });
  }

  getWordFrequencies(limit: number = 20): Observable<any> {
    // Use word cloud endpoint for general word frequencies (topic_id = -1 for all topics)
    return this.http.get(`${this.base}/visualizations/word-cloud/-1`, { 
      params: { limit: String(limit) } 
    });
  }

  getTopicWordCloud(topicId: number): Observable<any> {
    return this.http.get(`${this.base}/visualizations/word-cloud/${topicId}`);
  }
}
