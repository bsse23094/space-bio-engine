"""
Text preprocessing API routes
"""

from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from typing import Dict, List, Any, Optional
import pandas as pd
from pathlib import Path

from app.services.text_preprocessing_service import TextPreprocessingService
from app.services.data_exploration_service import DataExplorationService

router = APIRouter()

# Dependency to get text preprocessing service
def get_text_preprocessing_service():
    return TextPreprocessingService()

# Dependency to get data exploration service
def get_data_exploration_service():
    return DataExplorationService()

@router.post("/preprocessing/process-dataset")
async def process_dataset(
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    text_service: TextPreprocessingService = Depends(get_text_preprocessing_service),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Process dataset for text preprocessing"""
    try:
        # Load dataset
        df = await data_service.load_dataset(file_path)
        
        # Process dataset
        preprocessing_results, processed_df = await text_service.preprocess_dataset(df)
        
        # Save processed dataset in background
        background_tasks.add_task(
            text_service.save_processed_data, 
            processed_df
        )
        
        return {
            "message": "Dataset preprocessing completed",
            "results": preprocessing_results,
            "processed_shape": processed_df.shape
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preprocessing/topic-modeling")
async def perform_topic_modeling(
    n_topics: int = Query(5, ge=2, le=20, description="Number of topics"),
    file_path: Optional[str] = Query(None, description="Path to processed CSV file"),
    text_service: TextPreprocessingService = Depends(get_text_preprocessing_service),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Perform topic modeling on processed dataset"""
    try:
        # Load processed dataset
        if file_path:
            df = pd.read_csv(file_path)
        else:
            # Try to load from default processed file
            processed_path = Path("data/SB_publication_PMC_processed.csv")
            if processed_path.exists():
                df = pd.read_csv(processed_path)
            else:
                # Process dataset first
                raw_df = await data_service.load_dataset()
                _, df = await text_service.preprocess_dataset(raw_df)
        
        # Perform topic modeling
        topic_results, topic_df = await text_service.perform_topic_modeling(df, n_topics)
        
        # Save results
        output_path = Path("data/SB_publication_PMC_with_topics.csv")
        topic_df.to_csv(output_path, index=False)
        
        return {
            "message": "Topic modeling completed",
            "results": topic_results,
            "output_file": str(output_path)
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preprocessing/vocabulary")
async def get_vocabulary_analysis(
    file_path: Optional[str] = Query(None, description="Path to processed CSV file"),
    text_service: TextPreprocessingService = Depends(get_text_preprocessing_service)
):
    """Get vocabulary analysis from processed dataset"""
    try:
        # Load processed dataset
        if file_path:
            df = pd.read_csv(file_path)
        else:
            processed_path = Path("data/SB_publication_PMC_processed.csv")
            if not processed_path.exists():
                raise HTTPException(status_code=404, detail="Processed dataset not found. Please run preprocessing first.")
            df = pd.read_csv(processed_path)
        
        # Analyze vocabulary
        vocabulary_analysis = await text_service._analyze_vocabulary(df)
        
        return vocabulary_analysis
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preprocessing/summary")
async def get_preprocessing_summary(
    file_path: Optional[str] = Query(None, description="Path to processed CSV file"),
    text_service: TextPreprocessingService = Depends(get_text_preprocessing_service)
):
    """Get preprocessing summary"""
    try:
        # Load processed dataset
        if file_path:
            df = pd.read_csv(file_path)
        else:
            processed_path = Path("data/SB_publication_PMC_processed.csv")
            if not processed_path.exists():
                raise HTTPException(status_code=404, detail="Processed dataset not found. Please run preprocessing first.")
            df = pd.read_csv(processed_path)
        
        # Get summary
        summary = await text_service.get_preprocessing_summary(df)
        
        return summary
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preprocessing/clean-text")
async def clean_text(
    text: str,
    text_service: TextPreprocessingService = Depends(get_text_preprocessing_service)
):
    """Clean a single text string"""
    try:
        cleaned_text = text_service.clean_text(text)
        tokens = text_service.tokenize_text(cleaned_text)
        stemmed_tokens = text_service.stem_tokens(tokens)
        lemmatized_tokens = text_service.lemmatize_tokens(tokens)
        
        return {
            "original_text": text,
            "cleaned_text": cleaned_text,
            "tokens": tokens,
            "stemmed_tokens": stemmed_tokens,
            "lemmatized_tokens": lemmatized_tokens,
            "token_count": len(tokens)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preprocessing/tfidf-matrix")
async def create_tfidf_matrix(
    max_features: int = Query(1000, ge=100, le=5000, description="Maximum features"),
    file_path: Optional[str] = Query(None, description="Path to processed CSV file"),
    text_service: TextPreprocessingService = Depends(get_text_preprocessing_service)
):
    """Create TF-IDF matrix"""
    try:
        # Load processed dataset
        if file_path:
            df = pd.read_csv(file_path)
        else:
            processed_path = Path("data/SB_publication_PMC_processed.csv")
            if not processed_path.exists():
                raise HTTPException(status_code=404, detail="Processed dataset not found. Please run preprocessing first.")
            df = pd.read_csv(processed_path)
        
        # Create TF-IDF matrix
        tfidf_matrix, tfidf_vectorizer = await text_service.create_tfidf_matrix(df, max_features=max_features)
        
        # Save matrix and vectorizer
        import pickle
        matrix_path = Path("data/tfidf_matrix.pkl")
        vectorizer_path = Path("data/tfidf_vectorizer.pkl")
        
        with open(matrix_path, 'wb') as f:
            pickle.dump(tfidf_matrix, f)
        
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(tfidf_vectorizer, f)
        
        return {
            "message": "TF-IDF matrix created successfully",
            "matrix_shape": tfidf_matrix.shape,
            "vocabulary_size": len(tfidf_vectorizer.vocabulary_),
            "matrix_file": str(matrix_path),
            "vectorizer_file": str(vectorizer_path)
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preprocessing/topics")
async def get_topics(
    file_path: Optional[str] = Query(None, description="Path to dataset with topics"),
    text_service: TextPreprocessingService = Depends(get_text_preprocessing_service)
):
    """Get topic modeling results"""
    try:
        # Load dataset with topics
        if file_path:
            df = pd.read_csv(file_path)
        else:
            topics_path = Path("data/SB_publication_PMC_with_topics.csv")
            if not topics_path.exists():
                raise HTTPException(status_code=404, detail="Dataset with topics not found. Please run topic modeling first.")
            df = pd.read_csv(topics_path)
        
        if 'dominant_topic' not in df.columns:
            raise HTTPException(status_code=400, detail="Dataset does not contain topic information")
        
        # Analyze topics
        topic_stats = df['dominant_topic'].value_counts().to_dict()
        avg_confidence = df['topic_confidence'].mean() if 'topic_confidence' in df.columns else None
        
        return {
            "total_documents": len(df),
            "topic_distribution": topic_stats,
            "average_confidence": float(avg_confidence) if avg_confidence else None,
            "topics_found": len(topic_stats)
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preprocessing/word-frequency")
async def get_word_frequency(
    top_n: int = Query(50, ge=10, le=200, description="Number of top words"),
    file_path: Optional[str] = Query(None, description="Path to processed CSV file"),
    text_service: TextPreprocessingService = Depends(get_text_preprocessing_service)
):
    """Get word frequency analysis"""
    try:
        # Load processed dataset
        if file_path:
            df = pd.read_csv(file_path)
        else:
            processed_path = Path("data/SB_publication_PMC_processed.csv")
            if not processed_path.exists():
                raise HTTPException(status_code=404, detail="Processed dataset not found. Please run preprocessing first.")
            df = pd.read_csv(processed_path)
        
        # Get vocabulary analysis
        vocabulary_analysis = await text_service._analyze_vocabulary(df)
        
        # Return top words
        top_words = dict(list(vocabulary_analysis["top_words"].items())[:top_n])
        
        return {
            "total_vocabulary_size": vocabulary_analysis["total_vocabulary_size"],
            "total_word_count": vocabulary_analysis["total_word_count"],
            "top_words": top_words,
            "average_words_per_document": vocabulary_analysis["avg_words_per_document"]
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
