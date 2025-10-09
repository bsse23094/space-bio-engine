"""
Data exploration API routes
"""

from fastapi import APIRouter, HTTPException, Query, Depends, UploadFile, File
from typing import Dict, List, Any, Optional
import pandas as pd
from pathlib import Path
import tempfile
import os

from app.services.data_exploration_service import DataExplorationService

router = APIRouter()

# Dependency to get data exploration service
def get_data_exploration_service():
    return DataExplorationService()

@router.get("/data/overview")
async def get_dataset_overview(
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Get basic dataset overview"""
    try:
        overview = await data_service.get_dataset_overview()
        return overview
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/quality")
async def analyze_data_quality(
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Analyze data quality and completeness"""
    try:
        quality_analysis = await data_service.analyze_data_quality()
        return quality_analysis
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/text-analysis")
async def analyze_text_content(
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Analyze text content in the dataset"""
    try:
        text_analysis = await data_service.analyze_text_content()
        return text_analysis
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/publication-trends")
async def analyze_publication_trends(
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Analyze publication trends over time"""
    try:
        trends_analysis = await data_service.analyze_publication_trends()
        return trends_analysis
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/journal-distribution")
async def analyze_journal_distribution(
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Analyze journal distribution"""
    try:
        journal_analysis = await data_service.analyze_journal_distribution()
        return journal_analysis
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/author-distribution")
async def analyze_author_distribution(
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Analyze author distribution"""
    try:
        author_analysis = await data_service.analyze_author_distribution()
        return author_analysis
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/comprehensive-analysis")
async def get_comprehensive_analysis(
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Get comprehensive dataset analysis"""
    try:
        analysis = await data_service.get_comprehensive_analysis(file_path)
        return analysis
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/sample")
async def get_sample_data(
    n: int = Query(5, ge=1, le=100, description="Number of sample records"),
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Get sample data from dataset"""
    try:
        sample_data = await data_service.get_sample_data(n=n)
        return {"sample_data": sample_data, "count": len(sample_data)}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/data/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Upload and analyze a CSV dataset"""
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Analyze the uploaded dataset
            analysis = await data_service.get_comprehensive_analysis(tmp_file_path)
            
            # Add file info
            analysis["uploaded_file"] = {
                "filename": file.filename,
                "size": len(content),
                "content_type": file.content_type
            }
            
            return analysis
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/data/export-cleaned")
async def export_cleaned_dataset(
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    output_path: Optional[str] = Query(None, description="Output path for cleaned dataset"),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Export cleaned dataset"""
    try:
        cleaned_path = await data_service.export_cleaned_dataset(
            output_path=output_path
        )
        return {
            "message": "Cleaned dataset exported successfully",
            "output_path": cleaned_path
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/columns")
async def get_dataset_columns(
    file_path: Optional[str] = Query(None, description="Path to CSV file"),
    data_service: DataExplorationService = Depends(get_data_exploration_service)
):
    """Get dataset columns information"""
    try:
        df = await data_service.load_dataset(file_path)
        columns_info = []
        
        for col in df.columns:
            col_info = {
                "name": col,
                "dtype": str(df[col].dtype),
                "non_null_count": int(df[col].count()),
                "null_count": int(df[col].isnull().sum()),
                "unique_count": int(df[col].nunique())
            }
            
            # Add sample values for object columns
            if df[col].dtype == 'object':
                sample_values = df[col].dropna().head(3).tolist()
                col_info["sample_values"] = sample_values
            
            columns_info.append(col_info)
        
        return {
            "columns": columns_info,
            "total_columns": len(df.columns),
            "total_rows": len(df)
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
