#!/usr/bin/env python3
"""
Test script for Space Biology Knowledge Engine API
"""

import requests
import json
import time
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_endpoint(endpoint, method="GET", data=None, params=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, params=params)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        print(f"✅ {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict) and len(result) > 0:
                print(f"   Response keys: {list(result.keys())}")
            else:
                print(f"   Response: {result}")
        else:
            print(f"   Error: {response.text}")
        
        print()
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint}")
        print(f"   Error: Could not connect to API server")
        print(f"   Make sure the server is running at {BASE_URL}")
        print()
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint}")
        print(f"   Error: {str(e)}")
        print()
        return False

def main():
    """Run API tests"""
    print("🚀 Testing Space Biology Knowledge Engine API")
    print("=" * 50)
    
    # Test basic endpoints
    print("Testing basic endpoints...")
    test_api_endpoint("/")
    test_api_endpoint("/health")
    
    # Test data exploration endpoints
    print("Testing data exploration endpoints...")
    test_api_endpoint("/api/v1/data/overview")
    test_api_endpoint("/api/v1/data/quality")
    test_api_endpoint("/api/v1/data/text-analysis")
    test_api_endpoint("/api/v1/data/comprehensive-analysis")
    test_api_endpoint("/api/v1/data/sample", params={"n": 3})
    
    # Test text preprocessing endpoints
    print("Testing text preprocessing endpoints...")
    test_api_endpoint("/api/v1/preprocessing/summary")
    test_api_endpoint("/api/v1/preprocessing/vocabulary")
    test_api_endpoint("/api/v1/preprocessing/word-frequency", params={"top_n": 10})
    
    # Test article endpoints
    print("Testing article endpoints...")
    test_api_endpoint("/api/v1/articles")
    test_api_endpoint("/api/v1/articles/stats")
    test_api_endpoint("/api/v1/articles/search", params={"q": "space"})
    
    # Test text cleaning endpoint
    print("Testing text cleaning...")
    test_api_endpoint(
        "/api/v1/preprocessing/clean-text",
        method="POST",
        data={"text": "This is a test text with HTML <b>tags</b> and URLs https://example.com"}
    )
    
    print("=" * 50)
    print("✅ API testing completed!")
    print(f"📖 API Documentation: {BASE_URL}/docs")
    print(f"📋 ReDoc Documentation: {BASE_URL}/redoc")

if __name__ == "__main__":
    main()
