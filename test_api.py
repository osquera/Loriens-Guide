"""
Simple test script to verify the API endpoint functionality.
Run the server first with: python server.py
Then run this test with: python test_api.py
"""

import requests
import json


def test_get_guidance_endpoint():
    """Test the POST /api/get-guidance endpoint."""
    url = "http://localhost:8000/api/get-guidance"
    
    # Test data matching the problem statement
    payload = {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "question_text": "I'm looking for the exit, where is it?"
    }
    
    print("Testing POST /api/get-guidance endpoint...")
    print(f"Request payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"\nResponse (Status {response.status_code}):")
        print(json.dumps(result, indent=2))
        
        # Verify response structure
        assert "answer_text" in result, "Response missing 'answer_text' field"
        assert isinstance(result["answer_text"], str), "'answer_text' should be a string"
        assert len(result["answer_text"]) > 0, "'answer_text' should not be empty"
        
        print("\n✓ Test passed! API endpoint is working correctly.")
        return True
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to server. Is it running?")
        print("Start the server with: python server.py")
        return False
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        return False


def test_health_check():
    """Test the root health check endpoint."""
    url = "http://localhost:8000/"
    
    print("\n" + "="*60)
    print("Testing GET / health check endpoint...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        result = response.json()
        print(f"Response (Status {response.status_code}):")
        print(json.dumps(result, indent=2))
        
        print("\n✓ Health check passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Health check failed: {e}")
        return False


if __name__ == "__main__":
    print("="*60)
    print("Lórien's Guide API Test Suite")
    print("="*60)
    
    # Run tests
    test1 = test_health_check()
    test2 = test_get_guidance_endpoint()
    
    print("\n" + "="*60)
    if test1 and test2:
        print("All tests passed! ✓")
    else:
        print("Some tests failed. ✗")
    print("="*60)
