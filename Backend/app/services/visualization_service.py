"""
Visualization Service for Space Biology Knowledge Engine
Handles data processing and preparation for frontend visualizations
"""

import pandas as pd
import numpy as np
from collections import Counter
import json
import os
from typing import List, Dict, Any, Optional
import re
from datetime import datetime

from app.models.article import (
    TopicDistribution, TemporalAnalysis, WordCloudData, 
    NetworkData, NetworkNode, NetworkEdge, StatisticsResponse, 
    TopicInfo, VisualizationData
)

class VisualizationService:
    """
    Service for generating visualization data
    
    Frontend Integration Notes:
    - All methods return data structures ready for frontend consumption
    - Data is optimized for common charting libraries (Chart.js, D3.js, etc.)
    - Includes metadata for proper chart configuration
    """
    
    def __init__(self):
        self.data_path = "../datasets/sb_publications_clean.csv"
        self.topics_path = "../datasets/topics.csv"
        self.embeddings_path = "../datasets/embeddings.npy"
        self.metadata_path = "../datasets/metadata.json"
        
        # Load data
        self.df = None
        self.topics_df = None
        self.embeddings = None
        self.metadata = None
        self._load_data()
    
    def _load_data(self):
        """Load datasets for visualization"""
        try:
            # Load main publications data
            if os.path.exists(self.data_path):
                self.df = pd.read_csv(self.data_path)
                # Extract year from links
                self.df['year'] = self.df['link'].str.extract(r'PMC(\d{4})')
                self.df['year'] = pd.to_numeric(self.df['year'], errors='coerce')
                self.df['year'] = self.df['year'].where(
                    (self.df['year'] >= 1990) & (self.df['year'] <= 2024)
                )
            
            # Load topics data
            if os.path.exists(self.topics_path):
                self.topics_df = pd.read_csv(self.topics_path)
            
            # Load embeddings
            if os.path.exists(self.embeddings_path):
                self.embeddings = np.load(self.embeddings_path)
            
            # Load metadata
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                    
        except Exception as e:
            print(f"Error loading data: {e}")
    
    async def get_topic_distribution(self) -> List[TopicDistribution]:
        """
        Get topic distribution statistics
        
        Frontend Usage:
        - Pie charts: Use 'percentage' for slice sizes
        - Bar charts: Use 'article_count' for bar heights
        - Tooltips: Display 'top_words' for context
        """
        if self.df is None:
            return []
        
        # Filter out unassigned topics (-1)
        valid_topics = self.df[self.df['topic'] != -1]['topic'].dropna()
        topic_counts = valid_topics.value_counts().sort_index()
        
        distribution = []
        total_articles = len(valid_topics)
        
        for topic_id, count in topic_counts.items():
            percentage = (count / total_articles) * 100
            
            # Get top words for this topic
            top_words = []
            if self.topics_df is not None and topic_id in self.topics_df.columns:
                topic_col = f"Topic {int(topic_id)}"
                if topic_col in self.topics_df.columns:
                    top_words = self.topics_df[topic_col].dropna().tolist()[:5]
            
            distribution.append(TopicDistribution(
                topic_id=int(topic_id),
                topic_name=f"Topic {int(topic_id)}",
                article_count=int(count),
                percentage=round(percentage, 1),
                top_words=top_words
            ))
        
        return distribution
    
    async def get_temporal_trends(self, start_year: Optional[int] = None, 
                                end_year: Optional[int] = None) -> List[TemporalAnalysis]:
        """
        Get temporal analysis data
        
        Frontend Usage:
        - Line charts: 'year' on x-axis, 'article_count' on y-axis
        - Multi-line charts: Use 'topics' dict for topic-specific trends
        """
        if self.df is None:
            return []
        
        # Filter by year range if specified
        df_filtered = self.df.copy()
        if start_year:
            df_filtered = df_filtered[df_filtered['year'] >= start_year]
        if end_year:
            df_filtered = df_filtered[df_filtered['year'] <= end_year]
        
        # Get yearly counts
        yearly_counts = df_filtered['year'].value_counts().sort_index()
        
        trends = []
        for year, count in yearly_counts.items():
            # Get topic distribution for this year
            year_data = df_filtered[df_filtered['year'] == year]
            topic_counts = year_data['topic'].value_counts().to_dict()
            
            # Convert to int keys and filter out -1
            topic_counts = {int(k): int(v) for k, v in topic_counts.items() if k != -1}
            
            trends.append(TemporalAnalysis(
                year=int(year),
                article_count=int(count),
                topics=topic_counts
            ))
        
        return trends
    
    async def get_word_cloud_data(self, topic_id: int, max_words: int = 50) -> WordCloudData:
        """
        Get word cloud data for a topic
        
        Frontend Usage:
        - Word cloud libraries: WordCloud.js, D3.js word clouds
        - Word size: Proportional to frequency
        - Color: Can be based on topic or frequency
        """
        if self.topics_df is None:
            return WordCloudData(words={}, title="No Data Available")
        
        if topic_id == -1:
            # All topics combined
            all_words = []
            for col in self.topics_df.columns:
                if col.startswith('Topic'):
                    words = self.topics_df[col].dropna().tolist()
                    all_words.extend(words)
            title = "All Topics Combined"
        else:
            # Specific topic
            topic_col = f"Topic {topic_id}"
            if topic_col not in self.topics_df.columns:
                return WordCloudData(words={}, title=f"Topic {topic_id} - No Data")
            
            all_words = self.topics_df[topic_col].dropna().tolist()
            title = f"Topic {topic_id} Word Cloud"
        
        # Count word frequencies
        word_counts = Counter(all_words)
        
        # Get top words
        top_words = dict(word_counts.most_common(max_words))
        
        return WordCloudData(
            topic_id=topic_id if topic_id != -1 else None,
            words=top_words,
            title=title
        )
    
    async def get_network_data(self, network_type: str = "word_cooccurrence", 
                             min_frequency: int = 3, max_nodes: int = 50) -> NetworkData:
        """
        Get network visualization data
        
        Frontend Usage:
        - Network libraries: D3.js, vis.js, Cytoscape.js
        - Node size: Based on frequency/importance
        - Edge thickness: Based on weight/co-occurrence
        """
        if self.df is None:
            return NetworkData(nodes=[], edges=[], title="No Data Available")
        
        if network_type == "word_cooccurrence":
            return await self._get_word_cooccurrence_network(min_frequency, max_nodes)
        elif network_type == "topic_similarity":
            return await self._get_topic_similarity_network()
        else:
            return NetworkData(nodes=[], edges=[], title="Unknown Network Type")
    
    async def _get_word_cooccurrence_network(self, min_frequency: int, max_nodes: int) -> NetworkData:
        """Generate word co-occurrence network"""
        # Extract words from titles
        titles = self.df['title'].dropna().tolist()
        word_pairs = {}
        word_freq = {}
        
        for title in titles:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
            words = [w for w in words if len(w) > 2]
            
            # Count word frequencies
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Count co-occurrences
            for i, word1 in enumerate(words):
                for word2 in words[i+1:i+5]:  # Look at next 4 words
                    if word1 != word2:
                        pair = tuple(sorted([word1, word2]))
                        word_pairs[pair] = word_pairs.get(pair, 0) + 1
        
        # Filter by minimum frequency
        filtered_words = {word: freq for word, freq in word_freq.items() 
                         if freq >= min_frequency}
        
        # Get top words
        top_words = dict(Counter(filtered_words).most_common(max_nodes))
        
        # Create nodes
        nodes = []
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3']
        for i, (word, freq) in enumerate(top_words.items()):
            nodes.append(NetworkNode(
                id=word,
                label=word,
                size=freq * 2,  # Scale size
                color=colors[i % len(colors)]
            ))
        
        # Create edges
        edges = []
        for (word1, word2), count in word_pairs.items():
            if word1 in top_words and word2 in top_words:
                edges.append(NetworkEdge(
                    source=word1,
                    target=word2,
                    weight=count / 10,  # Scale weight
                    color='#95a5a6'
                ))
        
        return NetworkData(
            nodes=nodes,
            edges=edges,
            title="Word Co-occurrence Network",
            layout="force"
        )
    
    async def _get_topic_similarity_network(self) -> NetworkData:
        """Generate topic similarity network"""
        if self.topics_df is None:
            return NetworkData(nodes=[], edges=[], title="No Topic Data")
        
        # Calculate topic similarities
        topic_words = {}
        for col in self.topics_df.columns:
            if col.startswith('Topic'):
                topic_id = int(col.split()[1])
                words = set(self.topics_df[col].dropna().tolist())
                topic_words[topic_id] = words
        
        # Create nodes
        nodes = []
        for topic_id, words in topic_words.items():
            nodes.append(NetworkNode(
                id=f"topic_{topic_id}",
                label=f"Topic {topic_id}",
                size=len(words) * 2,
                color=f"hsl({topic_id * 40}, 70%, 50%)"
            ))
        
        # Create edges based on similarity
        edges = []
        topics = list(topic_words.keys())
        for i, topic1 in enumerate(topics):
            for topic2 in topics[i+1:]:
                words1 = topic_words[topic1]
                words2 = topic_words[topic2]
                
                if words1 and words2:
                    # Jaccard similarity
                    intersection = words1.intersection(words2)
                    union = words1.union(words2)
                    similarity = len(intersection) / len(union) if union else 0
                    
                    if similarity > 0.1:  # Only include significant similarities
                        edges.append(NetworkEdge(
                            source=f"topic_{topic1}",
                            target=f"topic_{topic2}",
                            weight=similarity,
                            color='#3498db'
                        ))
        
        return NetworkData(
            nodes=nodes,
            edges=edges,
            title="Topic Similarity Network",
            layout="circular"
        )
    
    async def get_comprehensive_statistics(self) -> StatisticsResponse:
        """
        Get comprehensive dataset statistics
        
        Frontend Usage:
        - Dashboard cards: Display key metrics
        - Overview charts: Use topic_distribution and temporal_trends
        """
        if self.df is None:
            return StatisticsResponse(
                total_articles=0,
                articles_with_topics=0,
                articles_with_year=0,
                unique_topics=0
            )
        
        # Basic statistics
        total_articles = len(self.df)
        articles_with_topics = len(self.df[self.df['topic'].notna() & (self.df['topic'] != -1)])
        articles_with_year = len(self.df[self.df['year'].notna()])
        unique_topics = self.df['topic'].nunique() - (1 if -1 in self.df['topic'].values else 0)
        
        # Year range
        year_range = None
        if articles_with_year > 0:
            years = self.df['year'].dropna()
            year_range = {"min": int(years.min()), "max": int(years.max())}
        
        # Average word count
        avg_word_count = self.df['word_count'].mean() if 'word_count' in self.df.columns else None
        
        # Get topic distribution
        topic_distribution = await self.get_topic_distribution()
        
        # Get temporal trends
        temporal_trends = await self.get_temporal_trends()
        
        return StatisticsResponse(
            total_articles=total_articles,
            articles_with_topics=articles_with_topics,
            articles_with_year=articles_with_year,
            unique_topics=unique_topics,
            year_range=year_range,
            average_word_count=round(avg_word_count, 1) if avg_word_count else None,
            topic_distribution=topic_distribution,
            temporal_trends=temporal_trends
        )
    
    async def get_topic_information(self) -> List[TopicInfo]:
        """
        Get detailed topic information
        
        Frontend Usage:
        - Topic selection dropdowns
        - Topic detail panels
        - Topic comparison views
        """
        if self.topics_df is None:
            return []
        
        topics = []
        for col in self.topics_df.columns:
            if col.startswith('Topic'):
                topic_id = int(col.split()[1])
                words = self.topics_df[col].dropna().tolist()
                
                # Count articles for this topic
                article_count = 0
                if self.df is not None:
                    article_count = len(self.df[self.df['topic'] == topic_id])
                
                topics.append(TopicInfo(
                    id=topic_id,
                    name=f"Topic {topic_id}",
                    description=f"Research topic focusing on {', '.join(words[:3])}",
                    top_words=words[:10],
                    article_count=article_count,
                    coherence_score=0.75  # Placeholder - would need actual calculation
                ))
        
        return sorted(topics, key=lambda x: x.article_count, reverse=True)
    
    async def get_chart_data(self, chart_type: str, topic_id: Optional[int] = None, 
                           year_range: Optional[str] = None) -> VisualizationData:
        """
        Get generic chart data for various visualization types
        
        Frontend Usage:
        - Flexible chart generation
        - Compatible with Chart.js, D3.js, etc.
        - Data structure optimized for common charting libraries
        """
        if self.df is None:
            return VisualizationData(
                chart_type="bar",
                title="No Data Available",
                data={}
            )
        
        # Filter data
        df_filtered = self.df.copy()
        if topic_id is not None:
            df_filtered = df_filtered[df_filtered['topic'] == topic_id]
        
        if year_range:
            start_year, end_year = map(int, year_range.split('-'))
            df_filtered = df_filtered[
                (df_filtered['year'] >= start_year) & 
                (df_filtered['year'] <= end_year)
            ]
        
        if chart_type == "word_count_distribution":
            return await self._get_word_count_chart(df_filtered)
        elif chart_type == "topic_evolution":
            return await self._get_topic_evolution_chart(df_filtered)
        elif chart_type == "publication_density":
            return await self._get_publication_density_chart(df_filtered)
        else:
            return VisualizationData(
                chart_type="bar",
                title="Unknown Chart Type",
                data={}
            )
    
    async def _get_word_count_chart(self, df: pd.DataFrame) -> VisualizationData:
        """Generate word count distribution chart"""
        word_counts = df['word_count'].dropna()
        
        # Create histogram bins
        bins = np.histogram(word_counts, bins=20)
        
        return VisualizationData(
            chart_type="histogram",
            title="Word Count Distribution",
            data={
                "labels": [f"{int(bins[1][i])}-{int(bins[1][i+1])}" for i in range(len(bins[0]))],
                "datasets": [{"data": bins[0].tolist(), "label": "Article Count"}]
            },
            x_axis="Word Count Range",
            y_axis="Number of Articles"
        )
    
    async def _get_topic_evolution_chart(self, df: pd.DataFrame) -> VisualizationData:
        """Generate topic evolution over time chart"""
        yearly_topic_counts = df.groupby(['year', 'topic']).size().unstack(fill_value=0)
        
        labels = yearly_topic_counts.index.tolist()
        datasets = []
        
        for topic in yearly_topic_counts.columns:
            if topic != -1:  # Skip unassigned
                datasets.append({
                    "label": f"Topic {int(topic)}",
                    "data": yearly_topic_counts[topic].tolist()
                })
        
        return VisualizationData(
            chart_type="line",
            title="Topic Evolution Over Time",
            data={
                "labels": labels,
                "datasets": datasets
            },
            x_axis="Year",
            y_axis="Number of Articles"
        )
    
    async def _get_publication_density_chart(self, df: pd.DataFrame) -> VisualizationData:
        """Generate publication density chart"""
        yearly_counts = df['year'].value_counts().sort_index()
        
        return VisualizationData(
            chart_type="bar",
            title="Publication Density Over Time",
            data={
                "labels": yearly_counts.index.tolist(),
                "datasets": [{"data": yearly_counts.values.tolist(), "label": "Publications"}]
            },
            x_axis="Year",
            y_axis="Number of Publications"
        )
    
    async def export_data(self, format: str, visualization_type: str) -> Dict[str, Any]:
        """
        Export visualization data in various formats
        
        Frontend Usage:
        - Download functionality
        - Data export buttons
        - External analysis tools integration
        """
        if format == "json":
            if visualization_type == "all":
                stats = await self.get_comprehensive_statistics()
                return {"data": stats.dict()}
            elif visualization_type == "topics":
                topics = await self.get_topic_information()
                return {"data": [topic.dict() for topic in topics]}
            elif visualization_type == "temporal":
                trends = await self.get_temporal_trends()
                return {"data": [trend.dict() for trend in trends]}
            else:
                return {"data": {}}
        
        elif format == "csv":
            # Return CSV data as string
            if visualization_type == "articles" and self.df is not None:
                csv_data = self.df.to_csv(index=False)
                return {"data": csv_data, "filename": "articles.csv"}
            else:
                return {"data": "", "filename": "empty.csv"}
        
        return {"data": {}}
