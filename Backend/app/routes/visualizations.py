"""
Visualization API routes for Space Biology Knowledge Engine
Provides endpoints for charts, graphs, and interactive visualizations
"""

from fastapi import APIRouter, HTTPException, Query, Path, Depends
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from collections import Counter
import json
import os

from app.models.article import (
    VisualizationData, TopicDistribution, TemporalAnalysis, 
    WordCloudData, NetworkData, NetworkNode, NetworkEdge,
    StatisticsResponse, TopicInfo
)
from app.services.visualization_service import VisualizationService

router = APIRouter()

# Dependency to get visualization service
def get_visualization_service():
    return VisualizationService()

@router.get("/visualizations/topic-distribution", response_model=List[TopicDistribution])
async def get_topic_distribution(
    visualization_service: VisualizationService = Depends(get_visualization_service)
):
    """
    Get topic distribution statistics
    
    Frontend Integration:
    - Use for pie charts and bar charts showing topic distribution
    - 'percentage' field for pie chart slices
    - 'article_count' for bar chart heights
    - 'top_words' for tooltips or legends
    
    Example Response:
    [
        {
            "topic_id": 0,
            "topic_name": "Spaceflight Research",
            "article_count": 146,
            "percentage": 25.7,
            "top_words": ["spaceflight", "microgravity", "space"]
        }
    ]
    """
    try:
        distribution = await visualization_service.get_topic_distribution()
        return distribution
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting topic distribution: {str(e)}")

@router.get("/visualizations/temporal-trends", response_model=List[TemporalAnalysis])
async def get_temporal_trends(
    start_year: Optional[int] = Query(None, ge=1990, le=2024),
    end_year: Optional[int] = Query(None, ge=1990, le=2024),
    visualization_service: VisualizationService = Depends(get_visualization_service)
):
    """
    Get temporal analysis data for publication trends
    
    Frontend Integration:
    - Use for line charts showing publication trends over time
    - 'year' for x-axis, 'article_count' for y-axis
    - 'topics' dict for multi-line charts (topic trends)
    
    Parameters:
    - start_year: Filter data from this year onwards
    - end_year: Filter data up to this year
    
    Example Response:
    [
        {
            "year": 2020,
            "article_count": 45,
            "topics": {0: 12, 1: 8, 2: 15}
        }
    ]
    """
    try:
        trends = await visualization_service.get_temporal_trends(start_year, end_year)
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting temporal trends: {str(e)}")

@router.get("/visualizations/word-cloud/{topic_id}", response_model=WordCloudData)
async def get_word_cloud_data(
    topic_id: int,
    max_words: int = Query(50, ge=10, le=200),
    visualization_service: VisualizationService = Depends(get_visualization_service)
):
    """
    Get word cloud data for a specific topic
    
    Frontend Integration:
    - Use for generating word clouds
    - 'words' dict contains word-frequency pairs
    - Higher frequency = larger word size
    - Use libraries like WordCloud.js or D3.js
    
    Parameters:
    - topic_id: Topic ID (-1 for all topics combined)
    - max_words: Maximum number of words to return
    
    Example Response:
    {
        "topic_id": 0,
        "words": {
            "spaceflight": 45,
            "microgravity": 32,
            "space": 28
        },
        "title": "Topic 0 Word Cloud"
    }
    """
    try:
        word_cloud = await visualization_service.get_word_cloud_data(topic_id, max_words)
        return word_cloud
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting word cloud data: {str(e)}")

@router.get("/visualizations/network", response_model=NetworkData)
async def get_network_data(
    network_type: str = Query("word_cooccurrence", description="Type: word_cooccurrence, topic_similarity"),
    min_frequency: int = Query(3, ge=1, description="Minimum word frequency for nodes"),
    max_nodes: int = Query(50, ge=10, le=200, description="Maximum number of nodes"),
    visualization_service: VisualizationService = Depends(get_visualization_service)
):
    """
    Get network visualization data
    
    Frontend Integration:
    - Use for network/graph visualizations
    - Libraries: D3.js, vis.js, Cytoscape.js
    - 'nodes' for graph nodes, 'edges' for connections
    - 'weight' determines edge thickness
    
    Parameters:
    - network_type: Type of network to generate
    - min_frequency: Minimum word frequency threshold
    - max_nodes: Maximum nodes to include
    
    Example Response:
    {
        "nodes": [
            {"id": "spaceflight", "label": "spaceflight", "size": 45, "color": "#ff6b6b"}
        ],
        "edges": [
            {"source": "spaceflight", "target": "microgravity", "weight": 0.8}
        ],
        "title": "Word Co-occurrence Network",
        "layout": "force"
    }
    """
    try:
        network = await visualization_service.get_network_data(network_type, min_frequency, max_nodes)
        return network
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting network data: {str(e)}")

@router.get("/visualizations/statistics", response_model=StatisticsResponse)
async def get_comprehensive_statistics(
    visualization_service: VisualizationService = Depends(get_visualization_service)
):
    """
    Get comprehensive dataset statistics
    
    Frontend Integration:
    - Use for dashboard overview cards
    - 'total_articles' for main statistics
    - 'topic_distribution' for charts
    - 'temporal_trends' for time series
    
    Example Response:
    {
        "total_articles": 624,
        "articles_with_topics": 569,
        "articles_with_year": 624,
        "unique_topics": 9,
        "year_range": {"min": 1990, "max": 2024},
        "average_word_count": 8.5,
        "topic_distribution": [...],
        "temporal_trends": [...]
    }
    """
    try:
        stats = await visualization_service.get_comprehensive_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

@router.get("/visualizations/topics", response_model=List[TopicInfo])
async def get_topic_information(
    visualization_service: VisualizationService = Depends(get_visualization_service)
):
    """
    Get detailed topic information
    
    Frontend Integration:
    - Use for topic selection dropdowns
    - Display topic names and descriptions
    - Show article counts for each topic
    
    Example Response:
    [
        {
            "id": 0,
            "name": "Spaceflight Research",
            "description": "Research on biological effects of spaceflight",
            "top_words": ["spaceflight", "microgravity", "space"],
            "article_count": 146,
            "coherence_score": 0.75
        }
    ]
    """
    try:
        topics = await visualization_service.get_topic_information()
        return topics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting topic information: {str(e)}")

@router.get("/visualizations/chart/{chart_type}", response_model=VisualizationData)
async def get_chart_data(
    chart_type: str,
    topic_id: Optional[int] = Query(None, description="Filter by topic ID"),
    year_range: Optional[str] = Query(None, description="Year range (e.g., '2020-2024')"),
    visualization_service: VisualizationService = Depends(get_visualization_service)
):
    """
    Get generic chart data for various visualization types
    
    Frontend Integration:
    - Flexible endpoint for different chart types
    - 'chart_type' determines the visualization
    - 'data' field contains chart-specific data
    - Use with Chart.js, D3.js, or other charting libraries
    
    Supported chart_types:
    - 'word_count_distribution': Histogram of word counts
    - 'topic_evolution': Topic trends over time
    - 'publication_density': Publications per year
    - 'topic_coherence': Topic quality scores
    
    Example Response:
    {
        "chart_type": "bar",
        "title": "Topic Distribution",
        "data": {
            "labels": ["Topic 0", "Topic 1"],
            "datasets": [{"data": [146, 89]}]
        },
        "x_axis": "Topics",
        "y_axis": "Article Count"
    }
    """
    try:
        chart_data = await visualization_service.get_chart_data(chart_type, topic_id, year_range)
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting chart data: {str(e)}")

@router.get("/visualizations/export/{format}")
async def export_visualization_data(
    format: str = Path(..., description="Export format: json, csv"),
    visualization_type: str = Query("all", description="Type of data to export"),
    visualization_service: VisualizationService = Depends(get_visualization_service)
):
    """
    Export visualization data in various formats
    
    Frontend Integration:
    - Use for data export functionality
    - Download buttons for different formats
    - Useful for external analysis tools
    
    Parameters:
    - format: Export format (json, csv)
    - visualization_type: Type of data (all, topics, temporal, network)
    
    Returns:
    - JSON or CSV file download
    """
    try:
        export_data = await visualization_service.export_data(format, visualization_type)
        return export_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting data: {str(e)}")
